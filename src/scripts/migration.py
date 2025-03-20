import joblib
import glob

from utils.io.paths import (
    READ_DATA_MODE,
    READ_DATA_PATH,
    WRITE_DATA_PATH,
    READ_SEP,
    WRITE_SEP,
    path_join,
)
from utils.io.io import read_parquet


def process_parquets(file):

    print(f"Processing file: {file}")

    df = read_parquet(file)

    file_dest = WRITE_DATA_PATH + file.replace(READ_DATA_PATH, "").replace(
        READ_SEP, WRITE_SEP
    )

    df.to_parquet(file_dest, index=False)

    print(f"{file} processed successfully")


glob_folder = path_join(READ_DATA_PATH, "**", "*.parquet", mode=READ_DATA_MODE)

# TODO: Create abstract glob function in utils.io.paths module
file_list = glob.glob(glob_folder, recursive=True, include_hidden=True)

job = joblib.Parallel(n_jobs=-1, verbose=10)(
    joblib.delayed(process_parquets)(file) for file in file_list
)  # process all files in parallel
