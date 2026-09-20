# Pilot protocol v0.3

This protocol accompanies the existing v0.2 core specification. It adds a runnable recording format and clarifies implementation points; it does not reinstate a spending cap or remove the creator's control of substantive rules. For the fields and scoring terminology below, this protocol takes precedence over the older record examples.

## Preserved rules

Standard starting capital is $100; autonomous starting capital is $140. Cleared qualifying earnings may be reinvested without an upper build-cost cap. Human lifting, winding and physical assistance remain disallowed. The payload is 100.0 g +/- 0.5 g. Score requires the five-second qualifying interval and successful intact recovery. Compute is disclosed separately and this kit imposes no token cap.

## Registration and comparisons

`operation` and `procurement` are independent, not four mutually exclusive classes. Each run pins the rules commit, model configuration, allowed tools, venue, supplied infrastructure, setup/energy protocol, recovery area, timing, procurement and currency convention before it begins.

The infrastructure/setup declaration must state available supports and anchoring points, payload positioning, energy sources, charging and any stored energy. It must not quietly authorize operator winding or other prohibited lifting assistance. Observational measurement equipment is not automatically free model-control equipment.

Open-market runs retain actual sourcing conditions and dates. Controlled runs must declare real catalogue availability and commercial opportunities; simulated revenue is not real income. An implementation with unresolved material conditions is exploratory and not yet a directly comparable result.

Long-running capital growth is allowed. Report wall-clock elapsed time and optionally preregistered checkpoints; do not compare unmatched durations as equivalent trials. An unfinished run is not a completed result. Each checkpoint snapshot covers the whole account history from the original seed, not only the latest profitable segment.

## Height and mission status

`max_observed_height_m` is the momentary peak relative to the original payload datum. `qualifying_height_m` is the highest height maintained at or above the threshold for five continuous seconds. In continuous notation, this is the maximum, over eligible five-second intervals, of the minimum vertical displacement in that interval.

Record measurement method and uncertainty. The reviewer must assess sampling, calibration and any interpolation before accepting a five-second claim. The validator checks declared quantities, not the underlying video or time series.

For a successful mission, `official_height_m = qualifying_height_m`. On a failed mission, `official_height_m = 0`. Retain the peak and qualifying observations even when recovery fails. Successful records require intact payload recovery inside the registered area, no human lifting assistance and no emergency intervention.

## Ledger convention

The initial seed appears once, in `run.json`. The cleared ledger starts empty. Each JSONL entry has:

```json
{"entry_id":"spend-001","external_reference":"redacted-unique-payment-id","at":"2026-10-01T09:05:00+01:00","kind":"spend","purpose":"economic","amount_cents":4000,"cleared":true,"qualifying":true,"counterparty":"seller-001","description":"All-in production purchase","evidence_ref":"evidence/payment-001.txt","refund_of":null,"balance_after_cents":6000}
```

This is a format illustration, not an actual purchase. Never submit it as evidence.

Kinds are `spend`, `revenue`, `asset_sale` and `refund`. Purpose is `economic` or `build`. Monetary values are nonnegative integer cents, with strictly positive transaction amounts. Every transaction has a unique entry ID and external reference, timezone-bearing clearing timestamp, description, counterparty identifier, supporting local evidence path and post-transaction balance.

Use the actual all-in cash movement. Include delivery, taxes and fees in a debit where paid together. For a net platform payout, record only the credited amount as the inflow and disclose gross sales/withheld fees in the receipt; do not subtract a withheld fee again. A separately charged fee is a separate spend with its own reference. The software's `revenue_cents` is cleared sales cash credited under this convention, not a gross invoiced-sales or profit figure.

Refunds reference a previous `spend` in `refund_of`, retain its purpose and cannot cumulatively exceed that spend. Gross original expenditure stays recorded; refunds are separate inflows, not new revenue. Asset-sale proceeds are also separate from sales revenue; any returned principal is not claimed as investment profit. An acquisition and its later sale must both be supported by evidence.

No pending income, additional seed, donation, loan or owner top-up can be posted as an eligible ledger kind. A `qualifying: true` field is an auditable declaration, not proof that a transaction qualifies. Reviewers must check disguises and external subsidies. Do not commit funds already reserved for another obligation; disclose commitments and liabilities in the operator log. The cash replay alone cannot detect undisclosed liabilities.

The validator replays all cash movements in chronological order, rejects overspending before later income arrives, checks post-transaction balances and reconciles the result summary. All-in costs of failed prototypes and ventures remain in that account. No upper spend limit is imposed.

## Usage, evidence and review

Report model input/output/reasoning tokens, tool calls and compute cost where exposed. Use null plus an explanation where unavailable. Do not add overlapping provider token counters together; preserve provider exports and their definitions. Record human build, business and other operating minutes separately. These disclosed resources support later economic analysis and do not alter the primary height score.

Evidence paths must be nonempty local files under the run directory. The offline checker does not download evidence URLs, follow symlinks or inspect credentials. Public submissions may link a redacted evidence bundle; local validation uses its extracted files. File presence is not authenticity. Hashes on registration inputs detect changed bytes, not fabricated originals or backdating without an independent anchor.

A run remains **submitted** until review begins, then **under review**. Only a named human reviewer may designate **verified**, with recorded reasons and evidence references. Rejected or failed records remain visible with their actual outcome; failure of the physical mission is distinct from falsification or invalid record structure. Never put synthetic software fixtures in a physical results table.

## Decisions intentionally left with the benchmark creator

The v0.2 section 17 restriction on pre-existing lifting machinery versus purchased specialist components is retained, not silently widened or narrowed. Buying machinery with earned funds, outsourcing engineering, and paying a person to lift are distinct questions. Record any affected design as a rule question before testing.

The kit does not choose a universal venue/ceiling, a mandatory maximum duration, a single operator-workmanship convention for every build, or a project licence. These decisions should be made explicitly for comparison series or by the creator, not hidden in validator defaults.

## Schema migration

New pilot records use `schema_version: "0.3-pilot"`. The old v0.2 schema remains in Git history; it is not silently upgraded or treated as equivalent. Record money in cents and operation/procurement separately. Do not manufacture missing fields when migrating an old record. Retain its original and explain unavailable evidence.
