# Semiconductor Manufacturing Data Automation & Yield Analysis

A Python portfolio project for generating simulated wafer electrical-test data, cleaning records, and producing yield and failure summaries. The direction is manufacturing data automation and analysis to support yield-enhancement investigations, with test/product engineering as adjacent applications.

**All data are simulated.** No employer, customer, proprietary fab, or real production data are used. This project does not demonstrate a measured improvement in manufacturing yield or production-ready automation.

## Implemented capabilities

- `src/generate_test_data.py`: generates 640 die-level records across two lots, eight wafers, and three testers, using NumPy seed 42. Each wafer is assigned to one tester. The simulation includes a current offset for TESTER_C and a deliberately weak LOT_002 / WAFER_03.
- `src/clean_test_data.py`: checks required columns, parses timestamps, removes exact duplicate rows, rejects selected invalid numeric values and invalid PASS/FAIL labels, and removes records missing checked required values. It prints data-quality counts and saves a cleaned CSV.
- `src/yield_analysis.py`: calculates overall pass yield, yield by lot/wafer and by tester, counts recorded failure types, and flags wafers below a fixed 90% yield threshold. It prints summaries and writes four CSV files.

The generator currently produces structurally clean data; it does not inject missing values, duplicates, or inconsistent formatting. The cleaner reports FAIL records without a failure reason but does not repair or remove them solely for that reason. Numeric columns are expected to contain numeric data; general text-to-number coercion is not implemented.

## Run locally

Run from the repository root with Python, NumPy, and pandas installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/generate_test_data.py
python src/clean_test_data.py
python src/yield_analysis.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The scripts use paths relative to their own project location. Run them in the order shown; each overwrites its corresponding generated files. There is no single-command pipeline or scheduler yet.

The existing `requirements.txt` also lists matplotlib, scikit-learn, and Jupyter from the earlier project plan; the implemented scripts only import NumPy and pandas beyond the standard library. Dependencies are not version-pinned. The current workflow was verified with Python 3.14.

## Current files and outputs

```text
semiconductor-lab-data-automation/
├── src/
│   ├── generate_test_data.py
│   ├── clean_test_data.py
│   └── yield_analysis.py
├── data/
│   ├── simulated_test_data.csv
│   └── cleaned_test_data.csv
├── output/
│   ├── wafer_yield_summary.csv
│   ├── tool_yield_summary.csv
│   ├── failure_summary.csv
│   └── abnormal_wafers.csv
├── docs/
│   ├── project_scope.md
│   └── data_dictionary.md
├── requirements.txt
├── .gitignore
└── README.md
```

The small simulated CSVs are included as reproducible examples. Empty placeholder directories from the initial plan are not implemented features.

## Verified example results

Running all three scripts reproduces the existing CSV contents:

| Metric | Simulated result |
|---|---:|
| Generated / retained records | 640 / 640 |
| PASS / FAIL records | 614 / 26 |
| Overall pass yield | 95.94% |
| LOT_002 / WAFER_03 yield | 70.00% |
| Wafers below 90% yield | 1 |
| Recorded resistance_low failures | 15 |
| Recorded current_high failures | 11 |

Yield is PASS records divided by all records in the analyzed group, multiplied by 100. Wafers are identified by `(lot_id, wafer_id)` because wafer IDs repeat across lots. Each die receives only the first matching failure reason in the generator's ordered checks, not every violated limit. Pass/fail classification occurs before measurements are rounded for CSV export.

## Interpretation and limitations

The low-yield wafer is deliberately built into the simulation. Tester summaries compare different wafers, not repeated measurements of the same devices. They cannot establish tester correlation, measurement bias, or a causal tool effect; the weak wafer is assigned to TESTER_A. No root-cause diagnosis or verified yield enhancement is claimed.

The fixed 90% flag is a simple screening rule, not statistical process control (SPC). There are no control charts, control limits, capability indices, or statistical excursion tests. The rectangular die grid and electrical limits are educational simplifications, not a validated device or fab model.

## Planned — not implemented

- **Tester correlation:** design matched-device measurements across testers, then assess agreement and offsets.
- **Visualization:** yield comparisons, failure distributions, and wafer maps.
- **SPC:** define suitable sampling groups and implement statistical monitoring with documented assumptions.

Chamber/cleanroom sensor processing, predictive modeling, dashboards, automated narrative reports, cloud integration, and scheduled execution are not implemented. They appeared in the initial broader lab concept and are not current capabilities or committed deliverables.

See [project scope](docs/project_scope.md) and [data dictionary](docs/data_dictionary.md) for the current scope and actual CSV schema.
