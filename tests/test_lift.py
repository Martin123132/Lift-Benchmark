"""Synthetic records only. No tests operate hardware, spend money, or report real lifts."""
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lift", ROOT / "scripts/lift.py")
lift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lift)


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / "run"
        self.folder.mkdir()
        (self.folder / "evidence").mkdir()
        (self.folder / "evidence/synthetic.txt").write_text("SYNTHETIC SOFTWARE FIXTURE. NO PHYSICAL LIFT OR PAYMENT.\n")
        (self.folder / "model_prompt.md").write_text("Synthetic prompt fixture.\n")
        self.config = dict(
            schema_version=lift.VERSION, run_id="synthetic-001", rules_commit="a" * 40,
            operation="standard", procurement="open-market", starting_capital_cents=10000,
            started_at="2026-01-01T00:01:00Z", checkpoint_hours=[24, 168],
            preregistration_ref="synthetic-only-reference", model="synthetic", model_version="test",
            provider="test", model_settings="test", available_tools=[], venue="synthetic",
            free_infrastructure=[], recovery_area="synthetic", setup_and_energy_protocol="synthetic",
            currency_conversion="USD cents; synthetic", procurement_protocol="synthetic", operator="synthetic",
            safety_plan_ref="evidence/synthetic.txt", outstanding_rule_decisions=[],
        )
        self.rows = [
            self.row("cost", "2026-01-01T00:02:00Z", "spend", "economic", 4000, 6000),
            self.row("sale", "2026-01-01T00:03:00Z", "revenue", "economic", 25000, 31000),
            self.row("build", "2026-01-01T00:04:00Z", "spend", "build", 28000, 3000),
        ]
        self.result = dict(
            schema_version=lift.VERSION, run_id="synthetic-001", record_type="synthetic",
            ended_at="2026-01-01T00:10:00Z", payload_mass_g=100.0,
            mission_success=True, max_observed_height_m=3.2, qualifying_height_m=3.0,
            verification_hold_s=5, official_height_m=3.0, measurement_uncertainty_m=0.01,
            measurement_method="synthetic fixture", recovery_success=True, payload_intact=True,
            recovery_in_area=True, human_assistance=False, emergency_intervention=False,
            economics=dict(physical_build_spend_cents=28000, economic_spend_cents=4000,
                revenue_cents=25000, asset_sale_proceeds_cents=0, refunds_cents=0,
                peak_cleared_capital_cents=31000, final_cleared_capital_cents=3000),
            usage=dict(input_tokens=None, output_tokens=None, reasoning_tokens=None, tool_calls=None,
                compute_cost_usd=None, unavailable_reason="Synthetic fixture; no model invocation.",
                human_build_minutes=0, human_business_minutes=0, human_other_minutes=0),
            evidence={k: "evidence/synthetic.txt" for k in ["conversation", "operator_log", "measurement", "mission", "payload"]},
            notes="SYNTHETIC ONLY: never include in results.",
        )
        self.save()

    @staticmethod
    def row(key, at, kind, purpose, amount, balance, refund_of=None):
        return dict(entry_id=key, external_reference="synthetic-" + key, at=at, kind=kind,
                    purpose=purpose, amount_cents=amount, cleared=True, qualifying=True,
                    counterparty="synthetic", description="synthetic fixture", evidence_ref="evidence/synthetic.txt",
                    refund_of=refund_of, balance_after_cents=balance)

    def save(self, reseal=True):
        lift.write_json(self.folder / "run.json", self.config)
        lift.write_json(self.folder / "result.json", self.result)
        (self.folder / "ledger.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.rows))
        if reseal:
            lift.write_json(self.folder / "registration.json", dict(
                sealed_at="2026-01-01T00:00:00Z", config_sha256=lift.digest(self.folder / "run.json"),
                prompt_sha256=lift.digest(self.folder / "model_prompt.md"),
                safety_plan_sha256=lift.digest(self.folder / self.config["safety_plan_ref"])))

    def check(self):
        self.save()
        return lift.validate(self.folder, allow_synthetic=True)

    def rejects(self, contains=None):
        self.save()
        with self.assertRaises(lift.Invalid) as exc:
            lift.validate(self.folder, allow_synthetic=True)
        if contains:
            self.assertIn(contains, str(exc.exception))

    def test_earnings_fund_build_above_seed(self):
        report = self.check()
        self.assertTrue(report["records_consistent"])
        self.assertEqual(report["economics"]["physical_build_spend_cents"], 28000)
        self.assertEqual(report["verification_level"], "records_checked_only")

    def test_million_dollar_build_has_no_spending_ceiling(self):
        self.rows[1].update(amount_cents=100_000_000, balance_after_cents=100_006_000)
        self.rows[2].update(amount_cents=100_000_000, balance_after_cents=6000)
        self.result["economics"].update(revenue_cents=100_000_000,
            physical_build_spend_cents=100_000_000, peak_cleared_capital_cents=100_006_000,
            final_cleared_capital_cents=6000)
        self.assertTrue(self.check()["records_consistent"])

    def test_synthetic_rejected_by_default(self):
        with self.assertRaisesRegex(lift.Invalid, "synthetic fixture rejected"):
            lift.validate(self.folder)

    def test_declared_physical_record_not_automatically_verified(self):
        self.result["record_type"] = "physical"  # Tests the label, not an actual physical result.
        self.save()
        report = lift.validate(self.folder)
        self.assertEqual(report["verification_level"], "records_checked_only")
        self.assertNotIn("verified", report)

    def test_failed_recovery_zero_score_can_be_valid_record(self):
        self.result.update(mission_success=False, recovery_success=False, official_height_m=0)
        self.assertTrue(self.check()["records_consistent"])

    def test_peak_spike_not_scored_as_held_height(self):
        self.result["max_observed_height_m"] = 100
        self.assertEqual(self.check()["declared_official_height_m"], 3)

    def test_refund_returns_cash_without_becoming_revenue(self):
        self.rows.append(self.row("refund", "2026-01-01T00:05:00Z", "refund", "build", 1000, 4000, "build"))
        self.result["economics"].update(refunds_cents=1000, final_cleared_capital_cents=4000)
        report = self.check()
        self.assertEqual(report["economics"]["revenue_cents"], 25000)

    def test_asset_sale_proceeds_kept_separate(self):
        self.rows.append(self.row("asset", "2026-01-01T00:05:00Z", "asset_sale", "economic", 500, 3500))
        self.result["economics"].update(asset_sale_proceeds_cents=500, final_cleared_capital_cents=3500)
        self.assertTrue(self.check()["records_consistent"])

    def test_autonomous_seed_valid(self):
        self.config.update(operation="autonomous", starting_capital_cents=14000)
        for row in self.rows:
            row["balance_after_cents"] += 4000
        self.result["economics"].update(peak_cleared_capital_cents=35000, final_cleared_capital_cents=7000)
        self.assertTrue(self.check()["records_consistent"])

    def test_controlled_and_autonomous_are_independent(self):
        self.config["procurement"] = "controlled"
        self.assertTrue(self.check()["records_consistent"])

    def test_standard_wrong_seed_rejected(self):
        self.config["starting_capital_cents"] = 100000
        self.rejects("run schema")

    def test_autonomous_wrong_seed_rejected(self):
        self.config["operation"] = "autonomous"
        self.rejects("run schema")

    def test_unresolved_rule_decision_warns(self):
        self.config["outstanding_rule_decisions"] = ["equipment boundary not settled"]
        self.assertTrue(any("exploratory pilot only" in w for w in self.check()["warnings"]))

    def test_overspend_before_later_income_rejected(self):
        self.rows[0]["amount_cents"] = 11000
        self.rejects("insufficient cleared capital")

    def test_duplicate_entry_rejected(self):
        self.rows[1]["entry_id"] = "cost"
        self.rejects("duplicate entry_id")

    def test_duplicate_external_payment_rejected(self):
        self.rows[1]["external_reference"] = self.rows[0]["external_reference"]
        self.rejects("duplicate external_reference")

    def test_uncleared_income_rejected(self):
        self.rows[1]["cleared"] = False
        self.rejects("transaction schema")

    def test_topup_rejected(self):
        self.rows[1]["kind"] = "owner_topup"
        self.rejects("transaction schema")

    def test_ineligible_income_rejected(self):
        self.rows[1]["qualifying"] = False
        self.rejects("transaction schema")

    def test_negative_money_rejected(self):
        self.rows[0]["amount_cents"] = -100
        self.rejects("transaction schema")

    def test_fractional_cents_rejected(self):
        self.rows[0]["amount_cents"] = 1.5
        self.rejects("transaction schema")

    def test_boolean_money_rejected(self):
        self.rows[0]["amount_cents"] = True
        self.rejects("transaction schema")

    def test_balance_mismatch_rejected(self):
        self.rows[1]["balance_after_cents"] += 1
        self.rejects("balance mismatch")

    def test_time_order_rejected(self):
        self.rows[1]["at"] = "2026-01-01T00:01:30Z"
        self.rejects("not chronological")

    def test_transaction_before_start_rejected(self):
        self.rows[0]["at"] = "2026-01-01T00:00:00Z"
        self.rejects("outside run")

    def test_transaction_after_end_rejected(self):
        self.rows[2]["at"] = "2026-01-01T01:00:00Z"
        self.rejects("outside run")

    def test_naive_timestamp_rejected(self):
        self.rows[0]["at"] = "2026-01-01T00:02:00"
        self.rejects("transaction schema")

    def test_refund_without_original_rejected(self):
        self.rows.append(self.row("r", "2026-01-01T00:05:00Z", "refund", "build", 1, 3001, "missing"))
        self.rejects("no prior spend")

    def test_refund_over_original_rejected(self):
        self.rows.append(self.row("r", "2026-01-01T00:05:00Z", "refund", "build", 28001, 31001, "build"))
        self.rejects("exceeds original")

    def test_cumulative_refunds_rejected(self):
        self.rows.extend([self.row("r1", "2026-01-01T00:05:00Z", "refund", "build", 20000, 23000, "build"),
            self.row("r2", "2026-01-01T00:06:00Z", "refund", "build", 10000, 33000, "build")])
        self.rejects("exceeds original")

    def test_refund_wrong_purpose_rejected(self):
        self.rows.append(self.row("r", "2026-01-01T00:05:00Z", "refund", "economic", 1, 3001, "build"))
        self.rejects("purpose mismatch")

    def test_summary_tampering_rejected(self):
        self.result["economics"]["physical_build_spend_cents"] -= 1
        self.rejects("economic summary mismatch")

    def test_missing_evidence_file_rejected(self):
        self.result["evidence"]["mission"] = "evidence/absent.txt"
        self.rejects("missing file")

    def test_evidence_path_escape_rejected(self):
        self.result["evidence"]["mission"] = "../secret.txt"
        self.rejects("path escape")

    def test_remote_evidence_not_fetched(self):
        self.result["evidence"]["mission"] = "https://example.invalid/file"
        self.rejects("relative POSIX path")

    def test_empty_evidence_rejected(self):
        (self.folder / "evidence/empty.txt").touch()
        self.result["evidence"]["mission"] = "evidence/empty.txt"
        self.rejects("empty evidence")

    def test_symlink_evidence_rejected(self):
        link = self.folder / "evidence/link.txt"
        try:
            link.symlink_to(self.folder / "evidence/synthetic.txt")
        except OSError:
            self.skipTest("symlinks unavailable on host")
        self.result["evidence"]["mission"] = "evidence/link.txt"
        self.rejects("symlink")

    def test_hash_change_detected(self):
        self.config["venue"] = "changed"
        self.save(reseal=False)
        with self.assertRaisesRegex(lift.Invalid, "hash mismatch"):
            lift.validate(self.folder, True)

    def test_prompt_change_detected(self):
        (self.folder / "model_prompt.md").write_text("Changed after registration")
        with self.assertRaisesRegex(lift.Invalid, "hash mismatch"):
            lift.validate(self.folder, True)

    def test_safety_plan_change_detected(self):
        (self.folder / "evidence/synthetic.txt").write_text("changed")
        with self.assertRaisesRegex(lift.Invalid, "hash mismatch"):
            lift.validate(self.folder, True)

    def test_late_registration_rejected(self):
        reg = lift.read_json(self.folder / "registration.json")
        reg["sealed_at"] = "2026-01-01T00:02:00Z"
        lift.write_json(self.folder / "registration.json", reg)
        with self.assertRaisesRegex(lift.Invalid, "after start"):
            lift.validate(self.folder, True)

    def test_new_registration_uses_real_current_time(self):
        self.config["started_at"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.save()
        (self.folder / "registration.json").unlink()
        registration = lift.seal(self.folder)
        self.assertLessEqual(lift.moment(registration["sealed_at"]), lift.moment(self.config["started_at"]))

    def test_seal_refuses_overwrite(self):
        with self.assertRaisesRegex(lift.Invalid, "already exists"):
            lift.seal(self.folder)

    def test_seal_refuses_backdated_registration(self):
        (self.folder / "registration.json").unlink()
        with self.assertRaisesRegex(lift.Invalid, "after the declared start"):
            lift.seal(self.folder)

    def test_init_refuses_overwrite(self):
        with self.assertRaisesRegex(lift.Invalid, "already exists"):
            lift.initialize(self.folder, "new", "standard", "open-market")

    def test_init_produces_incomplete_not_fake_result(self):
        folder = Path(self.tmp.name) / "new"
        lift.initialize(folder, "new", "standard", "open-market")
        self.assertIsNone(lift.read_json(folder / "result.json")["official_height_m"])
        self.assertEqual(lift.read_json(folder / "run.json")["starting_capital_cents"], 10000)
        with self.assertRaises(lift.Invalid):
            lift.validate(folder)

    def test_autonomous_init_prompt_matches_seed(self):
        folder = Path(self.tmp.name) / "auto"
        lift.initialize(folder, "auto", "autonomous", "open-market")
        prompt = (folder / "model_prompt.md").read_text()
        self.assertIn("**$140 USD", prompt)
        self.assertNotIn("**$100 USD", prompt)
        self.assertIn("No human may operate", prompt)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(lift.Invalid, "duplicate JSON key"):
            lift.decode('{"x": 1, "x": 2}')

    def test_nonfinite_json_rejected(self):
        for text in ['{"x": NaN}', '{"x": Infinity}', '{"x": 1e400}']:
            with self.subTest(text=text), self.assertRaises(lift.Invalid):
                lift.decode(text)

    def test_blank_ledger_line_rejected(self):
        (self.folder / "ledger.jsonl").write_text("\n")
        with self.assertRaisesRegex(lift.Invalid, "blank line"):
            lift.validate(self.folder, True)

    def test_missing_registration_cli_clean_error(self):
        (self.folder / "registration.json").unlink()
        with redirect_stderr(io.StringIO()) as err:
            status = lift.main(["validate", str(self.folder), "--allow-synthetic"])
        self.assertEqual(status, 1)
        self.assertFalse(json.loads(err.getvalue())["records_consistent"])

    def test_cli_success_is_records_only(self):
        with redirect_stdout(io.StringIO()) as out:
            status = lift.main(["validate", str(self.folder), "--allow-synthetic"])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(out.getvalue())["verification_level"], "records_checked_only")


# Each mutation is independently discovered/reported by unittest.
def add_result_test(name, changes):
    def test(self):
        self.result.update(changes)
        self.rejects()
    test.__name__ = name
    setattr(PilotTests, name, test)


for name, changes in {
    "test_one_second_hold_rejected": {"verification_hold_s": 1},
    "test_inflated_official_height_rejected": {"official_height_m": 100},
    "test_inflated_qualifying_height_rejected": {"qualifying_height_m": 100},
    "test_peak_instead_of_hold_rejected": {"official_height_m": 3.2},
    "test_failed_recovery_positive_score_rejected": {"recovery_success": False},
    "test_human_lifting_rejected": {"human_assistance": True},
    "test_emergency_stop_success_rejected": {"emergency_intervention": True},
    "test_damaged_payload_success_rejected": {"payload_intact": False},
    "test_outside_recovery_area_rejected": {"recovery_in_area": False},
    "test_wrong_payload_mass_rejected": {"payload_mass_g": 99},
    "test_end_before_start_rejected": {"ended_at": "2025-12-31T23:00:00Z"},
    "test_wrong_run_id_rejected": {"run_id": "different"},
    "test_negative_uncertainty_rejected": {"measurement_uncertainty_m": -1},
    "test_failed_mission_nonzero_score_rejected": {"mission_success": False},
}.items():
    add_result_test(name, changes)


def add_missing_test(name, key):
    def test(self):
        del self.result[key]
        self.rejects("result schema")
    setattr(PilotTests, name, test)


for key in ["verification_hold_s", "usage", "evidence", "economics"]:
    add_missing_test("test_missing_" + key + "_rejected", key)


if __name__ == "__main__":
    unittest.main()
