import pandas as pd
import os
import joblib
import glob
import json

from utils.io.paths import DICT_PATHS


def process_games_file(file):

    print(f"Processing file: {file}")

    game_id = os.path.basename(file).split(".")[0]

    df_games = json.loads(pd.read_json(file).to_json(orient="records"))
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

    df_games.to_parquet(f'{DICT_PATHS["cleaned_games"]}/{game_id}.parquet', index=False)


file_list = glob.glob(
    DICT_PATHS["raw_games"] + "/*.json"
)  # get the list of all json files in the directory

joblib.Parallel(n_jobs=-1, verbose=10)(
    joblib.delayed(process_games_file)(file) for file in file_list
)  # process all files in parallel
