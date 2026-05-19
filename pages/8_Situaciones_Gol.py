import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Situaciones de Gol", page_icon="🎯", layout="wide")
st.title("🎯 Equipos que Generan más Tiros al Arco")
st.caption("Top 10 por liga — mejor promedio de tiros al arco en su mejor temporada")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

with st.sidebar:
    st.header("Filtros")
    all_leagues = leagues["name"].tolist()
    selected_leagues = st.multiselect("Ligas a mostrar", all_leagues, default=all_leagues)
    top_n = st.slider("Equipos por liga", min_value=5, max_value=15, value=10)

ts = teamstats.merge(teams[["teamID", "name"]], on="teamID")
ts = ts.merge(games[["gameID", "leagueID"]], on="gameID")
avg = (
    ts.groupby(["leagueID", "teamID", "season", "name"])["shotsOnTarget"]
    .mean()
    .reset_index()
)
avg = avg.merge(leagues[["leagueID", "name"]].rename(columns={"name": "League"}), on="leagueID")
avg = avg.rename(columns={"name": "team_name"})

best = avg.loc[avg.groupby("teamID")["shotsOnTarget"].idxmax()].sort_values(
    ["leagueID", "shotsOnTarget"], ascending=[True, False]
)

filtered = best[best["League"].isin(selected_leagues)]
if filtered.empty:
    st.warning("Seleccioná al menos una liga.")
    st.stop()

top_per_league = pd.concat([
    group.nlargest(top_n, "shotsOnTarget")
    for _, group in filtered.groupby("League")
]).reset_index(drop=True)
top_per_league["shotsOnTarget"] = top_per_league["shotsOnTarget"].round(2)

n = len(top_per_league["League"].unique())
cols = min(n, 2)

fig = px.bar(
    top_per_league,
    x="shotsOnTarget",
    y="team_name",
    facet_col="League",
    facet_col_wrap=cols,
    orientation="h",
    color="shotsOnTarget",
    color_continuous_scale="Blues",
    text="shotsOnTarget",
    labels={"shotsOnTarget": "Prom. Tiros al Arco", "team_name": ""},
    title=f"Top {top_n} Equipos por Liga — Mayor Promedio de Tiros al Arco",
)
fig.update_traces(texttemplate="%{x:.1f}", textposition="outside")
fig.update_yaxes(matches=None)
fig.update_layout(
    height=max(400, top_n * 45 * ((n + cols - 1) // cols)),
    showlegend=False,
    coloraxis_showscale=False,
)

st.plotly_chart(fig, use_container_width=True)
