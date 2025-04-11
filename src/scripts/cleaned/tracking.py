"""Preprocess tracking data from JSON files and save as Parquet."""
import joblib
import pandas as pd
from utils.io.io import glob, read_json, to_parquet


def preprocess_json_column(
    df: pd.DataFrame, column: str, mode: str = "Smoothed"
) -> pd.DataFrame:

    """
    Preprocess a JSON column in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the JSON column.
        column (str): Name of the JSON column to preprocess.
        mode (str): Mode for preprocessing. Default is "Smoothed".

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """

    if column != "ballsSmoothed":
        df_players = df.explode(column).reset_index(drop=True)
    else:
        df_players = df

    df_players = pd.concat(
        [df_players["frameNum"], pd.json_normalize(df_players[column])], axis=1
    )

    if "Players" in column:
        df_players = df_players.dropna(subset=["jerseyNum"])

    df_players["teamGame"] = column
    df_players["smooth_mode"] = mode

    return df_players


def preprocess_tracking_data(path: str) -> None:

    """
    Preprocess tracking data from a JSON file and save as Parquet.

    Args:
        path (str): Path to the JSON file.
    """

    game_id = path.split("/")[-1].split(".")[0]

    print(f"Reading {game_id}...")

    tracking = read_json(path, lines=True, engine="pyarrow")
    tracking = tracking.drop_duplicates(subset=["frameNum"])

    columns = ["homePlayers", "awayPlayers", "balls"]
    modes = ["Raw"]

    print("Read each column data in parallel")

    df_full = joblib.Parallel(n_jobs=3)(
        joblib.delayed(preprocess_json_column)(
            tracking[["frameNum", column]], column, mode
        )
        for column in columns
        for mode in modes
    )

    df_full = pd.concat(df_full, ignore_index=True)

    time_cols = [
        "frameNum",
        "videoTimeMs",
        "period",
        "periodElapsedTime",
        "periodGameClockTime",
    ]

    df_full["game.id"] = game_id

    df_full["jerseyNum"] = df_full["jerseyNum"].fillna(-1).astype("int")

    df_full = df_full.reset_index(drop=True)

    index = ["game.id", "frameNum", "teamGame", "jerseyNum", "smooth_mode"]

    df_full = df_full.set_index(index)[
        ["visibility", "confidence", "x", "y", "z"]
    ].unstack("smooth_mode")

    df_full.columns = [".".join(col).lower() for col in df_full.columns]

    df_full = df_full.reset_index()

    df_full = df_full.merge(tracking[time_cols], on=["frameNum"], how="left")

    df_full["z.raw"] = df_full["z.raw"].fillna(0)

    to_parquet(data=df_full, path=f"data/cleaned/tracking/{game_id}.parquet")

    del tracking
    del df_full

    print(f"Tracking data for game {game_id} has been preprocessed")


if __name__ == "__main__":

    for file_unit in glob("data/raw/tracking/*.jsonl.bz2"):
        preprocess_tracking_data(file_unit)
