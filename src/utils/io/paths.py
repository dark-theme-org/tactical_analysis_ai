"""Module to standardize paths across the project.
   It allows to easily switch between local and cloud"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

READ_DATA_MODE = os.getenv("READ_DATA_MODE", "local")
WRITE_DATA_MODE = os.getenv("WRITE_DATA_MODE", "local")

print(
    f"Running with READ_DATA_MODE={READ_DATA_MODE} and WRITE_DATA_MODE={WRITE_DATA_MODE}"
)

LOCAL_STORAGE_OPTIONS = {}
S3_STORAGE_OPTIONS = {
    "key": os.getenv("AWS_ACCESS_KEY_ID"),
    "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
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


S3_BUCKET = os.getenv("S3_BUCKET").rstrip(S3_SEP)
LOCAL_BUCKET = os.getenv("LOCAL_BUCKET", "").rstrip(LOCAL_SEP)
READ_BUCKET = S3_BUCKET if READ_DATA_MODE == "s3" else LOCAL_BUCKET
WRITE_BUCKET = S3_BUCKET if WRITE_DATA_MODE == "s3" else LOCAL_BUCKET

S3_DATA_PATH = s3_path_join(S3_BUCKET, "data")
LOCAL_DATA_PATH = local_path_join(LOCAL_BUCKET, "data")
READ_DATA_PATH = S3_DATA_PATH if READ_DATA_MODE == "s3" else LOCAL_DATA_PATH
WRITE_DATA_PATH = S3_DATA_PATH if WRITE_DATA_MODE == "s3" else LOCAL_DATA_PATH
