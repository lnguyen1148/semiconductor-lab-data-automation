# Data Dictionary — Simulated Wafer Electrical Tests

All values are synthetic. Only wafer electrical-test data are implemented; there are no chamber or cleanroom datasets.

Both `data/simulated_test_data.csv` and `data/cleaned_test_data.csv` use these columns:

| Field | Meaning / generated values |
|---|---|
| timestamp | Simulated test time, starting 2026-09-15 08:00:00 in 20-second increments; no timezone |
| lot_id | LOT_001 or LOT_002 |
| wafer_id | WAFER_01 through WAFER_04 within each lot; use with lot_id |
| die_x | Integer 1–10 on a simplified rectangular grid |
| die_y | Integer 1–8 on a simplified rectangular grid |
| tool_id | TESTER_A, TESTER_B, or TESTER_C; one tester per wafer |
| test_type | electrical_parametric |
| voltage_v | Simulated voltage, volts; exported to four decimal places |
| current_ma | Simulated current, milliamps; exported to four decimal places |
| resistance_ohm | Simulated resistance, ohms; exported to three decimal places |
| temperature_c | Simulated temperature, Celsius; exported to two decimal places |
| result | PASS or FAIL |
| failure_type | Empty for PASS; first matching failure reason for FAIL |

## Simulated classification rules

The generator checks these rules in order on unrounded measurements:

1. voltage_v < 1.12 → voltage_low
2. voltage_v > 1.28 → voltage_high
3. current_ma > 0.98 → current_high
4. resistance_ohm < 94.0 → resistance_low
5. Otherwise PASS.

Temperature does not determine pass/fail. These limits are educational assumptions, not real product specifications. Only the first matching reason is recorded.

TESTER_C receives a +0.025 mA current offset. LOT_002 / WAFER_03 receives simulated increased current and reduced resistance. These are deliberately injected effects, not findings from real equipment.

## Summary CSVs

| File under output/ | Columns | Meaning |
|---|---|---|
| wafer_yield_summary.csv | lot_id, wafer_id, yield_percent | Pass percentage for each lot/wafer pair |
| tool_yield_summary.csv | tool_id, yield_percent | Pass percentage across each tester's assigned wafers |
| failure_summary.csv | failure_type, failure_count | Counts of recorded reasons among FAIL records |
| abnormal_wafers.csv | lot_id, wafer_id, yield_percent | Wafer summary rows below 90% yield |

Percentages are rounded to two decimal places. Overall yield and cleaning counts are printed to the console, not exported as separate reports. A FAIL record without a reason is reported by the cleaner; pandas grouping omits missing failure_type values from the failure summary.
