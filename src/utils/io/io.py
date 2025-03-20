"""Module to standardize io operations. It has support to Pandas and Dask Frameworks"""
import dask.dataframe as dd
import pandas as pd
from utils.io.paths import (
    READ_DATA_MODE,
    READ_SEP,
    READ_STORAGE_OPTIONS,
    READ_BUCKET,
    WRITE_DATA_MODE,
    WRITE_SEP,
    WRITE_STORAGE_OPTIONS,
    WRITE_BUCKET,
    path_join,
)

FRAMEWORK_DICT = {"pandas": pd, "dask": dd}


def read_any(func: str, path: str, framework: str = "pandas", **kwargs):
    """
    Reads a file using the specified function and framework.

    Parameters:
        func (str): The name of the read function (e.g., 'read_csv', 'read_parquet').
        path (str): The path of the to read. Use / as separator.
        framework (str, optional): The data framework to use ('pandas' or 'dask').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.

    Returns:
        DataFrame: A Pandas or Dask DataFrame depending on the chosen framework.
    """
    if (READ_DATA_MODE == "local") and (READ_SEP != "/"):
        path = path.replace("/", READ_SEP)

    path = path_join(READ_BUCKET, path, mode=READ_DATA_MODE)

    framework = FRAMEWORK_DICT.get(framework, "pandas")

    read_func = getattr(framework, func)

    return read_func(path, storage_options=READ_STORAGE_OPTIONS, **kwargs)


def to_any(func, data, path: str, **kwargs):
    """
    Writes a DataFrame to a file using the specified function.

    Parameters:
        func (str): The name of the write function (e.g., 'to_csv', 'to_parquet').
        data (DataFrame): The DataFrame to be saved.
        path (str): The path to write the file. Use / as separator.
        **kwargs: Additional arguments passed to the write function.

    Returns:
        None
    """

    if (WRITE_DATA_MODE == "local") and (WRITE_SEP != "/"):
        path = path.replace("/", WRITE_SEP)

    path = path_join(WRITE_BUCKET, path, mode=WRITE_DATA_MODE)

    return getattr(data, func)(path, storage_options=WRITE_STORAGE_OPTIONS, **kwargs)


def read_parquet(path: str, framework: str = "pandas", **kwargs):
    """
    Reads a Parquet file using the specified framework.
    """
    return read_any(func="read_parquet", path=path, framework=framework, **kwargs)


def read_csv(path: str, framework: str = "pandas", **kwargs):
    """
    Reads a CSV file using the specified framework.
    """
    return read_any(func="read_csv", path=path, framework=framework, **kwargs)


def read_json(path: str, framework: str = "pandas", **kwargs):
    """
    Reads a JSON file using the specified framework.
    """
    return read_any(func="read_json", path=path, framework=framework, **kwargs)


def to_parquet(data, path: str, **kwargs):
    """
    Writes a DataFrame to a Parquet file.
    """
    return to_any(func="to_parquet", data=data, path=path, **kwargs)


def to_csv(data, path: str, **kwargs):
    """
    Writes a DataFrame to a CSV file.
    """
    return to_any(func="to_csv", data=data, path=path, **kwargs)


def to_json(data, path: str, **kwargs):
    """
    Writes a DataFrame to a JSON file.
    """
    return to_any(func="to_json", data=data, path=path, **kwargs)
