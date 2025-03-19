import dash
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_player
import numpy as np
import pandas as pd
from utils.paths import DICT_PATHS, path_join
from utils.plots.pitch import drawPitch

#game selected
game_id = 10510

#loading_data
tracking_df = pd.read_parquet(path_join(DICT_PATHS['cleaned_tracking'], f'{game_id}.parquet'))
games_df = pd.read_parquet(path_join(DICT_PATHS['cleaned_games'], f'{game_id}.parquet'))
lineups_df = pd.read_parquet(path_join(DICT_PATHS['cleaned_lineups'], f'{game_id}.parquet'))

#getting video id to make the playlist url
video_id = games_df['videoUrl'].unique()[0].split('/')[-1]

#pitch variables
pitch_length = games_df['stadium.pitches.length'].unique()[0]
pitch_width = games_df['stadium.pitches.width'].unique()[0]
xaxis_range = [0, pitch_length]
yaxis_range = [0, pitch_width]

#game_variables
homeTeamName = games_df['homeTeam.name'].unique()[0]
awayTeamName = games_df['awayTeam.name'].unique()[0]

#creating a mock for the pitch_df

# Calculate the distance from each square to the goal
x_coords = pd.DataFrame(np.arange(0, pitch_length + 1), columns=['x_int']).assign(foo=1)
y_coords = pd.DataFrame(np.arange(0, pitch_width + 1), columns=['y_int']).assign(foo=1)

field_grid = pd.merge(x_coords, y_coords, on='foo').drop('foo', axis=1)

goal_positions = {'left': [0, pitch_width / 2], 'right': [pitch_length, pitch_width / 2]}

for goal, (goal_x, goal_y) in goal_positions.items():
    field_grid[f'distance_to_{goal}_goal'] = np.sqrt((field_grid['x_int'] - goal_x)**2 + (field_grid['y_int'] - goal_y)**2)
    field_grid[f'space_value_{goal}_goal'] = 1 - (field_grid[f'distance_to_{goal}_goal'] / np.sqrt(pitch_length**2 + pitch_width**2))

games_lineups_df = pd.merge(lineups_df,
                            games_df,
                            on = ['game.id'])

#getting teamgame to make merge easier

games_lineups_df['teamGame'] = np.where(
        games_lineups_df['team.id']==games_lineups_df['homeTeam.id'],
        'homePlayers',
        'awayPlayers')

games_lineups_df = games_lineups_df[['teamGame',
                                    'jerseyNum',
                                    'player.id',
                                    'player.nickname',
                                    'positionGroupType',
                                    'homeTeamKit.primaryColor',
                                    'awayTeamKit.primaryColor']]

#processing coordinate data

tracking_df['x'] = tracking_df[f'x.raw'] + (pitch_length / 2)
tracking_df['y'] = tracking_df[f'y.raw'] + (pitch_width / 2)
tracking_df['z'] = tracking_df[f'z.raw']

tracking_df['x_ball'] = np.where(tracking_df['teamGame']=='balls', tracking_df['x'], np.nan)
tracking_df['y_ball'] = np.where(tracking_df['teamGame']=='balls', tracking_df['y'], np.nan)
tracking_df['z_ball'] = np.where(tracking_df['teamGame']=='balls', tracking_df['z'], np.nan)

tracking_df['x_ball'] = tracking_df.groupby('frameNum')['x_ball'].transform('max')
tracking_df['y_ball'] = tracking_df.groupby('frameNum')['y_ball'].transform('max')
tracking_df['z_ball'] = tracking_df.groupby('frameNum')['z_ball'].transform('max')

tracking_df['x_ball'] = tracking_df.groupby(['jerseyNum','teamGame'])['x_ball'].ffill()
tracking_df['y_ball'] = tracking_df.groupby(['jerseyNum','teamGame'])['y_ball'].ffill()
tracking_df['z_ball'] = tracking_df.groupby(['jerseyNum','teamGame'])['z_ball'].ffill()

tracking_df['x'] = tracking_df.groupby(['jerseyNum','teamGame'])['x'].ffill()
tracking_df['y'] = tracking_df.groupby(['jerseyNum','teamGame'])['y'].ffill()
tracking_df['z'] = tracking_df.groupby(['jerseyNum','teamGame'])['z'].ffill()

#define milissecond pace of callback
ms_pace = int((1/games_df['fps'])*1000)*3

#integrating tracking data to games and lineups df
full_df = pd.merge(tracking_df,
                   games_lineups_df,
                   on = ['jerseyNum','teamGame'],
                   how = 'left')

#deleting dfs for saving data
del tracking_df
del games_lineups_df

#getting primary color of the team
full_df['primaryColor'] = np.where(full_df['teamGame'] == 'homePlayers',
                                        full_df['homeTeamKit.primaryColor'],
                                        np.where(full_df['teamGame'] == 'awayPlayers',
                                                 full_df['awayTeamKit.primaryColor'],
                                                 'black')
                                  )

full_df = full_df[['frameNum',
                   'videoTimeMs',
                   'player.nickname',
                   'jerseyNum',
                   'positionGroupType',
                   'visibility.raw',
                   'confidence.raw',
                   'teamGame',
                   'x',
                   'y',
                   'z',
                   'x_ball',
                   'y_ball',
                   'z_ball',
                   'primaryColor']]

#creating text for the hovertext
full_df['text_ttp'] = np.where(full_df['teamGame']=='balls',
                                "Frame:" + full_df["frameNum"].astype('str') + \
                                "<br>Ball" + \
                                "<br>Visibility:" + full_df["visibility.raw"],
                                "Frame:" + full_df["frameNum"].astype('str') + \
                                "<br>Player Name:" + full_df["player.nickname"] + \
                                "<br>Jersey Number:" + full_df["jerseyNum"].astype('str') + \
                                "<br>Position:" + full_df["positionGroupType"] + \
                                "<br>Visibility:" + full_df["visibility.raw"] + \
                                "<br>Confidence:" + full_df["confidence.raw"]
)


#getting video playlist url
video = f'https://d293djmf54wuo5.cloudfront.net/{video_id}/playlist.m3u8'

#building dash
tactical = dash.Dash(__name__,
                     title = 'Tactical Analysis',
                     update_title=None,
                     external_stylesheets=[dbc.themes.BOOTSTRAP])

#defining layout
tactical.layout = dbc.Row(
    children=[
        dbc.Row(dcc.Markdown(f'## {homeTeamName} vs {awayTeamName}', style={'textAlign': 'center'})),
        dbc.Row(
            justify='center',
            children=[
        dbc.Col(
            dash_player.DashPlayer(id='video-player',
                                    url=video,
                                    controls=True,
                                    muted=True,
                                    width='100%',
                                    height='100%',
                                    playsinline=True),
                ),
        dbc.Col(
            dcc.Graph(id='mean_chart',
                      figure=go.Figure(
                          data=[],
                          layout=go.Layout(
                                        #showlegend=False,
                                        margin=dict(l=0, r=0, b=0, t=0),
                                        xaxis=dict(range=xaxis_range,
                                                    autorange=False,
                                                    tickmode='array',
                                                    tickvals=np.arange(xaxis_range[0]+10, xaxis_range[0]-9, 5).tolist(),
                                                    showticklabels=False),
                                        yaxis=dict(range=yaxis_range,
                                                    autorange=False,
                                                    showgrid=False,
                                                    showticklabels=False),
                                        plot_bgcolor='#00FF00',
                                        shapes=drawPitch(x=pitch_length,
                                                         y=pitch_width,
                                                         num_zones_x=6,
                                                         num_zones_y=4)
                                        )
                                    )
            )
        )
        ]
        ),
        dbc.Row(),
    ]
)

#interaction to update current time
@tactical.callback(
    Output('video-player', 'intervalCurrentTime'),
    [Input('video-player', 'currentTime')])
def update_intervalCurrentTime(value):
    return ms_pace

# interaction to update field graph
@tactical.callback(
    Output(component_id='mean_chart', component_property='figure'),
    [Input(component_id='video-player', component_property='currentTime')],
    [State('mean_chart', 'figure')]
)
def update_graph(sec, fig):

    sec = sec if sec is not None else 0
    milisec = sec * 1000  # dash_player returns time in seconds, but the data is in milliseconds, so we need to convert it

    frame_df = full_df[full_df['videoTimeMs'].between(milisec-ms_pace, milisec)]
    frame_df = frame_df[frame_df['videoTimeMs']==frame_df['videoTimeMs'].max()]

    frame_df['x_int'] = frame_df['x'].astype(int)
    frame_df['y_int'] = frame_df['y'].astype(int)

    field_frame = pd.merge(field_grid,
                           frame_df[frame_df['teamGame']=='balls'][['x_int','y_int','x_ball','y_ball']],
                           on = ['x_int','y_int'],
                           how = 'left')

    field_frame['x_ball'] = field_frame['x_ball'].fillna(field_frame['x_ball'].max())
    field_frame['y_ball'] = field_frame['y_ball'].fillna(field_frame['y_ball'].max())

    field_frame['distance_to_ball'] = np.sqrt((field_frame['x_int'] - field_frame['x_ball'])**2 + (field_frame['y_int'] - field_frame['y_ball'])**2)
    field_frame['pass_probability'] = 1 - (field_frame['distance_to_ball'] / np.sqrt(pitch_length**2 + pitch_width**2))

    for goal, _ in goal_positions.items():
        field_frame[f'pass_value_{goal}_goal'] = field_frame['pass_probability'] * field_frame[f'space_value_{goal}_goal']

    field_frame['pass_value'] = field_frame['pass_value_left_goal'] - field_frame['pass_value_right_goal']

    field_frame = field_frame[['x_int','y_int','pass_value']]

    fig['data'] = [go.Heatmap(z=field_frame['pass_value'].values.reshape(((pitch_length + 1), (pitch_width + 1))).T,
                              x=field_frame['x_int'].unique(),
                              y=field_frame['y_int'].unique(),
                              colorscale='RdBu_r',
                              colorbar=dict(title='Pass Value'),
                              zmin=-1,
                              zmax=1,
                              showscale=True)
                  ] + \
                  [go.Scatter(x = team_df["x"],
                              y = team_df["y"],
                              mode = 'markers',
                              marker_size = 15 if team != 'balls' else 10,
                              marker_color = team_df["primaryColor"],
                              name = team,
                              hovertext = team_df["text_ttp"],
                              hoverinfo = "text"
                              )
                   for team, team_df in frame_df.groupby('teamGame')]

    return fig

#running app
if __name__ == '__main__':
    tactical.run()