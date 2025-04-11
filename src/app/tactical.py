"""Tactical analysis app for visualizing football tracking data."""

import time
import numpy as np
import pandas as pd
import dash
from dash import dcc, Patch
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_player

from utils.io.io import read_parquet
from utils.plots.pitch import drawPitch


# Constants
GAME_ID = 10510
DATA_PATH = "data/cleaned"
FPS_SCALE = 3
PROFILING = True


def load_data(game_id):
    """Load tracking, game, and lineup data."""
    tracking = read_parquet(path=f"{DATA_PATH}/tracking/{game_id}.parquet")
    game = read_parquet(path=f"{DATA_PATH}/games/{game_id}.parquet")
    lineup = read_parquet(path=f"{DATA_PATH}/lineups/{game_id}.parquet")
    return tracking, game, lineup


def process_field_grid(pitch_length, pitch_width):
    """Create a field grid with distance and space value calculations."""
    x_coords = pd.DataFrame({"x_int": np.arange(0, pitch_length + 1)})
    y_coords = pd.DataFrame({"y_int": np.arange(0, pitch_width + 1)})
    x_coords["foo"] = 1
    y_coords["foo"] = 1

    field_grid = pd.merge(x_coords, y_coords, on="foo").drop("foo", axis=1)

    goal_positions = {
        "left": (0, pitch_width / 2),
        "right": (pitch_length, pitch_width / 2),
    }

    for goal, (goal_x, goal_y) in goal_positions.items():
        dist_col = f"distance_to_{goal}_goal"
        value_col = f"space_value_{goal}_goal"
        field_grid[dist_col] = np.sqrt(
            (field_grid["x_int"] - goal_x) ** 2 + (field_grid["y_int"] - goal_y) ** 2
        )
        field_grid[value_col] = 1 - (field_grid[dist_col] / field_grid[dist_col].max())

    return field_grid


def prepare_tracking_data(tracking, pitch_length, pitch_width, fps):
    """Prepare tracking data for visualization."""
    tracking["x"] = tracking["x.raw"] + pitch_length / 2
    tracking["y"] = tracking["y.raw"] + pitch_width / 2
    tracking["z"] = tracking["z.raw"]

    for coord in ["x", "y", "z"]:
        ball_col = f"{coord}_ball"
        tracking[ball_col] = np.where(
            tracking["teamGame"] == "balls", tracking[coord], np.nan
        )
        tracking[ball_col] = tracking.groupby("frameNum")[ball_col].transform("max")
        tracking[ball_col] = tracking.groupby(["jerseyNum", "teamGame"])[
            ball_col
        ].ffill()

        tracking[coord] = tracking.groupby(["jerseyNum", "teamGame"])[coord].ffill()

    return tracking, int((1 / fps) * 1000) * FPS_SCALE


def build_app():
    """Build the Dash app for tactical analysis."""
    tracking_df, games_df, lineups_df = load_data(GAME_ID)

    video_id = games_df["videoUrl"].iloc[0].split("/")[-1]
    video_url = f"https://d293djmf54wuo5.cloudfront.net/{video_id}/playlist.m3u8"

    pitch_length = games_df["stadium.pitches.length"].iloc[0]
    pitch_width = games_df["stadium.pitches.width"].iloc[0]

    home_team = games_df["homeTeam.name"].iloc[0]
    away_team = games_df["awayTeam.name"].iloc[0]

    field_grid = process_field_grid(pitch_length, pitch_width)

    lineups_df = pd.merge(lineups_df, games_df, on="game.id")
    lineups_df["teamGame"] = np.where(
        lineups_df["team.id"] == lineups_df["homeTeam.id"],
        "homePlayers",
        "awayPlayers",
    )

    lineups_df = lineups_df[
        [
            "teamGame",
            "jerseyNum",
            "player.id",
            "player.nickname",
            "positionGroupType",
            "homeTeamKit.primaryColor",
            "awayTeamKit.primaryColor",
        ]
    ]

    tracking_df, ms_pace = prepare_tracking_data(
        tracking_df,
        pitch_length=pitch_length,
        pitch_width=pitch_width,
        fps=games_df["fps"].iloc[0],
    )

    merged_df = pd.merge(
        tracking_df, lineups_df, on=["jerseyNum", "teamGame"], how="left"
    )

    merged_df["primaryColor"] = np.where(
        merged_df["teamGame"] == "homePlayers",
        merged_df["homeTeamKit.primaryColor"],
        np.where(
            merged_df["teamGame"] == "awayPlayers",
            merged_df["awayTeamKit.primaryColor"],
            "black",
        ),
    )

    merged_df["x_int"] = merged_df["x"].astype(int)
    merged_df["y_int"] = merged_df["y"].astype(int)

    merged_df["text_ttp"] = np.where(
        merged_df["teamGame"] == "balls",
        "Frame:"
        + merged_df["frameNum"].astype(str)
        + "<br>Ball<br>Visibility:"
        + merged_df["visibility.raw"],
        "Frame:"
        + merged_df["frameNum"].astype(str)
        + "<br>Player Name:"
        + merged_df["player.nickname"]
        + "<br>Jersey Number:"
        + merged_df["jerseyNum"].astype(str)
        + "<br>Position:"
        + merged_df["positionGroupType"]
        + "<br>Visibility:"
        + merged_df["visibility.raw"]
        + "<br>Confidence:"
        + merged_df["confidence.raw"],
    )

    # casting ms to the ms_pace to reduce dataframe
    merged_df["videoTimeMs"] = merged_df["videoTimeMs"].astype(int)
    merged_df["videoTimeMs"] = merged_df["videoTimeMs"] // ms_pace * ms_pace

    # getting only the last frame of each videoTimeMs period
    merged_df["maxFrameMs"] = merged_df.groupby(["videoTimeMs"])["frameNum"].transform(
        "max"
    )
    merged_df = merged_df[merged_df["frameNum"] == merged_df["maxFrameMs"]].drop(
        columns=["maxFrameMs"]
    )

    # Set up efficient lookup using index
    merged_df = merged_df.set_index("videoTimeMs")

    app = dash.Dash(
        __name__,
        title="Tactical Analysis",
        update_title=None,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    # Initialize throttling variables
    last_frame = {"id": None}
    last_ball_pos = {"x": None, "y": None}

    field_layout = go.Layout(
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        xaxis={"range": [0, pitch_length], "autorange": False, "showticklabels": False},
        yaxis={"range": [0, pitch_width], "autorange": False, "showticklabels": False},
        plot_bgcolor="#00FF00",
        shapes=drawPitch(x=pitch_length, y=pitch_width, num_zones_x=6, num_zones_y=4),
    )

    app.layout = dbc.Row(
        [
            dbc.Row(
                dcc.Markdown(
                    f"## {home_team} vs {away_team}", style={"textAlign": "center"}
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dash_player.DashPlayer(
                            id="video-player",
                            url=video_url,
                            controls=True,
                            muted=True,
                            width="100%",
                            height="100%",
                            playsinline=True,
                        )
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="mean_chart",
                            figure=go.Figure(data=[], layout=field_layout),
                        )
                    ),
                ]
            ),
        ]
    )

    @app.callback(
        Output("video-player", "intervalCurrentTime"),
        Input("video-player", "currentTime"),
    )
    def set_video_interval(_):
        return ms_pace

    @app.callback(Output("mean_chart", "figure"), Input("video-player", "currentTime"))
    def update_figure(current_time):

        if PROFILING:
            start = time.perf_counter()  # ⏱️ Start timing

        nonlocal last_frame

        # Avoid updates when time_pace is lower then the ms_pace
        current_time = current_time or 0
        frame_number = int((current_time * 1000) // ms_pace) * ms_pace

        if frame_number == last_frame["id"]:
            raise dash.exceptions.PreventUpdate
        last_frame["id"] = frame_number

        try:
            frame_df = merged_df.loc[frame_number]
        except KeyError:
            raise dash.exceptions.PreventUpdate

        # If only one row was returned, make sure it's treated as a DataFrame
        if isinstance(frame_df, pd.Series):
            frame_df = frame_df.to_frame().T

        if frame_df.empty:
            raise dash.exceptions.PreventUpdate

        # Check if the ball data is present
        # If not, raise PreventUpdate to skip the callback
        ball_data = frame_df[frame_df["teamGame"] == "balls"]
        if ball_data.empty:
            raise dash.exceptions.PreventUpdate

        x_ball = ball_data["x_ball"].dropna().values[0]
        y_ball = ball_data["y_ball"].dropna().values[0]

        if last_ball_pos["x"] is not None:
            # Check if the ball has moved significantly
            # If it has, update the last ball position
            # If not, skip recalculation
            if (
                abs(x_ball - last_ball_pos["x"]) > 0.5
                or abs(y_ball - last_ball_pos["y"]) > 0.5
            ):
                # recalculate pass map
                last_ball_pos["x"], last_ball_pos["y"] = x_ball, y_ball
            else:
                # skip recalculation
                raise dash.exceptions.PreventUpdate

        grid_x = field_grid["x_int"].values
        grid_y = field_grid["y_int"].values

        dx = grid_x - x_ball
        dy = grid_y - y_ball
        distances = np.sqrt(dx**2 + dy**2)
        max_dist = np.max(distances) or 1
        pass_prob = 1 - (distances / max_dist)

        # Switch the scattertype based on the number of points
        # Use Scattergl for larger datasets for better performance
        scatter_type = go.Scatter if len(frame_df) < 100 else go.Scattergl

        # Create the scatter plot for the ball and players
        # Using Patch to update only the data, not the entire figure
        patch = Patch()
        patch["data"] = [
            go.Heatmap(
                z=pass_prob.reshape((pitch_length + 1, pitch_width + 1)).T,
                x=field_grid["x_int"].unique(),
                y=field_grid["y_int"].unique(),
                colorscale="RdYlGn_r",
                colorbar={"title": "Pass Value"},
                zmin=0,
                zmax=1,
                showscale=True,
            )
        ] + [
            scatter_type(
                x=df["x"],
                y=df["y"],
                mode="markers",
                marker_size=15 if team != "balls" else 10,
                marker_color=df["primaryColor"],
                name=team,
                hovertext=df["text_ttp"],
                hoverinfo="text",
            )
            for team, df in frame_df.groupby("teamGame")
        ]

        # Profiling response time
        if PROFILING:
            end = time.perf_counter()  # ⏱️ End timing
            exec_time_ms = (end - start) * 1000
            print(
                f"update_figure executed in {exec_time_ms:.2f} ms for frame {frame_number}"
            )

        return patch

    return app


if __name__ == "__main__":
    build_app().run()
