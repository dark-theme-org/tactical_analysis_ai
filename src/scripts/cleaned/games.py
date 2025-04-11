"""This script processes the games data from JSON files
and converts them into a cleaned Parquet format."""
import json
import os

import joblib
import pandas as pd
from utils.io.io import glob, read_json, to_parquet


def process_games_file(file: str) -> None:

    """
    Process a single JSON file containing game data.
    It reads the JSON file, normalizes the data, and saves it as a Parquet file.

    Args:
        file (str): The path to the JSON file to process.

    Returns:
        None
    """

    print(f"Processing file: {file}")

    game_id = os.path.basename(file).split(".")[0]

    df_games = json.loads(read_json(file).to_json(orient="records"))
    df_games = pd.concat(
        [
            pd.json_normalize(df_games).drop(columns=["stadium.pitches"]),
            pd.json_normalize(
                df_games,
                record_path=["stadium", ["pitches"]],
                record_prefix="stadium.pitches.",
            ),
        ],
        axis=1,
    )
    df_games["game.id"] = int(game_id)

    to_parquet(data=df_games, path=f"data/cleaned/games/{game_id}.parquet", index=False)


if __name__ == "__main__":

    file_list = glob(
        "data/raw/games/*.json"
    )  # get the list of all json files in the directory

    joblib.Parallel(n_jobs=-1, verbose=10)(
        joblib.delayed(process_games_file)(file) for file in file_list
    )  # process all files in parallel
