# Pilot-kit software test report

Date: 2026-09-20. Version: 0.3-pilot.

Local environment: Python 3.13.5; jsonschema 4.26.0.

Command: `python -m unittest discover -s tests -v`

Outcome: **70 tests passed, zero failures, zero errors, zero skips.**

All input records and payment/height examples in this test suite are synthetic software fixtures. No hardware was operated, no capital was spent or earned, and no physical benchmark result is reported.

Covered: above-seed reinvestment ($280 build and $1,000,000 build), correct class seed, ledger chronology and balances, duplicate payment references, uncleared or ineligible inflows, refunds, evidence-path handling, preregistration hashes, five-second hold, peak versus qualifying height, recovery conditions, missing fields and CLI behavior.

Schemas were syntax-checked with Draft202012Validator. YAML workflow, issue forms and citation metadata were parsed locally. These checks do not establish GitHub-hosted execution; consult the live workflow for that.

## Tested file SHA-256 values

- `scripts/lift.py`: `3b969e79217dc507c136fc7fdafa8d7176f9d6b1a5846cda8cb8c6b6ec472e4d`
- `tests/test_lift.py`: `4a53b7485b81de48954950b8ae15753555a376a36d014cc0da114a2dfd606e6a`
- `schemas/run.schema.json`: `30dbedb1da664bf6be423d9bb4b9ba0abd0e693bcde3287679aa7d64652177d5`
- `schemas/transaction.schema.json`: `21fc0acabf00df3332590dddc5cd0afc50316d430984a634cb1fd80bbcb3f98f`
- `schemas/result.schema.json`: `f578bf1e0cbb26ebe13dffb57cb99b4d9b43223cc3c4092c759067d316f75e26`
