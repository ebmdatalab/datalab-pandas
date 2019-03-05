from mock import patch
from ebmdatalab import bq
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


@patch('ebmdatalab.bq.pd.read_gbq')
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
        assert mock_read_gbq.call_count == 1

        # and now with `use_cache` param
        df = bq.cached_read(sql, csv_path=csv_file.name, use_cache=False)
        assert mock_read_gbq.call_count == 2


def _check_cached_read(csv_file, mock_read, sql, expected):
        mock_read.return_value = expected
        df = bq.cached_read(sql, csv_path=csv_file.name)
        assert str(df) == str(expected)


@patch('ebmdatalab.bq.pd.read_gbq')
def test_old_cache_markers_removed(mock_read_gbq):
    with tempfile.NamedTemporaryFile() as csv_file:
        # First, cause some sql to be cached
        inputs_and_outputs = [
            (
                "select * from foobar",
                DataFrame([{'a': 1}])
            ),
            (
                "select * from foobar order by id",
                DataFrame([{'a': 2}])
            )
        ]
        _check_cached_read(csv_file, mock_read_gbq, *inputs_and_outputs[0])
        _check_cached_read(csv_file, mock_read_gbq, *inputs_and_outputs[1])
        _check_cached_read(csv_file, mock_read_gbq, *inputs_and_outputs[0])
