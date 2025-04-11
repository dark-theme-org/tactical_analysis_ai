"""
This script processes parquet files from a source directory
and saves them to a destination directory.
It uses joblib for parallel processing and handles file paths
and separators for compatibility.
"""

import joblib
from utils.io.io import glob, read_parquet, to_parquet
from utils.io.paths import (
    READ_DATA_MODE,
    READ_DATA_PATH,
    READ_SEP,
    WRITE_DATA_PATH,
    WRITE_SEP,
    path_join,
)


def process_parquets(file):

    """
    Process parquet files from the source directory and save them to the destination directory.
    """

    # Read parquet file
    print(f"Processing file: {file}")

    df = read_parquet(path=file)

    file_dest = WRITE_DATA_PATH + file.replace(READ_DATA_PATH, "").replace(
        READ_SEP, WRITE_SEP
    )

    to_parquet(data=df, path=file_dest, index=False)

    print(f"{file} processed successfully")


glob_folder = path_join(READ_DATA_PATH, "**", "*.parquet", mode=READ_DATA_MODE)

file_list = glob(glob_folder, recursive=True, include_hidden=True)

job = joblib.Parallel(n_jobs=-1, verbose=10)(
    joblib.delayed(process_parquets)(file) for file in file_list
)  # process all files in parallel
