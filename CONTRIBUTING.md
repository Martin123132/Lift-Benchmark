# Contributing

Start with the quickstart and the pinned core/pilot rules. Preserve the defining rule: **$100 is seed capital; qualifying earned capital may increase build expenditure without a ceiling.**

## Run submissions

Use the **Submit a run** issue form. Supply the rules commit, operation/procurement settings, model, preregistration reference, declared score and peak, capital summary, elapsed time, validator output and a redacted evidence bundle. Failures and incomplete evidence are useful when described accurately. An issue is a submission, not certification.

Reviewers check the original registration, inputs, transaction provenance, capital chronology, human involvement, payload mass, calibrated height/hold evidence and controlled intact recovery. Record the reviewer, date, version, decision and reasons before marking a result verified. A consistent JSON file is not a substitute for that review. Physical mission failure can itself be a verified observation.

## Rule questions

Use **Report a rule ambiguity**. Identify the exact section, a concrete scenario, why interpretations differ and the proposed clarification. Do not change benchmark outcomes retrospectively by quietly changing rules. Resolve material ambiguities before comparative runs; preserve exploratory records as exploratory.

## Code changes

Run `python -m unittest discover -s tests -v`. Add a regression test for every scoring/accounting fix. Keep the above-seed and million-dollar-build tests. Do not let a passing checker claim physical verification, hide failed attempts, invent token counts or convert a seed allowance into a spending cap.

Tests use synthetic records in temporary directories and must never control hardware or make real transactions. Keep public evidence separate from test fixtures. Explain schema changes and retain version provenance. The GitHub workflow runs tests with read-only repository permission and no secrets supplied to tests.

## Privacy and credits

Publish redacted copies, not credentials, customer identities, home addresses or complete account numbers. Preserve amounts, timestamps and stable transaction references needed for audit. Keep originals privately available under an agreed review arrangement. Check metadata and conversation exports before sharing.

Benchmark creator: Martin Ollett. Add contributor credits transparently. Licence selection is pending the owner's decision; do not add or change a licence as an incidental housekeeping edit.
