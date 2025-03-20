import os
import dotenv

dotenv.load_dotenv(".env")

FOLDER_PATH = os.getenv("FOLDER_PATH")

if FOLDER_PATH.startswith("s3"):
    SEP = "/"

    def path_join(*args):
        return SEP.join(args)

    STORAGE_OPTIONS = {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_KEY_ID": os.getenv("AWS_SECRET_KEY_ID"),
    }

else:
    SEP = os.sep
    path_join = os.path.join
    STORAGE_OPTIONS = {}
    S3_BUCKET = FOLDER_PATH

DATA_PATH = path_join(FOLDER_PATH, "data")

LAYERS = ["raw", "cleaned", "curated"]
FOLDERS = ["tracking", "lineups", "games", "events"]

DICT_PATHS = {
    f"{layer}_{folder}": path_join(DATA_PATH, layer, folder)
    for layer in LAYERS
    for folder in FOLDERS
}
