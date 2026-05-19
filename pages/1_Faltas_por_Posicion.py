import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data_loader import load_data
from utils import add_football_field

st.set_page_config(page_title="Faltas por Posición", page_icon="🟨", layout="wide")
st.title("🟨 Faltas por Posición")
st.caption("Tarjetas amarillas por cada 100 apariciones, según posición en el campo")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

with st.sidebar:
    st.header("Filtros")
    season = st.selectbox("Temporada", sorted(games["season"].unique(), reverse=True))

    league_ids = games[games["season"] == season]["leagueID"].unique()
    league_map = (
        leagues[leagues["leagueID"].isin(league_ids)]
        .set_index("leagueID")["name"]
        .to_dict()
    )
    league_id = st.selectbox("Liga", list(league_map.keys()), format_func=lambda x: league_map[x])

    mask = (games["leagueID"] == league_id) & (games["season"] == season)
    team_ids = pd.concat([games[mask]["homeTeamID"], games[mask]["awayTeamID"]]).unique()
    team_map = (
        teams[teams["teamID"].isin(team_ids)]
        .sort_values("name")
        .set_index("teamID")["name"]
        .to_dict()
    )
    team_id = st.selectbox("Equipo", list(team_map.keys()), format_func=lambda x: team_map[x])

game_ids = games[
    (games["leagueID"] == league_id)
    & (games["season"] == season)
    & ((games["homeTeamID"] == team_id) | (games["awayTeamID"] == team_id))
]["gameID"].unique()

app_f = appearances[appearances["gameID"].isin(game_ids)]

if app_f.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

yellow = app_f.groupby("position")["yellowCard"].sum().reset_index()
count = app_f.groupby("position").size().reset_index(name="apps")
result = yellow.merge(count, on="position")
result["yellowCard"] = result["yellowCard"].astype(int)
result["per100"] = (result["yellowCard"] * 100 / result["apps"]).round(1)
end = pd.merge(result, positions, on="position", how="inner")

fig = go.Figure()
add_football_field(fig)

fig.add_trace(
    go.Scatter(
        x=end["X"],
        y=end["Y"],
        mode="markers+text",
        marker=dict(size=42, color="gold", opacity=0.9, line=dict(color="darkgoldenrod", width=2)),
        text=end["per100"].astype(str),
        textposition="middle center",
        textfont=dict(size=11, color="black", family="Arial Black"),
        customdata=end[["position", "yellowCard", "apps", "per100"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Total amarillas: %{customdata[1]}<br>"
            "Apariciones: %{customdata[2]}<br>"
            "Por 100 juegos: %{customdata[3]}<extra></extra>"
        ),
    )
)

fig.update_layout(
    title=dict(text=f"{team_map[team_id]} — Temporada {season}", font=dict(size=18)),
    showlegend=False,
    height=520,
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(fig, use_container_width=True)
st.caption("El número en cada posición indica las tarjetas amarillas por cada 100 apariciones.")

with st.expander("Ver tabla de datos"):
    st.dataframe(
        end[["position", "yellowCard", "apps", "per100"]]
        .rename(columns={
            "position": "Posición",
            "yellowCard": "Total Amarillas",
            "apps": "Apariciones",
            "per100": "Amarillas / 100 juegos",
        })
        .sort_values("Amarillas / 100 juegos", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
