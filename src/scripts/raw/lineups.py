import pandas as pd
import os
import joblib
import glob
import json

from utils.paths import DICT_PATHS

def process_lineups_file(file):

    print(f'Processing file: {file}')

    game_id = os.path.basename(file).split('.')[0]

    df_lineups = json.loads(pd.read_json(file).to_json(orient='records'))
    df_lineups = pd.json_normalize(df_lineups)
    df_lineups["game.id"] = int(game_id)
    df_lineups = df_lineups.rename(columns={'shirtNumber':'jerseyNum'})

    df_lineups.to_parquet(f'{DICT_PATHS["cleaned_lineups"]}/{game_id}.parquet', index=False)

file_list = glob.glob(DICT_PATHS['raw_lineups'] + '/*.json') # get the list of all json files in the directory

job = joblib.Parallel(n_jobs=-1, verbose=10)(joblib.delayed(process_lineups_file)(file) for file in file_list) # process all files in parallel
