# Datalab-pandas

This is very early stage library to simplify working with pandas for
common EBMDataLab operations


## Usage

Install the package as you usually would, e.g.

    pip install ebmdatalab

### Convenience for caching/storing bigquery data as CSV

This will save the results of the SQL query as a CSV, and when it's
run again, as long as the SQL hasn't changed, load that CSV rather
than querying BigQuery again:


```python
from ebmdatalab import bq

sql = "SELECT * FROM ebmdatalab.hscic.bnf"
df = bq.cached_read(sql, csv_path='bnf_codes.csv')  # add `use_cache=False` to override
df.head()

```



### Other functions

See the `examples/` directory for:

* Logistic regression
* CCG maps
* Deciles charts


## Development

This project uses `flit` for bundling and publishing. Publish thus:

    flit publish

To install a package locally for development, install with a symlink so you can test changes without reinstalling the module:

    flit install --symlink
