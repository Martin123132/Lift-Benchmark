# Operator Protocol

## Purpose

The operator supplies hands, measurements and factual observations. The operator does not supply engineering judgement.

## Before the run

1. Start a fresh model conversation.
2. Record model name, version, provider and account/API configuration.
3. Provide only the official benchmark prompt.
4. Record available benchmark infrastructure.
5. Record the currency-conversion method if purchases are not in USD.
6. Start the purchase ledger at zero.

## Allowed operator actions

The operator may:

- answer factual questions about the test environment;
- measure requested dimensions, mass, voltage or other quantities;
- photograph components;
- buy specifically requested components;
- assemble exactly as instructed;
- perform ordinary competent workmanship;
- report that something does not fit, bind, slip, overheat, stall, break or otherwise fail;
- stop a test immediately for safety.

## Forbidden operator assistance

The operator must not:

- propose the lifting mechanism;
- suggest a motor, pulley, balloon or other approach unless asked for factual inventory information;
- optimize dimensions;
- select substitute parts without approval;
- improve gearing;
- add reinforcement because it “looks weak” without first reporting the concern;
- troubleshoot on the model's behalf;
- contribute energy to the scored lift;
- physically guide the payload during a scored attempt.

## Ambiguity rule

When an instruction requires design judgement:

1. Stop that step.
2. State exactly what is ambiguous.
3. Provide factual observations only.
4. Wait for the model to decide.

Acceptable:

> “The 4 mm shaft does not fit through the 3 mm bore. Do you want the bore enlarged, the shaft changed, or another action?”

Not acceptable:

> “I drilled it out because that was obviously what you meant.”

## Failed components

Purchased components remain charged even if they fail or are abandoned.

Refunds reduce spend only when a real refund is received.

## Scored operation

For LIFT-100, the operator may perform the agreed start/stop switch action only.

For LIFT-100A, the operator performs no control action after arming the test except an emergency safety stop.

Emergency intervention invalidates the scored mission and is logged.

## Logging

Each substantive intervention records:

- timestamp;
- model instruction;
- operator action;
- materials affected;
- whether the action altered the design;
- cost impact;
- result.

## Safety

Safety overrides scoring.

The operator may stop any action that creates an immediate safety, legal, fire, electrical, structural or aviation risk.

A safety stop is recorded as a failed attempt rather than repaired off-record.
