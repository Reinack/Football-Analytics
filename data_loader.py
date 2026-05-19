import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    games = pd.read_csv("Clean/games.csv")
    shots = pd.read_csv("Clean/shots.csv")
    players = pd.read_csv("Clean/players.csv")
    teams = pd.read_csv("Clean/teams.csv")
    teamstats = pd.read_csv("Clean/teamstats.csv")
    leagues = pd.read_csv("Clean/leagues.csv")
    appearances = pd.read_csv("Clean/appearances.csv")
    teams_with_geo = pd.read_csv("Clean/teams_with_geo.csv")
    positions = pd.read_csv("Clean/positions.csv")
    return games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions
