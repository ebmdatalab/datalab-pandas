from ebmdatalab import charts
import pandas as pd
import numpy as np


def test_add_percentiles():
    rows = [["2023-09-01", n * 5] for n in range(1001)]
    df = pd.DataFrame(rows, columns=["month", "val"])
    dfp = (
        charts.add_percentiles(df, period_column="month", column="val")
        .sort_values("percentile")
        .reset_index(drop=True)
    )
    percentiles = [
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 20, 30, 40, 50, 60, 70, 80, 90,
        91, 92, 93, 94, 95, 96, 97, 98, 99,
    ]
    expected_rows = [["2023-09-01", percentile, percentile * 50.0] for percentile in percentiles]
    expected = pd.DataFrame(expected_rows, columns=["month", "percentile", "val"])
    pd.testing.assert_frame_equal(dfp, expected)


def test_deciles_chart():
    """Currently just tests it doesn't fail
    """
    df = pd.DataFrame(np.random.rand(1000, 1), columns=["val"])
    months = pd.date_range("2018-01-01", periods=12, freq="M")
    df["month"] = np.random.choice(months, len(df))

    charts.deciles_chart(
        df,
        period_column="month",
        column="val",
        title="thing",
        show_outer_percentiles=True,
    )
