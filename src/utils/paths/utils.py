import os

FOLDER_PATH = os.getenv('FOLDER_PATH',
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if FOLDER_PATH.startswith('s3'):
    SEP = '/'
    path_join = lambda *args: SEP.join(*args)
    STORAGE_OPTIONS = {'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
                       'AWS_SECRET_KEY_ID': os.getenv('AWS_SECRET_KEY_ID')}
else:
    SEP = os.sep
    path_join = path_join

DATA_PATH = path_join(FOLDER_PATH, 'data')

LAYERS = ['raw', 'cleaned', 'curated']
FOLDERS = ['tracking', 'lineups', 'games', 'events']

DICT_PATHS = {f'{layer}_{folder}': path_join(DATA_PATH, layer, folder)
              for layer in LAYERS
              for folder in FOLDERS}