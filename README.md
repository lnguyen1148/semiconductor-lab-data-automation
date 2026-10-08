# Semiconductor Manufacturing Data Automation & Yield Analysis

I’m building this project to learn about semiconductor wafer-test data, yield analysis, and practical Python.

The current code generates simulated electrical-test data, cleans selected data-quality issues, and calculates yield by wafer and tester. It also
summarizes failure reasons and flags wafers with yield below 90%.

All data are simulated for learning. The results do not represent a real manufacturing process.

## What the code does

The project currently has three scripts:

- `src/generate_test_data.py` creates 640 simulated die-test records across two lots and eight wafers. Each wafer is assigned to one
  of three testers.
- `src/clean_test_data.py` checks the required columns, converts timestamps, removes duplicate rows and selected invalid records,
  and saves a cleaned CSV. It prints a summary of the checks.
- `src/yield_analysis.py` calculates overall yield and yield by wafer and tester. It counts recorded failure reasons and saves CSV
  summaries, including wafers below 90% yield.

The generated data has no missing required values or duplicate rows, so it does not exercise every cleaning rule. The failure reason is intentionally empty for passing records.

The cleaner reports FAIL records without a failure reason but keeps them unless another rule removes them. It also expects numeric columns
to contain numbers; it does not convert invalid text into numeric values.

## Run locally

From the project folder, create and activate a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you already created `.venv`, you only need to activate it.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the scripts in this order:

```bash
python src/generate_test_data.py
python src/clean_test_data.py
python src/yield_analysis.py
```

The generator creates the simulated data, the cleaner reads that data, and the analysis script reads the cleaned file. Running them again
overwrites their existing CSV outputs.

These commands use macOS/Linux environment activation. On Windows, use `.venv\Scripts\activate.bat` in Command Prompt.

The current scripts use NumPy and pandas. The requirements file also includes matplotlib, scikit-learn, and Jupyter from the earlier plan,
but the scripts do not use them yet.

## Project files

The `data/` folder contains the simulated input and cleaned data.
The `output/` folder contains the yield and failure summaries.

The CSV files are included so you can inspect the results without running the scripts. You can regenerate them by running the three
scripts in order.

## Example results

The included simulated dataset has 640 tested dies: 614 passed and 26 failed, giving an overall yield of 95.94%.

LOT_002 / WAFER_03 has 56 passing dies out of 80, giving a yield of 70%. It accounts for 24 of the dataset’s 26 failures. This wafer was
deliberately given different measurement values in the generator to practice identifying a low-yield wafer.

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

## What the results can tell us

The summaries show where failures appear in the simulated data. They do not explain the cause of a failure.

Each wafer is assigned to one tester. A tester with lower yield may have tested weaker wafers, so comparing tester yields alone cannot
show whether a tester is measuring incorrectly.

The 90% wafer-yield threshold is a rule chosen for this exercise. It is not an industry standard or a statistical process control
(SPC) limit.

The die grid, measurement values, and test limits are simplified examples for learning.

## Next steps

Before adding features, I want to review the existing code and test the cleaner with deliberately messy records.

Ideas to explore after that:

- Plot wafer yield and failure counts.
- Simulate measurements of the same dies on different testers to compare their results.
- Learn how statistical process control (SPC) works and decide how to apply it to a suitable simulated dataset.

These features are not implemented yet.

More details are in the [project scope](docs/project_scope.md) and [data dictionary](docs/data_dictionary.md).