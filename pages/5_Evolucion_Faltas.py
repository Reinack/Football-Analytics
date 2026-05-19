import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Evolución de Faltas", page_icon="📈", layout="wide")
st.title("📈 Evolución de Faltas por Liga")
st.caption("Promedio de faltas por partido, por liga y temporada")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

merged = teamstats[["gameID", "season", "fouls"]].merge(games[["gameID", "leagueID"]], on="gameID")
grouped = merged.groupby(["leagueID", "season"])
fouls_avg = (grouped["fouls"].sum() / grouped["gameID"].nunique()).reset_index()
fouls_avg.columns = ["leagueID", "season", "fouls_per_game"]
result = fouls_avg.merge(leagues[["leagueID", "name"]], on="leagueID")

fig = px.line(
    result,
    x="season",
    y="fouls_per_game",
    color="name",
    markers=True,
    labels={"season": "Temporada", "fouls_per_game": "Faltas por partido", "name": "Liga"},
    title="Promedio de Faltas por Partido — Evolución por Liga",
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig.update_traces(line=dict(width=2.5), marker=dict(size=9))
fig.update_layout(
    height=520,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver datos por temporada"):
    pivot = result.pivot(index="season", columns="name", values="fouls_per_game").round(2)
    st.dataframe(pivot, use_container_width=True)
