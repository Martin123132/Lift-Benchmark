# Capital Accounting Rules

Version: **0.2-draft**

## 1. Seed capital, not budget cap

The defining economic rule of LIFT-100 is:

> The model starts with $100. It is not limited to spending $100 forever.

The model is allowed to use its starting capital to create additional capital.

Once qualifying proceeds are real, cleared and documented, they become part of the benchmark account and can be spent on the physical challenge.

There is no preset maximum balance and no preset maximum final build cost.

## 2. Account model

For standard LIFT-100:

```text
B_0 = $100
```

For LIFT-100A:

```text
B_0 = $140
```

Every transaction updates the account:

```text
B_(i+1) = B_i + qualifying inflows - outflows
```

The account must never go negative in core LIFT-100.

The model may commit only money that has actually cleared into the benchmark account.

## 3. Example

A model starts with $100.

It spends $40 producing something and sells it for $250.

Its balance is then:

```text
$100 - $40 + $250 = $310
```

It may now spend up to $310.

If it uses that money to create a service that earns $10,000, the new cleared proceeds may also be reinvested.

If repeated successful activity eventually produces $1,000,000 of available benchmark capital, a $1,000,000-scale engineering solution is within scope.

That is intentional.

## 4. Why this exists

The benchmark is designed to test more than mechanical design.

It can reveal whether a model can:

- avoid wasting scarce capital;
- identify cheaper substitutes;
- create products or services;
- generate income;
- compound economic gains;
- decide when earning more capital is preferable to engineering around scarcity;
- convert digital reasoning into physical and economic consequences.

## 5. Qualifying inflows

Examples may include:

- sales revenue;
- service revenue;
- licensing revenue;
- resale proceeds;
- commissions;
- realized gains on benchmark-owned assets where allowed;
- refunds;
- other documented arm's-length proceeds.

Revenue is not counted merely because an invoice exists. It must be received and available.

## 6. Excluded inflows

Core LIFT-100 excludes:

- owner top-ups;
- gifts;
- donations;
- fake purchases by the evaluator;
- circular payments;
- undisclosed subsidies;
- loans and credit advances.

These exclusions keep the starting-capital claim meaningful.

## 7. Asset ownership

Items purchased with benchmark capital belong to the benchmark account for the duration of the run.

They may be:

- used in the lift;
- transformed into another asset;
- sold;
- scrapped;
- returned for a genuine refund.

Sale proceeds re-enter the account when received.

## 8. Failed attempts

Failure has an economic cost.

If the model spends $70 on a failed prototype and recovers only $10 by selling the remains, the account bears the $60 net loss.

This is part of the evaluation.

## 9. Required ledger fields

Every transaction should record:

- timestamp;
- type;
- description;
- counterparty;
- gross inflow;
- gross outflow;
- fees;
- evidence reference;
- cleared/not-cleared state;
- post-transaction cash balance;
- associated asset where relevant.

## 10. Reported economic quantities

At minimum:

```text
S             = starting capital
R_external    = total qualifying external revenue
C_economic    = costs used to generate capital
C_physical    = physical lifting-system spend
B_peak        = highest cleared cash balance
B_final       = final cleared cash balance
M_capital     = B_peak / S
```

These are reported dimensions, not replacements for the primary physical score.

The primary benchmark result remains verified recovered height.
