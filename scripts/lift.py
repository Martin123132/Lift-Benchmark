#!/usr/bin/env python3
"""LIFT-100 pilot records: initialize, seal, and validate offline. No hardware control."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

VERSION = "0.3-pilot"
ROOT = Path(__file__).resolve().parents[1]
SUMMARY_KEYS = (
    "physical_build_spend_cents", "economic_spend_cents", "revenue_cents",
    "asset_sale_proceeds_cents", "refunds_cents", "peak_cleared_capital_cents",
    "final_cleared_capital_cents",
)


class Invalid(ValueError):
    """A record is incomplete, unsafe to read, or internally inconsistent."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Invalid(message)


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_finite(value: Any) -> None:
    if isinstance(value, float):
        require(math.isfinite(value), "non-finite JSON number")
    elif isinstance(value, dict):
        for item in value.values():
            check_finite(item)
    elif isinstance(value, list):
        for item in value:
            check_finite(item)


def decode(text: str) -> Any:
    value = json.loads(text, object_pairs_hook=no_duplicates)
    check_finite(value)
    return value


def read_json(path: Path) -> Any:
    return decode(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def checked_file(folder: Path, relative: str) -> Path:
    """Evidence stays inside the run folder; URLs and symlinks are not followed."""
    require(isinstance(relative, str) and bool(relative.strip()), "empty file reference")
    require("\\" not in relative and ":" not in relative, f"use a relative POSIX path: {relative}")
    p = Path(relative)
    require(not p.is_absolute() and ".." not in p.parts, f"path escape: {relative}")
    candidate = folder
    for part in p.parts:
        candidate = candidate / part
        require(not candidate.is_symlink(), f"symlink not allowed: {relative}")
    require(candidate.is_file(), f"missing file: {relative}")
    require(candidate.stat().st_size > 0, f"empty evidence/file: {relative}")
    return candidate


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def moment(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(dt.tzinfo is not None and dt.utcoffset() is not None, "timestamp needs a timezone")
    return dt.astimezone(timezone.utc)


def schema_check(kind: str, value: Any) -> None:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise Invalid("Install dependencies: python -m pip install -r requirements.txt") from exc
    schema = read_json(ROOT / "schemas" / f"{kind}.schema.json")
    Draft202012Validator.check_schema(schema)
    formats = FormatChecker()

    @formats.checks("date-time", raises=(ValueError, TypeError))
    def zoned_timestamp(item: Any) -> bool:
        # Do not depend on jsonschema's optional format-validation packages.
        pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
        return (isinstance(item, str) and re.fullmatch(pattern, item) is not None
                and datetime.fromisoformat(item.replace("Z", "+00:00")).utcoffset() is not None)

    errors = sorted(Draft202012Validator(schema, format_checker=formats).iter_errors(value),
                    key=lambda e: str(list(e.absolute_path)))
    if errors:
        details = "; ".join(f"{'.'.join(map(str, e.absolute_path)) or '$'}: {e.message}" for e in errors[:8])
        raise Invalid(f"{kind} schema: {details}")


def load_config(folder: Path) -> dict[str, Any]:
    config = read_json(checked_file(folder, "run.json"))
    schema_check("run", config)
    require(config["checkpoint_hours"] == sorted(config["checkpoint_hours"]), "checkpoints must be ascending")
    moment(config["started_at"])
    checked_file(folder, config["safety_plan_ref"])
    return config


def seal(folder: Path) -> dict[str, Any]:
    """Seal completed inputs before the planned start; never overwrite a seal."""
    config = load_config(folder)
    require(not (folder / "registration.json").exists(), "registration already exists; use a new run")
    now = datetime.now(timezone.utc)
    require(now <= moment(config["started_at"]), "cannot preregister after the declared start")
    prompt = checked_file(folder, "model_prompt.md")
    registration = {
        "sealed_at": now.isoformat(), "config_sha256": digest(folder / "run.json"),
        "prompt_sha256": digest(prompt),
        "safety_plan_sha256": digest(checked_file(folder, config["safety_plan_ref"])),
    }
    write_json(folder / "registration.json", registration)
    return registration


def check_registration(folder: Path, config: dict[str, Any]) -> None:
    registration = read_json(checked_file(folder, "registration.json"))
    require(isinstance(registration, dict), "registration must be an object")
    require(moment(registration["sealed_at"]) <= moment(config["started_at"]), "registration is after start")
    for key, filename in (("config_sha256", "run.json"), ("prompt_sha256", "model_prompt.md"),
                          ("safety_plan_sha256", config["safety_plan_ref"])):
        require(registration[key] == digest(checked_file(folder, filename)), f"registration hash mismatch: {filename}")


def load_ledger(folder: Path) -> list[dict[str, Any]]:
    path = folder / "ledger.jsonl"
    require(path.is_file() and not path.is_symlink(), "missing ledger.jsonl or symlink")
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require(bool(line.strip()), f"ledger line {line_number}: blank line")
        try:
            row = decode(line)
            schema_check("transaction", row)
            rows.append(row)
        except (Invalid, ValueError) as exc:
            raise Invalid(f"ledger line {line_number}: {exc}") from exc
    return rows


def replay(config: dict[str, Any], rows: list[dict[str, Any]], end: datetime,
           folder: Path) -> dict[str, int]:
    balance = config["starting_capital_cents"]
    totals = dict.fromkeys(SUMMARY_KEYS, 0)
    totals["peak_cleared_capital_cents"] = balance
    entries: dict[str, dict[str, Any]] = {}
    references: set[str] = set()
    refunded: dict[str, int] = {}
    previous = start = moment(config["started_at"])
    for row in rows:
        key = row["entry_id"]
        require(key not in entries, f"duplicate entry_id: {key}")
        require(row["external_reference"] not in references, f"duplicate external_reference: {row['external_reference']}")
        at = moment(row["at"])
        require(start <= at <= end, f"transaction outside run: {key}")
        require(at >= previous, f"ledger is not chronological: {key}")
        previous = at
        checked_file(folder, row["evidence_ref"])
        amount, kind = row["amount_cents"], row["kind"]
        if kind == "spend":
            require(balance >= amount, f"insufficient cleared capital before {key}")
            balance -= amount
            field = "physical_build_spend_cents" if row["purpose"] == "build" else "economic_spend_cents"
            totals[field] += amount
        else:
            if kind == "refund":
                target = row["refund_of"]
                require(target in entries and entries[target]["kind"] == "spend", f"refund has no prior spend: {key}")
                require(entries[target]["purpose"] == row["purpose"], f"refund purpose mismatch: {key}")
                refunded[target] = refunded.get(target, 0) + amount
                require(refunded[target] <= entries[target]["amount_cents"], f"refund exceeds original spend: {key}")
            field = {"revenue": "revenue_cents", "asset_sale": "asset_sale_proceeds_cents", "refund": "refunds_cents"}[kind]
            balance += amount
            totals[field] += amount
        require(row["balance_after_cents"] == balance, f"balance mismatch after {key}: expected {balance}")
        totals["peak_cleared_capital_cents"] = max(totals["peak_cleared_capital_cents"], balance)
        entries[key] = row
        references.add(row["external_reference"])
    totals["final_cleared_capital_cents"] = balance
    return totals


def validate(folder: Path, allow_synthetic: bool = False) -> dict[str, Any]:
    folder = folder.resolve()
    config = load_config(folder)
    check_registration(folder, config)
    result = read_json(checked_file(folder, "result.json"))
    schema_check("result", result)
    require(result["run_id"] == config["run_id"], "run_id mismatch")
    require(allow_synthetic or result["record_type"] == "physical", "synthetic fixture rejected; use --allow-synthetic for software tests only")
    start, end = moment(config["started_at"]), moment(result["ended_at"])
    require(end >= start, "end precedes start")
    require(result["qualifying_height_m"] <= result["max_observed_height_m"], "qualifying height exceeds observed peak")
    require(result["official_height_m"] <= result["max_observed_height_m"], "official height exceeds observed peak")
    if result["qualifying_height_m"] > 0:
        require(result["verification_hold_s"] >= 5, "positive qualifying height needs a five-second hold")
    if result["mission_success"]:
        require(result["official_height_m"] == result["qualifying_height_m"], "official score must equal qualifying held height")
    usage = result["usage"]
    if any(usage[k] is None for k in ("input_tokens", "output_tokens", "reasoning_tokens", "tool_calls", "compute_cost_usd")):
        require(bool(usage["unavailable_reason"].strip()), "explain unavailable usage; do not substitute zero")
    for ref in result["evidence"].values():
        checked_file(folder, ref)
    totals = replay(config, load_ledger(folder), end, folder)
    for key, expected in totals.items():
        require(result["economics"][key] == expected, f"economic summary mismatch: {key}; expected {expected}")
    warnings = [
        "Internal record checks only: evidence authenticity, actual hold/recovery, revenue eligibility and safety require human review.",
        "A local hash seal is not independent timestamp evidence; review the external preregistration reference.",
    ]
    if config["outstanding_rule_decisions"]:
        warnings.append("Unresolved rule decisions: exploratory pilot only, not comparison-ready.")
    if result["record_type"] == "synthetic":
        warnings.append("SYNTHETIC SOFTWARE FIXTURE: not a physical result and never a leaderboard entry.")
    return {
        "records_consistent": True, "verification_level": "records_checked_only", "schema_version": VERSION,
        "run_id": result["run_id"], "record_type": result["record_type"],
        "declared_official_height_m": result["official_height_m"],
        "elapsed_seconds": (end - start).total_seconds(), "economics": totals, "warnings": warnings,
    }


def initialize(folder: Path, run_id: str, operation: str, procurement: str) -> None:
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", run_id)), "invalid run ID")
    require(not folder.exists(), "destination already exists; nothing overwritten")
    config = {k: None for k in read_json(ROOT / "schemas/run.schema.json")["required"]}
    seed = 10000 if operation == "standard" else 14000
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True, check=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = None
    config.update(schema_version=VERSION, run_id=run_id, rules_commit=commit, operation=operation,
                  procurement=procurement, starting_capital_cents=seed, checkpoint_hours=[],
                  available_tools=[], free_infrastructure=[], outstanding_rule_decisions=[],
                  safety_plan_ref="evidence/safety-plan.md")
    prompt = (ROOT / "docs/MODEL_PROMPT.md").read_text(encoding="utf-8")
    # Two exact substitutions keep the participant prompt free of mechanism suggestions.
    if operation == "autonomous":
        prompt = prompt.replace("**$100 USD", "**$140 USD")
        prompt = prompt.replace("In the standard class, the operator may switch the completed system on and off when you explicitly instruct them.",
                                "In the autonomous class, you must initiate, manage and terminate the mission through the computer interface. No human may operate the system during the mission except for an emergency stop.")
    folder.mkdir(parents=True)
    (folder / "evidence").mkdir()
    write_json(folder / "run.json", config)
    (folder / "model_prompt.md").write_text(prompt, encoding="utf-8")
    (folder / "ledger.jsonl").write_text("", encoding="utf-8")
    result = {k: None for k in read_json(ROOT / "schemas/result.schema.json")["required"]}
    result.update(schema_version=VERSION, run_id=run_id, record_type="physical", notes="",
                  economics={k: None for k in SUMMARY_KEYS},
                  usage={k: None for k in ("input_tokens", "output_tokens", "reasoning_tokens", "tool_calls",
                         "compute_cost_usd", "human_build_minutes", "human_business_minutes", "human_other_minutes")},
                  evidence={k: None for k in ("conversation", "operator_log", "measurement", "mission", "payload")})
    result["usage"]["unavailable_reason"] = ""
    write_json(folder / "result.json", result)
    (folder / "operator-log.md").write_text("# Operator log\n\nRecord every model instruction, human action, elapsed time, transaction, failure and safety stop. No entries yet.\n", encoding="utf-8")
    (folder / "evidence/README.md").write_text("# Evidence\n\nAdd real evidence locally. Remove personal/account information before sharing. Do not upload this folder automatically.\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create an incomplete starter folder without overwriting")
    init.add_argument("folder", type=Path)
    init.add_argument("--run-id", required=True)
    init.add_argument("--operation", choices=["standard", "autonomous"], default="standard")
    init.add_argument("--procurement", choices=["controlled", "open-market"], default="open-market")
    sealed = sub.add_parser("seal", help="validate and hash completed preregistration inputs")
    sealed.add_argument("folder", type=Path)
    check = sub.add_parser("validate", help="check a completed run; does not verify physical evidence")
    check.add_argument("folder", type=Path)
    check.add_argument("--allow-synthetic", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            initialize(args.folder, args.run_id, args.operation, args.procurement)
            print("Starter created. Complete null fields, supply the safety plan, then seal before the planned start. No experiment has been run.")
        else:
            report = seal(args.folder) if args.command == "seal" else validate(args.folder, args.allow_synthetic)
            print(json.dumps(report, indent=2, allow_nan=False))
        return 0
    except (Invalid, OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        print(json.dumps({"records_consistent": False, "error": str(exc)}, allow_nan=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
