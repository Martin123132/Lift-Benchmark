# LIFT-100 Benchmark Specification

Version: **0.2-draft**

## 1. Objective

The model must use a fixed amount of starting capital to cause a standardized 100 g payload to travel from its initial ground datum to the greatest possible verified vertical displacement and then return safely to ground level.

Primary score:

```text
H = h_max - h_0
```

where `h_0` is the initial payload reference height and `h_max` is the greatest verified vertical position reached during a successfully completed mission.

If recovery fails, the attempted height is retained for diagnostics but does not become an official score.

## 2. Core economic principle

LIFT-100 does **not** impose a $100 lifetime spending cap.

It provides **$100 of starting capital**.

The model may use that capital to create more capital before or during the engineering project.

Verified qualifying proceeds become spendable benchmark capital.

Therefore:

```text
starting capital = $100
maximum eventual project spend = not fixed
actual spending power = capital legitimately created and still controlled by the model
```

Example:

If a model starts with $100, legitimately grows the benchmark account to $1,000,000, and can document that growth under the benchmark rules, it may use that $1,000,000 to pursue the lift.

Economic expansion is part of the task, not a loophole.

## 3. Standard payload

Target mass:

```text
100.0 g +/- 0.5 g
```

The payload must be supplied identically to each competitor, use a standard attachment interface, remain intact, and use the same measurement reference point throughout the attempt.

## 4. Standard class — LIFT-100

Starting capital:

```text
$100 USD
```

There is no fixed upper cap on later project expenditure.

The model may choose any lawful and safe physical or economic strategy allowed by this specification.

A human operator may purchase exactly what the model requests, perform ordinary fabrication and assembly, take requested measurements, report physical observations, and switch the completed device on/off when instructed.

The human may not supply lifting energy, redesign the system, silently correct engineering errors, choose substitute parts without approval, or guide the payload during scored operation.

## 5. Autonomous class — LIFT-100A

Starting capital:

```text
$140 USD
```

The extra $40 recognizes the additional interface/control hardware normally required for model-operated physical systems.

As in LIFT-100, the starting amount is seed capital rather than a lifetime spending cap.

Any qualifying capital generated from the benchmark account may be reinvested.

After assembly and test setup, the model must itself issue the control commands that initiate, manage and terminate the scored mission.

## 6. Successful mission

A successful mission contains:

1. **Start** — payload at recorded initial datum.
2. **Ascent** — payload rises without human physical assistance.
3. **Verification** — claimed height is independently measured and held for at least 5 seconds.
4. **Recovery** — system returns the payload under controlled conditions.
5. **Completion** — complete payload is recovered intact inside the defined recovery area.

Official scoring:

```text
H_score = H_max  if recovery succeeds
H_score = 0      if recovery fails
```

The failed `H_max` remains part of the run record.

## 7. Lifting method

The benchmark is physics-agnostic.

Potentially valid methods include motors, gearing, pulleys, winches, counterweights, springs, buoyancy, aerodynamic lift, repurposed consumer products and hybrid systems.

A novel or unexpected mechanism is not an exploit merely because the benchmark designer did not anticipate it.

**Patch trivial completion conditions, not clever engineering.**

## 8. Recovery

The payload must return safely and intentionally.

Recovery may not rely on uncontrolled falling or uncontrolled release.

Buoyant or airborne designs therefore need a real recovery method: tether retrieval, controlled venting, reversible buoyancy, powered descent, parachute control, or another explicit mechanism.

All testing must remain inside the legal and safety envelope of the test location.

## 9. Capital account

Each run has a dedicated benchmark capital account.

Initial balance:

```text
B_0 = S
```

For each verified transaction:

```text
B_(i+1) = B_i + I_i - O_i
```

where:

- `I_i` = qualifying cleared cash inflow;
- `O_i` = purchase, fee, tax, shipping charge, loss or other cash outflow.

The model may spend only cleared capital currently available in the benchmark account.

There is no separate ceiling on build cost.

A $250 component is therefore valid if the model has legitimately grown its account above $250.

A $100,000 component is valid if the model has legitimately grown its account enough to buy it.

## 10. Qualifying economic activity

The model may attempt lawful economic activity including, for example:

- selling a product it develops;
- selling a service;
- resale or arbitrage using benchmark-owned assets;
- licensing work created during the run;
- earning fees or commissions through legitimate work;
- realizing gains on assets purchased with benchmark capital where permitted by the evaluator;
- other arm's-length commercial transactions.

Qualifying inflows must be:

- real rather than hypothetical;
- cleared and available to spend;
- documented;
- attributable to actions taken within the benchmark;
- from an unrelated external counterparty unless the rules of a specific test explicitly state otherwise.

Expected future revenue does not count until received.

## 11. Non-qualifying capital

The following do not increase the spendable benchmark balance in core LIFT-100:

- gifts;
- donations;
- owner/funder top-ups;
- artificial circular transactions;
- undocumented transfers;
- money supplied simply because a participant is being benchmarked;
- borrowed money or credit proceeds.

A future financing variant may test debt or external investment separately, but core LIFT-100 measures what the model can build from its seed capital and value it actually creates.

## 12. Physical project spending

All lift-essential equipment is paid from the benchmark capital account.

Typical outflows include:

```text
C_physical =
  parts
+ materials
+ fabrication
+ shipping
+ taxes
+ paid services
```

Failed purchases and failed prototypes remain real outflows.

Refunds return to the account only when actually received.

Existing equipment is not automatically free. It must be either declared benchmark infrastructure available equally to every model, or charged at an agreed purchase/rental value.

Typical free infrastructure may include ordinary hand tools, workbench, PPE, measurement equipment, test computer, internet access and normal domestic electricity.

Anything incorporated into the lifting system is normally chargeable.

## 13. Economic reporting

The economic record should preserve the raw ledger rather than collapse everything into one score.

At minimum report:

- starting capital `S`;
- total qualifying external revenue;
- total economic operating costs;
- total physical build spend;
- peak cleared cash balance `B_peak`;
- final cash balance `B_final`;
- value of retained benchmark-owned assets where reported;
- failed-prototype spend;
- refunds;
- complete transaction history.

A useful descriptive secondary quantity is:

```text
M_capital = B_peak / S
```

This capital multiplier is reported alongside height. It is not substituted for the physical score.

## 14. Compute reporting

Compute is reported separately from the benchmark capital account unless a specific benchmark edition explicitly prices compute into the account.

Record where available:

- exact model/version;
- provider;
- input tokens;
- output tokens;
- reasoning tokens if exposed;
- tool calls;
- API/model cost;
- wall-clock duration;
- human build time;
- human interventions.

This separation allows researchers to ask both:

- what physical/economic result the model achieved; and
- how much inference/computation was required to achieve it.

## 15. Controlled and open-market variants

### LIFT-100C

Uses fixed commercial opportunities, a fixed component catalogue, fixed prices and standardized availability.

Purpose: reproducibility and direct comparison.

### LIFT-100O

Uses real markets, real suppliers and actual transactions.

Purpose: real-world procurement, value creation, substitution and economic performance.

Controlled and open-market results must be identified separately.

## 16. Human-as-compiler rule

The human builder is an execution interface, not an engineering or business collaborator.

If an instruction is incomplete, impossible or materially ambiguous, the operator reports the factual condition to the model and waits for a decision.

Normal workmanship is allowed. Design judgement and business strategy from the operator are not.

## 17. No hidden outsourcing of the physical objective

The payload may not simply be placed in an existing lift, crane or other pre-existing lifting machine and treated as the model's engineering result.

A person may not be paid to physically perform the scored lift.

Repurposing a general-purpose product as a component is allowed.

```text
component substitution = allowed
outsourcing the scored physical objective = not allowed
```

The model may, however, purchase legitimate fabrication or specialist services when those services produce components or capabilities for the model-designed system.

## 18. Iteration

Prototyping, testing, failure and redesign are allowed.

Financial consequences persist.

Money spent on failed approaches reduces the capital available until and unless some of that value is legitimately recovered.

This means bad physical reasoning can destroy capital, while good planning can preserve it.

## 19. Repeated evaluation

Official comparisons should use at least three independent runs with fresh conversations.

Report individual heights, median official height, best official height, economic ledger outcomes, build spend and failure rate.

## 20. Evidence

An official run should retain:

- full model conversation;
- initial prompt;
- complete capital ledger;
- receipts and transaction evidence;
- bill of materials;
- human-action log;
- build photographs;
- video of the scored mission;
- measurement data;
- failed-attempt records;
- token/compute accounting;
- evidence for qualifying economic inflows;
- final design diagram or annotated photograph.
