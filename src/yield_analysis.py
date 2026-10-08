from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "cleaned_test_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_yield(results):
    """
    Calculate pass yield as a percentage.
    """
    return (results == "PASS").mean() * 100

def analyze_wafer_yield(df):
    wafer_yield = (
        df.groupby(["lot_id", "wafer_id"])["result"]
        .apply(calculate_yield)
        .reset_index(name="yield_percent")
    )

    wafer_yield["yield_percent"] = wafer_yield[
        "yield_percent"
    ].round(2)

    return wafer_yield

def analyze_tool_yield(df):
    tool_yield = (
        df.groupby("tool_id")["result"]
        .apply(calculate_yield)
        .reset_index(name="yield_percent")
    )

    tool_yield["yield_percent"] = tool_yield[
        "yield_percent"
    ].round(2)

    return tool_yield

def analyze_failures(df):
    failures = (
        df.loc[df["result"] == "FAIL"]
        .groupby("failure_type")
        .size()
        .reset_index(name="failure_count")
        .sort_values(
            "failure_count",
            ascending=False
        )
    )

    return failures

def detect_abnormal_wafers(wafer_yield):
    abnormal = wafer_yield.loc[
        wafer_yield["yield_percent"] < 90.0
    ].copy()

    return abnormal

def main():
    df = pd.read_csv(INPUT_FILE)

    overall_yield = calculate_yield(df["result"])

    wafer_yield = analyze_wafer_yield(df)
    tool_yield = analyze_tool_yield(df)
    failures = analyze_failures(df)
    abnormal_wafers = detect_abnormal_wafers(wafer_yield)

    wafer_yield.to_csv(
        OUTPUT_DIR / "wafer_yield_summary.csv",
        index=False
    )

    tool_yield.to_csv(
        OUTPUT_DIR / "tool_yield_summary.csv",
        index=False
    )

    failures.to_csv(
        OUTPUT_DIR / "failure_summary.csv",
        index=False
    )

    abnormal_wafers.to_csv(
        OUTPUT_DIR / "abnormal_wafers.csv",
        index=False
    )

    print(f"Overall yield: {overall_yield:.2f}%")

    print("\nWafer yield:")
    print(wafer_yield.to_string(index=False))

    print("\nTool yield:")
    print(tool_yield.to_string(index=False))

    print("\nFailure summary:")
    print(failures.to_string(index=False))

    print("\nAbnormal wafers (<90% yield):")

    if abnormal_wafers.empty:
        print("None")
    else:
        print(abnormal_wafers.to_string(index=False))


if __name__ == "__main__":
    main()
