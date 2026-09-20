# Lift Benchmark

A physical-world AI benchmark for measuring how effectively a model can turn limited starting capital, reasoning and planning into a verified real-world result.

## Core challenge

> Start with a fixed amount of capital. Raise a standardized 100 g payload as high as possible, then return it safely to the ground.

The primary score is deliberately simple:

```text
H = maximum verified vertical displacement of the 100 g payload
```

A height only becomes an official result after successful recovery.

## The key economic rule

**$100 is seed capital, not a spending cap.**

For standard LIFT-100, the model begins with:

```text
S = $100 USD
```

The model may spend, trade, sell, build, provide services, make products, invest benchmark funds, or otherwise conduct lawful economic activity.

Any verified money the model legitimately generates becomes part of its available benchmark capital and may be reinvested into the lift.

There is **no upper cap on final project spend**.

If a model legitimately turns $100 into $1,000,000, then it may spend up to the capital it has actually generated and controls on the lifting system.

The benchmark therefore tests both:

1. how effectively the model engineers the physical task; and
2. how effectively it expands or preserves the capital available to solve it.

## Benchmark classes

| Class | Starting capital | Human role | Purpose |
|---|---:|---|---|
| LIFT-100 | $100 | Assemble exactly as instructed; may switch system on/off | Engineering + economic agency |
| LIFT-100A | $140 | Assemble exactly as instructed; no operating assistance | Engineering + economic agency + autonomous control |
| LIFT-100C | Fixed seed | Fixed catalogue/prices | Reproducible controlled comparison |
| LIFT-100O | Fixed seed | Real-market procurement | Real-world sourcing and economic performance |

## Mission

```text
GROUND -> ASCENT -> VERIFIED MAXIMUM HEIGHT -> CONTROLLED RECOVERY -> GROUND
```

The benchmark does **not** prescribe the lifting method. Motors, gearing, pulleys, buoyancy, aerodynamic lift, counterweights, repurposed consumer products and hybrid systems are all potentially valid if they satisfy the same safety, evidence and recovery rules.

## Capital accounting

The benchmark maintains a real capital ledger.

```text
B_0 = starting capital

B_(i+1) = B_i + qualifying cash inflows - cash outflows
```

A purchase is allowed only if the model has sufficient cleared benchmark capital at that point.

Revenue, realized gains, refunds and proceeds from legitimate sales may increase the balance.

Failed prototypes still consume capital.

Borrowed money, owner top-ups, gifts and artificial transfers do not increase the spendable balance in the core benchmark.

## Reporting

Height remains the headline result. Every run also reports:

- starting capital;
- total qualifying external revenue;
- realized economic gains/losses;
- total physical build spend;
- peak spendable capital;
- final capital balance;
- token usage and model/API cost where measurable;
- human build time;
- human interventions;
- number of attempts and failed purchases/prototypes.

## Repository structure

- [Benchmark specification](docs/SPEC.md)
- [Capital accounting rules](docs/CAPITAL_ACCOUNTING.md)
- [Operator protocol](docs/OPERATOR_PROTOCOL.md)
- [Initial model prompt](docs/MODEL_PROMPT.md)
- [Measurement and recovery protocol](docs/MEASUREMENT_AND_RECOVERY.md)
- [Run-log template](templates/RUN_LOG.md)
- [Machine-readable result schema](schemas/result.schema.json)

## Status

**Draft v0.2 — September 2026**

The benchmark is being developed as an auditable physical evaluation. Rules are expected to tighten after pilot runs expose edge cases.
