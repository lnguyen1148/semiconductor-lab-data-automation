# Project Scope

## Direction

Semiconductor Manufacturing Data Automation & Yield Analysis: an educational Python workflow for simulated wafer electrical-test data. Manufacturing automation and yield-enhancement investigation are the focus; test/product engineering is adjacent.

## Current implementation

1. Generate 640 simulated die records across two lots, eight wafers, and three testers.
2. Validate required columns, clean selected invalid records, and print data-quality counts.
3. Calculate overall, wafer, and tester pass yield; summarize recorded failure reasons.
4. Export four summary CSVs, including wafers below a fixed 90% yield threshold.

The implemented workflow is three manually invoked scripts. See the [README](../README.md) for commands, verified results, and limitations.

## Planned, not implemented

- Tester correlation using matched-device measurements across testers.
- Yield, failure, and wafer-map visualizations.
- Statistical process control (SPC) with documented assumptions.

## Boundaries

All data are simulated for learning and portfolio use. The project does not use real production data, model exact semiconductor physics, diagnose root causes, or establish actual manufacturing yield improvements. Current tester summaries are not a correlation study, and the fixed wafer threshold is not SPC.

The original broader lab concept included chamber and cleanroom sensor data, machine learning, cloud storage, and scheduled execution. None is implemented or a committed deliverable in the current scope.
