# Datalab-pandas

This is very early stage library to simplify working with pandas for
common EBMDataLab operations


## Usage

Install the package as you usually would, e.g.

    pip install ebmdatalab

### Convenience for caching/storing bigquery data as CSV

This will save the results of the SQL query as a CSV, and when it's
run again, as long as the SQL hasn't changed, load that CSV rather
than querying BigQuery again. Use a `.zip`, `.gz`, `.bz2` or `.xz`
file extension to store the cache in a compressed format, or `.csv`
for uncompressed:


```python
from ebmdatalab import bq

sql = "SELECT * FROM ebmdatalab.hscic.bnf"
df = bq.cached_read(sql, csv_path='bnf_codes.zip')  # add `use_cache=False` to override
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
    
 ## Updating the package in Windows
 
**1. Clone repository to local drive e.g. through GitHub desktop.**

**2. Open Anaconda command prompt by right-clicking and selecting `Run as administrator`.**
  - Type `pip list` to check that `ebmdatalab` is installed
    - If it is, uninstall using `pip uninstall ebmdatalab`
  - Install `flit`: check if already installed using e.g. `flit help`, if not, type `pip install flit`
  - Change directory to work in same location as the repo e.g. `>cd C:\Users\hcurtis\Documents\GitHub\datalab-pandas`
  - Install `symlink`: `flit install --symlink`
  
**3. Make changes to the package `.py` files as required**
   - Edit code e.g. via Jupyter notebook
   - If you think this change should be incorporated into its own release, open `__init__.py` and increase the version number
   
**4. Test the changes**
   - To avoid having to restart the kernel every time you make a change, add the following commands in your notebook to tell the kernel to update its reference to the package (e.g. for `charts`):
```python
import importlib
from ebmdatalab import charts
importlib.reload(charts)
```

**5. Push changes**
   - Open GitHub desktop and you should see your changed files.
   - Create a branch rather than commiting to `master`.
   - Describe and commit changes.
   - Make a pull request to merge branch with master (select from dropdown menu under `Branch`). 
   - This will take you to GitHub where you need to click `Create pull request`
 
 
 
