"""Module to standardize paths across the project.
   It allows to easily switch between local and cloud"""
import os

import dotenv

dotenv.load_dotenv(".env")

READ_DATA_MODE = os.getenv("READ_DATA_MODE", "local")
WRITE_DATA_MODE = os.getenv("WRITE_DATA_MODE", "local")

LOCAL_STORAGE_OPTIONS = {}
S3_STORAGE_OPTIONS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_KEY_ID": os.getenv("AWS_SECRET_KEY_ID"),
}
READ_STORAGE_OPTIONS = (
    S3_STORAGE_OPTIONS if READ_DATA_MODE == "s3" else LOCAL_STORAGE_OPTIONS
)
WRITE_STORAGE_OPTIONS = (
    S3_STORAGE_OPTIONS if WRITE_DATA_MODE == "s3" else LOCAL_STORAGE_OPTIONS
)

LOCAL_SEP = os.sep
S3_SEP = "/"
READ_SEP = S3_SEP if READ_DATA_MODE == "s3" else LOCAL_SEP
WRITE_SEP = S3_SEP if WRITE_DATA_MODE == "s3" else LOCAL_SEP


def local_path_join(*args):
    """
    Joins path components using the local filesystem separator.

    Parameters:
        *args: Components of the path.

    Returns:
        str: Joined path string.
    """
    return os.path.join(*args)


def s3_path_join(*args):
    """
    Joins path components using the S3 path separator ('/').

    Parameters:
        *args: Components of the path.

    Returns:
        str: Joined S3 path string.
    """
    return S3_SEP.join(args)


def path_join(*args, mode="local"):
    """
    Joins path components based on the specified storage mode.

    Parameters:
        *args: Components of the path.
        mode (str, optional): Storage mode ('local' or 's3'). Defaults to 'local'.

    Returns:
        str: Joined path string based on the mode.
    """
    if mode == "s3":
        return s3_path_join(*args)
    return local_path_join(*args)


S3_BUCKET = os.getenv("S3_BUCKET")
LOCAL_BUCKET = os.getenv("LOCAL_BUCKET", "")

S3_DATA_PATH = s3_path_join(S3_BUCKET, "data")
LOCAL_DATA_PATH = local_path_join(LOCAL_BUCKET, "data")
READ_DATA_PATH = S3_DATA_PATH if READ_DATA_MODE == "s3" else LOCAL_DATA_PATH
WRITE_DATA_PATH = S3_DATA_PATH if WRITE_DATA_MODE == "s3" else LOCAL_DATA_PATH

LAYERS = ["raw", "cleaned", "curated"]
FOLDERS = ["tracking", "lineups", "games", "events"]

READ_DICT_PATHS = {
    f"{layer}_{folder}": path_join(READ_DATA_PATH, layer, folder, mode=READ_DATA_MODE)
    for layer in LAYERS
    for folder in FOLDERS
}

WRITE_DICT_PATHS = {
    f"{layer}_{folder}": path_join(WRITE_DATA_PATH, layer, folder, mode=WRITE_DATA_MODE)
    for layer in LAYERS
    for folder in FOLDERS
}
