import pandas as pd
import statsmodels.formula.api as smf


def compute_regression(df, formula=""):
    """Fit a regression model
    """
    # Uses R-style formula as described here
    # https://www.statsmodels.org/dev/example_formulas.html
    data = df.copy()

    lm = smf.ols(
        formula=formula,
        data=data).fit()

    # output regression coefficients and p-values:
    params = pd.DataFrame(lm.params).reset_index().rename(
        columns={0: 'coefficient', 'index': 'factor'})
    pvals = pd.DataFrame(lm.pvalues[[1, 2]]).reset_index().rename(
        columns={0: 'p value', 'index': 'factor'})
    params = params.merge(pvals, how='left', on='factor').set_index('factor')

    # add confidence intervals
    conf = pd.DataFrame(data=lm.conf_int())
    conf.columns = ["conf_int_low", "conf_int_high"]
    return params.join(conf)
