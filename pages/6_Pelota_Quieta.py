import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Pelota Quieta", page_icon="⚽", layout="wide")
st.title("⚽ Especialistas en Balón Parado")
st.caption("Top 6 jugadores con más goles + asistencias en corners, tiros libres y penales")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

with st.sidebar:
    st.header("Filtros")
    n_players = st.slider("Número de jugadores a mostrar", min_value=3, max_value=10, value=6)

situations = ["FromCorner", "SetPiece", "Penalty", "DirectFreekick", "DirectFreeKick"]
goals_sp = shots[
    shots["situation"].isin(situations) & (shots["shotResult"] == "Goal")
].drop_duplicates()

score = goals_sp[["gameID", "shooterID"]].rename(columns={"shooterID": "playerID"})
assist = (
    goals_sp[goals_sp["assisterID"] != -1][["gameID", "assisterID"]]
    .rename(columns={"assisterID": "playerID"})
)
assist["playerID"] = assist["playerID"].astype(int)

total = pd.concat([score, assist])
total = total.merge(games[["gameID", "season"]], on="gameID")
total_contrib = total.groupby(["playerID", "season"]).size().reset_index(name="contributions")

top_ids = (
    total_contrib.groupby("playerID")["contributions"].sum()
    .nlargest(n_players)
    .index
)
top_contrib = total_contrib[total_contrib["playerID"].isin(top_ids)]
top_contrib = top_contrib.merge(players[["playerID", "name"]], on="playerID")

fig = px.line(
    top_contrib,
    x="season",
    y="contributions",
    color="name",
    markers=True,
    labels={"season": "Temporada", "contributions": "Goles + Asistencias", "name": "Jugador"},
    title=f"Top {n_players} — Participaciones en Goles de Balón Parado",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_traces(line=dict(width=2.5), marker=dict(size=9))
fig.update_layout(
    height=520,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver totales por jugador"):
    totals = (
        top_contrib.groupby("name")["contributions"]
        .sum()
        .reset_index()
        .rename(columns={"name": "Jugador", "contributions": "Total Contribuciones"})
        .sort_values("Total Contribuciones", ascending=False)
    )
    st.dataframe(totals, use_container_width=True, hide_index=True)
