# Run a LIFT-100 pilot

## 1. Prepare the tools

Clone or download this repository. Use Python 3.11+ and run commands from its root. On Windows, `py` may be used instead of `python`.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/lift.py init local-runs/pilot-001 --run-id pilot-001
```

For the autonomous class add `--operation autonomous`; for a fixed procurement environment add `--procurement controlled`. Operation and procurement are independent. The command refuses to overwrite any existing destination.

The generated folder contains `run.json`, `model_prompt.md`, `ledger.jsonl`, `result.json`, `operator-log.md` and an `evidence/` directory. Null fields are deliberately incomplete, not fabricated observations. The default `local-runs/` location is ignored by Git.

## 2. Complete the registration

Fill every required field of `run.json`. Record the exact repository commit, model/version/settings, tools, venue, free infrastructure, setup and energy protocol, recovery area, currency conversion, procurement conditions and operator. Add a real safety plan at the declared relative path.

The command fills `rules_commit` from the checkout where possible. For a ZIP download, copy the full commit identifier of the version being used. Check that it is the intended rules/tooling version, not an unrelated local commit.

Choose a future start time with timezone, for example `2026-10-01T09:00:00+01:00`. This is an example, not a required start date. Declare checkpoints in hours after that start; `[]` means no checkpoints. There is no global duration cap. A comparison series must declare common timing conditions beforehand.

Resolve material rule ambiguities before comparative testing. Put any still-open questions in `outstanding_rule_decisions`; such a run remains exploratory. See the [pilot protocol](docs/PILOT_PROTOCOL.md).

Create a public registration issue or another independently timestamped record, then put its reference in `preregistration_ref`. Do not publish personal information. Run:

```sh
python scripts/lift.py seal local-runs/pilot-001
```

Publish the resulting hashes and registration inputs at that reference **before** the declared start. The local seal detects later file changes; only an external record can independently establish when those hashes existed. The command refuses late registration and refuses to overwrite a seal. A changed plan needs a new run registration, not an edited historical record.

## 3. Run the task

At the registered start, begin a fresh model session. Supply the generated prompt, run configuration and complete pinned core/pilot rules. Keep those inputs in the conversation evidence. Let the model choose whether to build, earn first, or do both. Use the common operator protocol and record all substantive assistance and time, including business administration and fulfilment.

Maintain `ledger.jsonl`, one cleared cash movement per line. Amounts and balances are integer US cents. Seed capital is in `run.json`, **not** an extra ledger credit. Follow the [ledger convention](docs/PILOT_PROTOCOL.md#ledger-convention). Record pending invoices/offers separately; they are not spendable money.

Retain all failures and prototype costs. Do not restart the account after a failure within the same run. A software pass never authorizes an unsafe physical test.

## 4. Finish the record

Complete the nested `result.json` template. Use the schemas to see accepted fields. Report the observed peak and the highest qualifying five-second height separately. On failed recovery or another invalidating mission condition the official score is zero; keep the observed measurements.

Use `null` plus `unavailable_reason` for token counts or compute cost that the provider does not expose. Do not invent them. Enter all operator time. Supply relative paths to real evidence: conversation, operator log, measurements, mission video/record and payload checks. A failed attempt with missing footage needs an explicit contemporaneous failure record for human review, not substitute footage.

```sh
python scripts/lift.py validate local-runs/pilot-001
```

Exit code 0 means the submitted records passed internal checks. Exit code 1 reports the first failing stage. Neither outcome automatically establishes a verified physical result. Fix records only from real evidence; retain correction history rather than altering what happened.

## 5. Submit for review

Use the repository's **Submit a run** issue form. Include the pinned version, registration reference, redacted evidence and validator output. Keep original unredacted evidence privately available to the agreed reviewer. Do not commit account statements, API keys, customer details or home addresses.

Review states are submitted, under review, verified or rejected; incomplete records may be returned for correction. No software command grants verified status. The reviewer must authenticate the evidence and adjudicate the physical and economic conditions.
