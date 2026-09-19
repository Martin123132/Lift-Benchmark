# Lift Benchmark

A physical-world AI benchmark for measuring how effectively a model can turn limited capital, reasoning and planning into a verified real-world result.

## Core challenge

> Raise a standardized 100 g payload as high as possible, then return it safely to the ground, within a fixed budget.

The primary score is deliberately simple:

```text
H = maximum verified vertical displacement of the 100 g payload
```

A height only becomes an official result after successful recovery.

## Benchmark classes

| Class | Budget | Human role | Purpose |
|---|---:|---|---|
| LIFT-100 | $100 | Assemble exactly as instructed; may switch system on/off | Mechanical design, planning, procurement, execution |
| LIFT-100A | $140 | Assemble exactly as instructed; no operating assistance | Adds model-controlled automation |
| LIFT-100C | Class budget | Fixed catalogue/prices | Reproducible controlled comparison |
| LIFT-100O | Class budget | Real-market procurement | Real-world economic and sourcing performance |

## Mission

```text
GROUND -> ASCENT -> VERIFIED MAXIMUM HEIGHT -> CONTROLLED RECOVERY -> GROUND
```

The benchmark does **not** prescribe the lifting method. Motors, gearing, pulleys, buoyancy, aerodynamic lift, counterweights, repurposed consumer products and hybrid systems are all potentially valid if they satisfy the same budget, safety, evidence and recovery rules.

## Economic reporting

Height remains the headline result. Every run also reports:

- gross physical spend;
- verified revenue generated during the run, if any;
- net external capital consumed;
- token usage and model/API cost where measurable;
- human build time;
- human interventions;
- number of attempts and failed purchases/prototypes.

Generated income may reduce reported net capital, but it does not increase the physical build-spend cap.

## Repository structure

- [Benchmark specification](docs/SPEC.md)
- [Operator protocol](docs/OPERATOR_PROTOCOL.md)
- [Initial model prompt](docs/MODEL_PROMPT.md)
- [Measurement and recovery protocol](docs/MEASUREMENT_AND_RECOVERY.md)
- [Run-log template](templates/RUN_LOG.md)
- [Machine-readable result schema](schemas/result.schema.json)

## Status

**Draft v0.1 — September 2026**

The benchmark is being developed as an auditable physical evaluation. Rules are expected to tighten after pilot runs expose edge cases.
