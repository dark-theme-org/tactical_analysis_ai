import pandas as pd
import os
import joblib
import glob

from utils.io.paths import STORAGE_OPTIONS, FOLDER_PATH, DATA_PATH, S3_BUCKET, path_join


# WARNING: THIS SCRIPT WILL ONLY WORK WHEN FOLDER_PATH IS A LOCAL FOLDER
def process_parquets(file):

    print(f"Processing file: {file}")

    df = pd.read_parquet(file)

    file_dest = S3_BUCKET + file.replace(FOLDER_PATH, "").replace(os.sep, "/")

    df.to_parquet(file_dest, index=False, storage_options=STORAGE_OPTIONS)

    print(f"{file} processed successfully")


glob_folder = path_join(DATA_PATH, "**", "*.parquet")

file_list = glob.glob(glob_folder, recursive=True, include_hidden=True)

job = joblib.Parallel(n_jobs=-1, verbose=10)(
    joblib.delayed(process_parquets)(file) for file in file_list
)  # process all files in parallel
