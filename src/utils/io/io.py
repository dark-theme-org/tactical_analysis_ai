"""Module to standardize io operations. It has support to Pandas and Dask Frameworks"""
from typing import Union

import dask.dataframe as dd
import fsspec
import pandas as pd
import polars as pl
from utils.io.paths import (
    READ_BUCKET,
    READ_DATA_MODE,
    READ_SEP,
    READ_STORAGE_OPTIONS,
    WRITE_BUCKET,
    WRITE_DATA_MODE,
    WRITE_SEP,
    WRITE_STORAGE_OPTIONS,
    path_join,
)

FRAMEWORK_DICT = {"pandas": pd, "dask": dd, "polars": pl}


def glob(path: str, **kwargs) -> list:

    """
    Returns a list of files matching the given pattern.

    Args:
        path (str): The pattern to match files. Can be a glob pattern or a directory.
        **kwargs: Additional arguments passed to the glob function.
    Returns:
        list: A list of file paths matching the pattern.
    """

    if READ_DATA_MODE == "s3":
        fs = fsspec.filesystem("s3", storage_options=READ_STORAGE_OPTIONS)
    else:
        fs = fsspec.filesystem("file")

    return fs.glob(path, **kwargs)


def read_any(
    func: str, path: str, framework: str = "pandas", **kwargs
) -> Union[pd.DataFrame, dd.DataFrame, pl.DataFrame]:
    """
    Reads a file using the specified function and framework.

    Parameters:
        func (str): The name of the read function (e.g., 'read_csv', 'read_parquet').
        path (str): The path of the to read. Use / as separator.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.

    Returns:
        DataFrame: A Pandas, Dask or Polars DataFrame depending on the chosen framework.
    """
    if (READ_DATA_MODE == "local") and (READ_SEP != "/"):
        path = path.replace("/", READ_SEP)

    path = path_join(READ_BUCKET, path, mode=READ_DATA_MODE)

    framework = FRAMEWORK_DICT.get(framework, "pandas")

    read_func = getattr(framework, func)

    return read_func(path, storage_options=READ_STORAGE_OPTIONS, **kwargs)


def to_any(
    func: str,
    data: Union[pd.DataFrame, dd.DataFrame],
    path: str,
    framework: str = "pandas",
    **kwargs
) -> None:
    """
    Writes a DataFrame to a file using the specified function.

    Parameters:
        func (str): The name of the write function (e.g., 'to_csv', 'to_parquet').
        data (Union[pd.DataFrame, dd.DataFrame]): The DataFrame to be saved.
        path (str): The path to write the file. Use / as separator.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the write function.

    Returns:
        None
    """

    if (WRITE_DATA_MODE == "local") and (WRITE_SEP != "/"):
        path = path.replace("/", WRITE_SEP)

    path = path_join(WRITE_BUCKET, path, mode=WRITE_DATA_MODE)

    if framework == "polars":
        func = func.replace("to_", "write_")

    return getattr(data, func)(path, storage_options=WRITE_STORAGE_OPTIONS, **kwargs)


def read_parquet(
    path: str, framework: str = "pandas", **kwargs
) -> Union[pd.DataFrame, dd.DataFrame, pl.DataFrame]:
    """
    Reads a Parquet file using the specified framework.

    Parameters:
        path (str): The path to the Parquet file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.
    Returns:
        DataFrame: A Pandas, Dask or Polars DataFrame depending on the chosen framework.
    Raises:
        ValueError: If the framework is not supported.
    """
    return read_any(func="read_parquet", path=path, framework=framework, **kwargs)


def read_csv(
    path: str, framework: str = "pandas", **kwargs
) -> Union[pd.DataFrame, dd.DataFrame, pl.DataFrame]:
    """
    Reads a CSV file using the specified framework.

    Parameters:
        path (str): The path to the CSV file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.
    Returns:
        DataFrame: A Pandas, Dask or Polars DataFrame depending on the chosen framework.
    Raises:
        ValueError: If the framework is not supported.
    """
    return read_any(func="read_csv", path=path, framework=framework, **kwargs)


def read_json(
    path: str, framework: str = "pandas", **kwargs
) -> Union[pd.DataFrame, dd.DataFrame, pl.DataFrame]:
    """
    Reads a JSON file using the specified framework.

    Parameters:
        path (str): The path to the JSON file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the read function.
    Returns:
        DataFrame: A Pandas, Dask or Polars DataFrame depending on the chosen framework.
    Raises:
        ValueError: If the framework is not supported.
    """
    return read_any(func="read_json", path=path, framework=framework, **kwargs)


def to_parquet(
    data: Union[pd.DataFrame, dd.DataFrame, pl.DataFrame],
    path: str,
    framework: str = "pandas",
    **kwargs
):
    """
    Writes a DataFrame to a Parquet file.

    Parameters:
        data (Union[pd.DataFrame, dd.DataFrame]): The DataFrame to be saved.
        path (str): The path to write the Parquet file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the write function.
    Returns:
        None
    Raises:
        ValueError: If the framework is not supported.
    """
    return to_any(
        func="to_parquet", data=data, path=path, framework=framework, **kwargs
    )


def to_csv(
    data: Union[pd.DataFrame, dd.DataFrame, pl.DataFrame],
    path: str,
    framework: str = "pandas",
    **kwargs
):
    """
    Writes a DataFrame to a CSV file.

    Parameters:
        data (Union[pd.DataFrame, dd.DataFrame]): The DataFrame to be saved.
        path (str): The path to write the CSV file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the write function.
    Returns:
        None
    Raises:
        ValueError: If the framework is not supported.
    """
    return to_any(func="to_csv", data=data, path=path, framework=framework, **kwargs)


def to_json(
    data: Union[pd.DataFrame, dd.DataFrame, pl.DataFrame],
    path: str,
    framework: str = "pandas",
    **kwargs
):
    """
    Writes a DataFrame to a JSON file.

    Parameters:
        data (Union[pd.DataFrame, dd.DataFrame]): The DataFrame to be saved.
        path (str): The path to write the JSON file.
        framework (str, optional): The data framework to use ('pandas', 'dask' or 'polars').
                                   Defaults to 'pandas'.
        **kwargs: Additional arguments passed to the write function.
    Returns:
        None
    Raises:
        ValueError: If the framework is not supported.
    """
    return to_any(func="to_json", data=data, path=path, framework=framework, **kwargs)
