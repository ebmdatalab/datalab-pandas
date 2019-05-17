from ebmdatalab import stats
import pandas as pd
import random


def test_compute_regression():
    # build dataframe with predictable regression characteristics
    matrix = []
    multiple = 3
    for a in range(1, 50):
        # we want b + c to be a multiple of a
        target_val = a * multiple
        b = target_val / random.randint(1, target_val)
        c = target_val - b
        matrix.append([a, b, c])
    df = pd.DataFrame(matrix, columns=['A', 'B', 'C'])

    # test against it
    formula = ('A ~ B + C')
    df2 = stats.compute_regression(df, formula=formula).round(5)

    col_b_data = df2.loc['B']
    expected_ratio = round(1/multiple, 5)
    assert col_b_data['p value'] == 0
    assert col_b_data['coefficient'] == expected_ratio
    assert col_b_data['conf_int_low'] == expected_ratio
    assert col_b_data['conf_int_high'] == expected_ratio
    assert col_b_data['p value'] == 0

    intercept_data = df2.loc['Intercept']
    assert intercept_data['coefficient'] == 0
