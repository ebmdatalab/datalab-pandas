from mock import patch
from datalab import bq
from pandas import DataFrame
import tempfile


def test_fingerprint_sql():
    input_sql = (
        'select *, "Frob" from x -- comment\n'
        'where (a >= 4);')
    same_sql_different_caps = (
        'SELECT *, "Frob" from x -- comment\n'
        'where (a >= 4);')
    same_sql_different_quoted_caps = (
        'SELECT *, "frob" from x -- comment\n'
        'where (a >= 4);')
    same_sql_different_comment = (
        'select *, "Frob" from x -- comment 2\n'
        'where (a >= 4);')
    same_sql_different_whitespace = (
        'select *, "Frob" from x -- comment 2\n'
        '\n'
        ' where (a >= 4);')
    fingerprint = bq.fingerprint_sql(input_sql)

    assert fingerprint == bq.fingerprint_sql(same_sql_different_caps)
    assert fingerprint != bq.fingerprint_sql(same_sql_different_quoted_caps)
    assert fingerprint == bq.fingerprint_sql(same_sql_different_comment)
    assert fingerprint == bq.fingerprint_sql(same_sql_different_whitespace)


@patch('datalab.bq.pd.read_gbq')
def test_cached_read(mock_read_gbq):
    mock_read_gbq.return_value = DataFrame([{'a': 3}])
    sql = "select * from foobar"

    # Test identical SQL bypasses reading BQ
    with tempfile.NamedTemporaryFile() as csv_file:
        for _ in range(0, 2):
            df = bq.cached_read(
                sql,
                csv_path=csv_file.name)
        assert df.loc[0]['a'] == 3
        mock_read_gbq.assert_called_once()
