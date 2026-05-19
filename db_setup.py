"""
One-time script to create tables in Neon and load data from the Clean/ CSVs.

Usage:
    DATABASE_URL=<neon-connection-string> python db_setup.py
"""

import os

import pandas as pd
from sqlalchemy import create_engine

TABLES = {
    "games": "Clean/games.csv",
    "shots": "Clean/shots.csv",
    "players": "Clean/players.csv",
    "teams": "Clean/teams.csv",
    "teamstats": "Clean/teamstats.csv",
    "leagues": "Clean/leagues.csv",
    "appearances": "Clean/appearances.csv",
    "teams_with_geo": "Clean/teams_with_geo.csv",
    "positions": "Clean/positions.csv",
}


def main():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("Set DATABASE_URL before running this script.")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(url)

    for table, csv_path in TABLES.items():
        print(f"Loading {csv_path} → {table} ...", end=" ", flush=True)
        df = pd.read_csv(csv_path)
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"done ({len(df):,} rows)")

    print("All tables loaded successfully.")


if __name__ == "__main__":
    main()
