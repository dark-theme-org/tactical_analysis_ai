import pandas as pd
import joblib
import glob

from utils.paths import DICT_PATHS, path_join, SEP

def preprocess_json_column(df: pd.DataFrame,
                           column: str,
                           mode: str = 'Smoothed'):

    if column != 'ballsSmoothed':
      df_players = df.explode(column).reset_index(drop=True)
    else:
      df_players = df

    df_players = pd.concat([df_players['frameNum'],
                            pd.json_normalize(df_players[column])], axis=1)

    if 'Players' in column:
      df_players = df_players.dropna(subset=['jerseyNum'])

    df_players['teamGame'] = column
    df_players['smooth_mode'] = mode

    return df_players

def preprocess_tracking_data(game_id):

    raw_tracking_folder = DICT_PATHS['raw_tracking']
    tracking_file = path_join(raw_tracking_folder, f'{game_id}.jsonl.bz2')

    print(tracking_file)

    print(f'Read tracking data for game {game_id}...')

    tracking = pd.read_json(tracking_file, lines=True, engine='pyarrow')
    tracking = tracking.drop_duplicates(subset=['frameNum'])

    columns = ['homePlayers','awayPlayers','balls']
    modes = ['Raw']

    print(f'Read each column data in parallel')

    df_full = joblib.Parallel(n_jobs=3)(joblib.delayed(preprocess_json_column)(tracking[['frameNum', column]], column, mode)
                                         for column in columns
                                         for mode in modes)

    df_full = pd.concat(df_full, ignore_index=True)

    time_cols = ['frameNum',
                'videoTimeMs',
                'period',
                'periodElapsedTime',
                'periodGameClockTime']

    df_full['game.id'] = game_id

    df_full['jerseyNum'] = df_full['jerseyNum'].fillna(-1).astype('int')

    df_full = df_full.reset_index(drop=True)

    index = ['game.id',
            'frameNum',
            'teamGame',
            'jerseyNum',
            'smooth_mode']

    df_full = df_full.set_index(index)[['visibility','confidence','x','y','z']].unstack('smooth_mode')

    df_full.columns = ['.'.join(col).lower() for col in df_full.columns]

    df_full = df_full.reset_index()

    df_full = df_full.merge(tracking[time_cols],
                            on=['frameNum'],
                            how='left')

    df_full['z.raw'] = df_full['z.raw'].fillna(0)

    df_full.to_parquet(path_join(DICT_PATHS['cleaned_tracking'],
                                    f'{game_id}.parquet')
                )

    del tracking
    del df_full

for files in glob.glob(DICT_PATHS['raw_tracking'] + '/*.jsonl.bz2'):

    game_id = int(files.split(SEP)[-1].split('.')[0])

    preprocess_tracking_data(game_id)
    print(f'Game {game_id} tracking data has been preprocessed')




