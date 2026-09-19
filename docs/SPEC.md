# LIFT-100 Benchmark Specification

Version: **0.1-draft**

## 1. Objective

The model must cause a standardized 100 g payload to travel from its initial ground datum to the greatest possible verified vertical displacement and then return safely to ground level.

Primary score:

```text
H = h_max - h_0
```

where `h_0` is the initial payload reference height and `h_max` is the greatest verified vertical position reached during a successfully completed mission.

If recovery fails, the attempted height is retained for diagnostics but does not become an official score.

## 2. Standard payload

Target mass:

```text
100.0 g +/- 0.5 g
```

The payload must be supplied identically to each competitor, use a standard attachment interface, remain intact, and use the same measurement reference point throughout the attempt.

## 3. Standard class — LIFT-100

Maximum physical-project spend:

```text
$100 USD
```

The model may choose any lawful and safe physical approach.

A human operator may purchase exactly what the model requests, perform ordinary fabrication and assembly, take requested measurements, report physical observations, and switch the completed device on/off when instructed.

The human may not supply lifting energy, redesign the system, silently correct engineering errors, choose substitute parts without approval, or guide the payload during scored operation.

## 4. Autonomous class — LIFT-100A

Maximum physical-project spend:

```text
$140 USD
```

The additional allowance exists for control hardware such as microcontrollers, relays, sensors, interfaces and communications equipment.

After assembly and test setup, the model must itself issue the control commands that initiate, manage and terminate the scored mission.

## 5. Successful mission

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

## 6. Lifting method

The benchmark is physics-agnostic.

Potentially valid methods include motors, gearing, pulleys, winches, counterweights, springs, buoyancy, aerodynamic lift, repurposed consumer products and hybrid systems.

A novel or unexpected mechanism is not an exploit merely because the benchmark designer did not anticipate it.

**Patch trivial completion conditions, not clever engineering.**

## 7. Recovery

The payload must return safely and intentionally.

Recovery may not rely on uncontrolled falling or uncontrolled release.

Buoyant or airborne designs therefore need a real recovery method: tether retrieval, controlled venting, reversible buoyancy, powered descent, parachute control, or another explicit mechanism.

All testing must remain inside the legal and safety envelope of the test location.

## 8. Budget accounting

All lift-essential equipment is charged.

```text
C_physical =
  parts
+ materials
+ fabrication
+ shipping
+ taxes
+ paid services
```

Failed purchases and failed prototypes remain charged.

Existing equipment is not automatically free. It must be either declared benchmark infrastructure available equally to every model, or charged at an agreed purchase/rental value.

Typical free infrastructure may include ordinary hand tools, workbench, PPE, measurement equipment, test computer, internet access and normal domestic electricity.

Anything incorporated into the lifting system is normally chargeable.

## 9. Economic-value track

The model may attempt legitimate economic activity during the run.

```text
C_net = C_physical - R
```

where `R` is verified qualifying revenue.

Revenue does **not** raise the physical-spend cap.

Qualifying revenue must be lawful, arm's-length, paid by an unrelated third party and documented.

Gifts, donations, owner transfers, artificial circular transactions, loans and gambling proceeds do not qualify.

## 10. Compute reporting

Compute is reported separately from the physical budget.

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

Optional all-in economics:

```text
C_all_in = C_physical + C_compute + C_labour - R
```

This does not replace the primary height score.

## 11. Controlled and open-market variants

### LIFT-100C

Fixed catalogue, prices and availability.

Purpose: reproducibility and direct engineering comparison.

### LIFT-100O

Real-market procurement and actual transaction prices.

Purpose: sourcing, substitution and real-world economic performance.

Controlled and open-market results must be identified separately.

## 12. Human-as-compiler rule

The human builder is an execution interface, not an engineering collaborator.

If an instruction is incomplete, impossible or materially ambiguous, the operator reports the physical condition to the model and waits for a decision.

Normal workmanship is allowed. Design judgement is not.

## 13. No hidden outsourcing

The payload may not simply be placed in an existing lift, crane or other pre-existing lifting machine.

A person may not be paid to perform the physical lift.

Repurposing a general-purpose product as a component is allowed.

```text
component substitution = allowed
outsourcing the objective = not allowed
```

## 14. Iteration

Prototyping, testing, failure and redesign are allowed.

Financial consequences persist. Money spent on failed approaches remains spent.

## 15. Repeated evaluation

Official comparisons should use at least three independent runs with fresh conversations.

Report individual heights, median official height, best official height, spend per run and failure rate.

## 16. Evidence

An official run should retain the full model conversation, initial prompt, purchase ledger, receipts, bill of materials, human-action log, build photographs, video of the scored mission, measurement data, failed-attempt records, token/compute accounting, revenue evidence where applicable, and a final design diagram or annotated photograph.
