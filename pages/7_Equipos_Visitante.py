import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Equipos Visitante", page_icon="✈️", layout="wide")
st.title("✈️ Equipos Dominantes de Visitante")
st.caption("Porcentaje de puntos obtenidos sobre el total posible jugando de visitante (2014-2020)")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

with st.sidebar:
    st.header("Filtros")
    top_n = st.slider("Equipos a mostrar", min_value=10, max_value=30, value=20)
    all_leagues = leagues["name"].tolist()
    selected_leagues = st.multiselect("Ligas", all_leagues, default=all_leagues)

away = games[["gameID", "leagueID", "season", "awayTeamID", "awayGoals", "homeGoals"]].rename(
    columns={"awayTeamID": "teamID", "awayGoals": "goals", "homeGoals": "opp"}
)
perf = away.groupby(["leagueID", "teamID"]).agg(
    awayGames=("gameID", "count"), awayGoals=("goals", "sum")
)
away_wins = away[away["goals"] > away["opp"]].groupby(["leagueID", "teamID"]).size().rename("awayWins")
away_draws = away[away["goals"] == away["opp"]].groupby(["leagueID", "teamID"]).size().rename("awayDraws")
perf = perf.join(away_wins).join(away_draws).fillna(0)
perf["awayPoints"] = perf["awayWins"] * 3 + perf["awayDraws"]
perf["performance"] = (perf["awayPoints"] / (3 * perf["awayGames"]) * 100).round(1)
perf = perf.reset_index()

result = perf.merge(
    leagues[["leagueID", "name"]].rename(columns={"name": "Liga"}), on="leagueID"
)
result = result.merge(
    teams[["teamID", "name"]].rename(columns={"name": "Equipo"}), on="teamID"
)

filtered = result[result["Liga"].isin(selected_leagues)]
if filtered.empty:
    st.warning("Seleccioná al menos una liga.")
    st.stop()

top = filtered.nlargest(top_n, "performance").sort_values("performance")

fig = px.bar(
    top,
    x="performance",
    y="Equipo",
    color="Liga",
    orientation="h",
    text="performance",
    labels={"performance": "Puntos obtenidos (%)"},
    title=f"Top {top_n} Equipos por Rendimiento de Visitante",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
fig.update_layout(
    height=max(400, top_n * 28),
    uniformtext_minsize=10,
    legend_title="Liga",
    xaxis=dict(range=[0, 80]),
)

st.plotly_chart(fig, use_container_width=True)
