# Datalab-pandas

This is very early stage library to simplify working with pandas for
common EBMDataLab operations


## Usage

Install geopandas using conda, then install the package as you usually would, e.g.

    conda install geopandas

    pip install ebmdatalab

### Convenience for caching/storing bigquery data as CSV

This will save the results of the SQL query as a CSV, and when it's
run again, as long as the SQL hasn't changed, load that CSV rather
than querying BigQuery again:


```python
from ebmdatalab import bq

sql = "SELECT * FROM ebmdatalab.hscic.bnf"
df = bq.cached_read(sql, csv_path='bnf_codes.csv')
df.head()

```


### Maps

Draw a CCG map, optionally with London separated out.

```python
from ebmdatalab import maps

df = pd.DataFrame(
    [
        ["99P", 0.3],
        ["13T", 1.2]
    ], columns=['pct', 'val'])
plt = maps.ccg_map(df, title="foo", column='val', separate_london=True)
plt.show()
```

### Deciles

Given a dataframe with a date column and a values column, compute
percentiles for each date and plot them in a line chart.

```python
from ebmdatalb import charts

# make a datafrom with a date column and a values column
df = pd.DataFrame(np.random.rand(1000, 1), columns=['val'])
months = pd.date_range('2018-01-01', periods=12, freq='M')
df['month'] = np.random.choice(months, len(df))

charts.deciles_chart(
        df,
        period_column='month',
        column='val',
        title="Random values",
        show_outer_percentiles=True)

```

### Logistic regression

```python
from ebmdatalab import stats
import numpy as np

# Three columns of random numbers
df = pd.DataFrame(np.random.rand(100, 3), columns=['a', 'b', 'c'])
formula = 'A ~ B + C'
stats.compute_regression(df, formula=formula)
```

outputs:

```
           coefficient   p value  conf_int_low  conf_int_high
factor
Intercept     0.470080       NaN      0.387447       0.552712
b            -0.089574  0.107805     -0.198860       0.019713
c             0.158883  0.006195      0.045469       0.272297

```


## Development

This project uses `flit` for bundling and publishing. Publish thus:

    flit publish

To install a package locally for development, install with a symlink so you can test changes without reinstalling the module:

    flit install --symlink
