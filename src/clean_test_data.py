from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "simulated_test_data.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "cleaned_test_data.csv"

REQUIRED_COLUMNS = [
    "timestamp",
    "lot_id",
    "wafer_id",
    "die_x",
    "die_y",
    "tool_id",
    "test_type",
    "voltage_v",
    "current_ma",
    "resistance_ohm",
    "temperature_c",
    "result",
    "failure_type",
]


def validate_and_clean(df):
    print(f"Input records: {len(df):,}")

    # -----------------------------
    # Required-column validation
    # -----------------------------
    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # -----------------------------
    # Timestamp conversion
    # -----------------------------
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    invalid_timestamps = df["timestamp"].isna().sum()

    # -----------------------------
    # Duplicate detection
    # -----------------------------
    duplicate_count = df.duplicated().sum()

    if duplicate_count:
        df = df.drop_duplicates()

    # -----------------------------
    # Numeric validity checks
    # -----------------------------
    invalid_numeric = (
        (df["die_x"] < 0)
        | (df["die_y"] < 0)
        | (df["voltage_v"] < 0)
        | (df["current_ma"] < 0)
        | (df["resistance_ohm"] <= 0)
    )

    invalid_numeric_count = invalid_numeric.sum()

    # Remove physically invalid records.
    df = df.loc[~invalid_numeric].copy()

    # -----------------------------
    # Result validation
    # -----------------------------
    valid_results = {"PASS", "FAIL"}

    invalid_result_mask = ~df["result"].isin(valid_results)
    invalid_result_count = invalid_result_mask.sum()

    df = df.loc[~invalid_result_mask].copy()

    # -----------------------------
    # Failure-type consistency
    # -----------------------------
    failed_without_reason = (
        (df["result"] == "FAIL")
        & (
            df["failure_type"].isna()
            | (df["failure_type"].astype(str).str.strip() == "")
        )
    )

    failed_without_reason_count = failed_without_reason.sum()

    # -----------------------------
    # Missing-value report
    # -----------------------------
    required_for_all_records = [
        "timestamp",
        "lot_id",
        "wafer_id",
        "die_x",
        "die_y",
        "tool_id",
        "voltage_v",
        "current_ma",
        "resistance_ohm",
        "temperature_c",
        "result",
    ]

    missing_required = (
        df[required_for_all_records]
        .isna()
        .any(axis=1)
    )

    missing_required_count = missing_required.sum()

    df = df.loc[~missing_required].copy()

    print("\nData-quality report:")
    print(f"Invalid timestamps: {invalid_timestamps}")
    print(f"Duplicate records: {duplicate_count}")
    print(f"Invalid numeric records: {invalid_numeric_count}")
    print(f"Invalid result values: {invalid_result_count}")
    print(
        "FAIL records without failure type: "
        f"{failed_without_reason_count}"
    )
    print(
        "Records missing required values: "
        f"{missing_required_count}"
    )

    return df


def main():
    df = pd.read_csv(INPUT_FILE)

    cleaned_df = validate_and_clean(df)

    cleaned_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nClean records: {len(cleaned_df):,}")
    print(f"Saved cleaned dataset to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
