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

# # Reading from Google Sheets
#
# There are complicated read/write possibilities (e.g. [this](https://socraticowl.com/post/integrate-google-sheets-and-jupyter-notebooks/) and [this](https://github.com/robin900/gspread-dataframe)), but on the assumption we are happy to share contents of sheets publicly, the easiest thing is to publish a worksheet in CSV format using [Google Sheets "publish" functionality](https://support.google.com/docs/answer/183965).
#

# +
import pandas as pd

# This URL obtained via the Google Sheets's `publish to the web` menu (File > Publish to the web; 
# select the worksheet from the first dropdown and "comma-separated values" from the second; 
# copy the link)
google_sheet = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTefoHueV7W523NR2uc5ckS9zJFeuWFr2v84WkzThbobQq5KPKIqlued_UqRCy31YGhF4P3XEyJWlI8/pub?gid=252563648&single=true&output=csv"

pd.read_csv(google_sheet).head()
