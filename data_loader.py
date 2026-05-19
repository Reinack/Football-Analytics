import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


def _get_engine():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    # Neon provides postgres:// URIs; SQLAlchemy 2.x requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return create_engine(url)


@st.cache_data
def load_data():
    engine = _get_engine()
    with engine.connect() as conn:
        games = pd.read_sql("SELECT * FROM games", conn)
        shots = pd.read_sql("SELECT * FROM shots", conn)
        players = pd.read_sql("SELECT * FROM players", conn)
        teams = pd.read_sql("SELECT * FROM teams", conn)
        teamstats = pd.read_sql("SELECT * FROM teamstats", conn)
        leagues = pd.read_sql("SELECT * FROM leagues", conn)
        appearances = pd.read_sql("SELECT * FROM appearances", conn)
        teams_with_geo = pd.read_sql("SELECT * FROM teams_with_geo", conn)
        positions = pd.read_sql("SELECT * FROM positions", conn)
    return games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions
