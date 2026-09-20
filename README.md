# Lift Benchmark

**Start with $100. Lift 100 g as high as possible. Bring it safely back.**

The $100 is **starting capital, not a spending cap**. An AI may buy parts immediately or use lawful, documented economic activity to earn more first. Qualifying cleared earnings are fully reinvestable. A million-dollar build is within scope if the model genuinely generates the capital to fund it.

The human supplies hands and factual observations, not engineering or business strategy and not lifting energy. In the standard class they may switch the system on/off. The autonomous class starts with $140 and operates through the computer interface.

**Primary score:** highest verified vertical height maintained for five continuous seconds, conditional on intact, controlled recovery. Record momentary peak height separately.

## Start a pilot

Read [QUICKSTART.md](QUICKSTART.md). With Python 3.11 or newer:

```sh
python -m pip install -r requirements.txt
python scripts/lift.py init local-runs/pilot-001 --run-id pilot-001
```

This creates incomplete input and result templates. It does not run a model, spend money or operate hardware. Complete and preregister the inputs before starting.

```sh
python scripts/lift.py seal local-runs/pilot-001
python scripts/lift.py validate local-runs/pilot-001
python -m unittest discover -s tests -v
```

Validation checks record structure, transaction arithmetic, declared mission conditions, evidence-file presence and preregistration hashes. **It does not authenticate a payment, inspect a video or certify a physical result.** Synthetic test fixtures are rejected by default and are never results.

## Two independent settings

| Setting | Options |
|---|---|
| Operation | `standard`: $100 seed; `autonomous`: $140 seed |
| Procurement | `open-market`: actual transactions; `controlled`: declared catalogue and commercial opportunities |

Compare runs with matching conditions. Long-running capital growth remains allowed; publish elapsed time and declared checkpoints rather than adding a spending ceiling.

## Rules and records

- [Core specification, v0.2](docs/SPEC.md) and [capital principles](docs/CAPITAL_ACCOUNTING.md)
- [Pilot protocol, v0.3](docs/PILOT_PROTOCOL.md): recording conventions, held-height scoring and rule decisions
- [Model prompt](docs/MODEL_PROMPT.md), [operator protocol](docs/OPERATOR_PROTOCOL.md) and [measurement/recovery](docs/MEASUREMENT_AND_RECOVERY.md)
- [Run log](templates/RUN_LOG.md) and [schemas](schemas)
- [Submission and review guide](CONTRIBUTING.md), [results status](results/README.md) and [changelog](CHANGELOG.md)

## Status

**v0.3-pilot — September 2026.** This release supplies pilot tooling and synthetic software tests. No physical result is claimed by the kit. Core rules not explicitly clarified by the pilot protocol remain unchanged, including the existing equipment/outsourcing restriction pending the creator's decision.

Created by **Martin Ollett**. Citation metadata is in [CITATION.cff](CITATION.cff). Licence selection remains an owner decision; this release does not add a licence.
