from ebmdatalab import charts
import pandas as pd
import numpy as np


def test_add_percentiles():
    df = pd.DataFrame(np.random.rand(1000, 1), columns=['val'])
    months = pd.date_range('2018-01-01', periods=12, freq='M')
    df['month'] = np.random.choice(months, len(df))
    df = charts.add_percentiles(df, period_column='month', column='val')
    # This is a statistically-likely test, so might fail!
    assert (df[df.percentile == 99].val > 0.75).all()


def test_deciles_chart():
    """Currently just tests it doesn't fail
    """
    df = pd.DataFrame(np.random.rand(1000, 1), columns=['val'])
    months = pd.date_range('2018-01-01', periods=12, freq='M')
    df['month'] = np.random.choice(months, len(df))

    charts.deciles_chart(
        df, period_column='month',
        column='val', title="thing", show_outer_percentiles=True)
