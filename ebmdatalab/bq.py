import glob
import os
import random
import re
from hashlib import md5
import string

from google.oauth2.service_account import Credentials
import pandas as pd


def fingerprint_sql(sql):
    # remove comments
    sql = re.sub(r"--(.*)", "", sql)
    # remove whitespace
    sql = re.sub(r"\s", "", sql)
    # lowercase everything not in double quotes
    to_lowercase = sql[:]
    to_substitute = []
    for quoted in re.findall(r'".*?"', sql):
        to_lowercase = to_lowercase.replace(quoted, "{}")
        to_substitute.append(quoted)
    to_lowercase = to_lowercase.lower()
    sql = to_lowercase.format(*to_substitute)
    return md5(sql.encode("utf-8")).hexdigest()


def cached_read(sql, csv_path=None, use_cache=True, **kwargs):
    """Run SQL in BigQuery and return dataframe, caching results in a CSV
    file

    """
    assert csv_path, "You must supply csv_path"
    fingerprint = fingerprint_sql(sql)
    csv_dir, csv_filename = os.path.split(csv_path)
    fingerprint_path = os.path.join(
        csv_dir, "." + csv_filename + "." + fingerprint + ".tmp"
    )
    already_cached = os.path.exists(fingerprint_path)
    if use_cache and already_cached:
        return pd.read_csv(csv_path)

    defaults = {
        "project_id": "ebmdatalab",
        "dialect": "standard",
        "credentials": load_credentials(),
    }
    defaults.update(kwargs)
    os.makedirs(csv_dir, exist_ok=True)
    temp_path = os.path.join(
        csv_dir, '.tmp{}.{}'.format(_random_str(8), csv_filename)
    )
    df = pd.read_gbq(sql, **defaults)
    df.to_csv(temp_path, index=False)
    old_fingerprint_files = glob.glob(
        os.path.join(csv_dir, "." + csv_filename + ".*.tmp")
    )
    for f in old_fingerprint_files:
        os.remove(f)
    os.replace(temp_path, csv_path)
    with open(fingerprint_path, "w") as f:
        f.write("File created by {}".format(__file__))
    return df


def _random_str(length):
    return ''.join(
        [random.choice(string.ascii_lowercase) for _ in range(length)]
    )


def load_credentials():
    # To authenticate with a service account EBMDATALAB_BQ_CREDENTIALS_PATH should be
    # the path of a file containing the service account's private key.  See README.md
    # for requirements of the service account.
    path = os.getenv("EBMDATALAB_BQ_CREDENTIALS_PATH")
    if path is None:
        # If no credentials are provided, users will have to authenticate via OAuth.
        return
    return Credentials.from_service_account_file(path)
