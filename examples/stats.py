# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernelspec:
#     display_name: Python (jupyter virtualenv)
#     language: python
#     name: jupyter
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.5
# ---

# ## Logistic regression
#
#

# +
import numpy as np
import pandas as pd

from ebmdatalab import stats

# Three columns of random numbers
df = pd.DataFrame(np.random.rand(100, 3), columns=['A', 'B', 'C'])
formula = 'A ~ B + C'
stats.compute_regression(df, formula=formula)

