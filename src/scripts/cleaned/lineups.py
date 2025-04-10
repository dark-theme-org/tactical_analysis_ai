"""
This script processes the lineups data from JSON files
and converts them into a cleaned Parquet format.
It reads the JSON files, normalizes the data,
and saves it in a structured format for further analysis.
It also handles the extraction of specific columns
and ensures that the data is in a consistent format.
"""
import os
import json
import joblib
import pandas as pd

from utils.io.io import read_json, to_parquet, glob


def process_lineups_file(file):

    """
    Process a single JSON file containing lineup data.
    It reads the JSON file, normalizes the data, and saves it as a Parquet file.

    Args:
        file (str): The path to the JSON file to process.

    Returns:
        None
    """

    print(f"Processing file: {file}")

    game_id = os.path.basename(file).split(".")[0]

    df_lineups = json.loads(read_json(file).to_json(orient="records"))
    df_lineups = pd.json_normalize(df_lineups)
    df_lineups["game.id"] = int(game_id)
    df_lineups = df_lineups.rename(columns={"shirtNumber": "jerseyNum"})

    to_parquet(
        data=df_lineups, path=f"data/cleaned/lineups/{game_id}.parquet", index=False
    )


file_list = glob(
    "data/raw/lineups/*.json"
)  # get the list of all json files in the directory

job = joblib.Parallel(n_jobs=-1, verbose=10)(
    joblib.delayed(process_lineups_file)(file) for file in file_list
)  # process all files in parallel
