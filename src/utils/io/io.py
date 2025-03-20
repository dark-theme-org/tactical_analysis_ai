"""Module to standardize io operations. It has support to Pandas and Dask Frameworks"""
import dask.dataframe as dd
import pandas as pd
from utils.io.paths import (
    READ_DATA_MODE,
    READ_DICT_PATHS,
    READ_STORAGE_OPTIONS,
    WRITE_DATA_MODE,
    WRITE_DICT_PATHS,
    WRITE_STORAGE_OPTIONS,
    path_join,
)

FRAMEWORK_DICT = {"pandas": pd, "dask": dd}


def read_any(func, folder, file, framework="pandas", **kwargs):
    """
    Reads a file using the specified function and framework.

    Parameters:
        func (str): The name of the read function (e.g., 'read_csv', 'read_parquet').
        folder (str): The folder key to retrieve the read path.
        file (str): The filename to read.
        framework (str, optional): The data framework to use ('pandas' or 'dask').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.

    Returns:
        DataFrame: A Pandas or Dask DataFrame depending on the chosen framework.
    """
    path = path_join(READ_DICT_PATHS[folder], file, mode=READ_DATA_MODE)
    framework = FRAMEWORK_DICT.get(framework, "pandas")
    read_func = getattr(framework, func)
    return read_func(path, storage_options=READ_STORAGE_OPTIONS, **kwargs)


def to_any(func, data, folder, file, **kwargs):
    """
    Writes a DataFrame to a file using the specified function.

    Parameters:
        func (str): The name of the write function (e.g., 'to_csv', 'to_parquet').
        data (DataFrame): The DataFrame to be saved.
        folder (str): The folder key to retrieve the write path.
        file (str): The filename to write to.
        **kwargs: Additional arguments passed to the write function.

    Returns:
        None
    """
    path = path_join(WRITE_DICT_PATHS[folder], file, mode=WRITE_DATA_MODE)
    return getattr(data, func)(path, storage_options=WRITE_STORAGE_OPTIONS, **kwargs)


def read_parquet(folder, file, framework="pandas", **kwargs):
    """
    Reads a Parquet file using the specified framework.
    """
    return read_any(
        func="read_parquet", folder=folder, file=file, framework=framework, **kwargs
    )


def read_csv(folder, file, framework="pandas", **kwargs):
    """
    Reads a CSV file using the specified framework.
    """
    return read_any(
        func="read_csv", folder=folder, file=file, framework=framework, **kwargs
    )


def read_json(folder, file, framework="pandas", **kwargs):
    """
    Reads a JSON file using the specified framework.
    """
    return read_any(
        func="read_json", folder=folder, file=file, framework=framework, **kwargs
    )


def to_parquet(data, folder, file, **kwargs):
    """
    Writes a DataFrame to a Parquet file.
    """
    return to_any(func="to_parquet", data=data, folder=folder, file=file, **kwargs)


def to_csv(data, folder, file, **kwargs):
    """
    Writes a DataFrame to a CSV file.
    """
    return to_any(func="to_csv", data=data, folder=folder, file=file, **kwargs)


def to_json(data, folder, file, **kwargs):
    """
    Writes a DataFrame to a JSON file.
    """
    return to_any(func="to_json", data=data, folder=folder, file=file, **kwargs)
