from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# Reproducible random data
RNG = np.random.default_rng(seed=42)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "simulated_test_data.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_wafer_test_data():
    """
    Generate simulated semiconductor wafer electrical test data.

    Each wafer is assigned to one tester for its production test run.
    All data is synthetic and intended only for portfolio,
    learning, and yield-analysis purposes.
    """

    records = []

    lots = ["LOT_001", "LOT_002"]
    wafers_per_lot = 4

    tools = [
        "TESTER_A",
        "TESTER_B",
        "TESTER_C",
    ]

    start_time = datetime(2026, 9, 15, 8, 0, 0)

    # Simple rectangular die grid for MVP.
    die_x_values = range(1, 11)
    die_y_values = range(1, 9)

    record_number = 0
    wafer_run_number = 0

    for lot_id in lots:
        for wafer_number in range(1, wafers_per_lot + 1):

            wafer_id = f"WAFER_{wafer_number:02d}"

            # -----------------------------------
            # Assign one tester to the whole wafer
            # -----------------------------------
            tool_id = tools[
                wafer_run_number % len(tools)
            ]

            wafer_run_number += 1

            for die_x in die_x_values:
                for die_y in die_y_values:

                    # -----------------------------
                    # Normal electrical behavior
                    # -----------------------------
                    voltage_v = RNG.normal(
                        1.20,
                        0.025
                    )

                    current_ma = RNG.normal(
                        0.85,
                        0.045
                    )

                    resistance_ohm = RNG.normal(
                        102.0,
                        3.0
                    )

                    temperature_c = RNG.normal(
                        25.0,
                        0.8
                    )

                    # -----------------------------
                    # Controlled tester effect
                    # -----------------------------

                    # TESTER_C has a small systematic
                    # current-measurement bias.
                    if tool_id == "TESTER_C":
                        current_ma += 0.025

                    # -----------------------------
                    # Controlled wafer excursion
                    # -----------------------------

                    # LOT_002 / WAFER_03 is intentionally
                    # weaker because of simulated process variation.
                    weak_wafer = (
                        lot_id == "LOT_002"
                        and wafer_id == "WAFER_03"
                    )

                    if weak_wafer:
                        current_ma += RNG.normal(
                            0.07,
                            0.02
                        )

                        resistance_ohm -= RNG.normal(
                            5.0,
                            1.5
                        )

                    # -----------------------------
                    # Simulated electrical test limits
                    # -----------------------------
                    failure_type = ""

                    if voltage_v < 1.12:
                        result = "FAIL"
                        failure_type = "voltage_low"

                    elif voltage_v > 1.28:
                        result = "FAIL"
                        failure_type = "voltage_high"

                    elif current_ma > 0.98:
                        result = "FAIL"
                        failure_type = "current_high"

                    elif resistance_ohm < 94.0:
                        result = "FAIL"
                        failure_type = "resistance_low"

                    else:
                        result = "PASS"

                    timestamp = start_time + timedelta(
                        seconds=record_number * 20
                    )

                    records.append(
                        {
                            "timestamp": timestamp,
                            "lot_id": lot_id,
                            "wafer_id": wafer_id,
                            "die_x": die_x,
                            "die_y": die_y,
                            "tool_id": tool_id,
                            "test_type": "electrical_parametric",
                            "voltage_v": round(
                                voltage_v,
                                4
                            ),
                            "current_ma": round(
                                current_ma,
                                4
                            ),
                            "resistance_ohm": round(
                                resistance_ohm,
                                3
                            ),
                            "temperature_c": round(
                                temperature_c,
                                2
                            ),
                            "result": result,
                            "failure_type": failure_type,
                        }
                    )

                    record_number += 1

    return pd.DataFrame(records)


def main():
    df = generate_wafer_test_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Generated {len(df):,} simulated test records."
    )

    print(
        f"Saved dataset to: {OUTPUT_FILE}"
    )

    print("\nWafer-to-tester assignments:")

    assignments = (
        df[
            [
                "lot_id",
                "wafer_id",
                "tool_id",
            ]
        ]
        .drop_duplicates()
    )

    print(
        assignments.to_string(index=False)
    )

    print("\nResult counts:")
    print(
        df["result"].value_counts()
    )

    print("\nOverall simulated yield:")

    yield_percent = (
        (df["result"] == "PASS").mean()
        * 100
    )

    print(
        f"{yield_percent:.2f}%"
    )


if __name__ == "__main__":
    main()
