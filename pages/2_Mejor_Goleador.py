import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import plotly.graph_objects as go
from data_loader import load_data
from utils import add_football_field_scatter

st.set_page_config(page_title="Mejor Goleador", page_icon="🎯", layout="wide")
st.title("🎯 Dónde Anota el Mejor Goleador")
st.caption("Posiciones exactas de cada gol del máximo anotador de la temporada seleccionada")

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

games_f = games[(games["season"] == season) & (games["leagueID"] == league_id)]
shots_f = shots[shots["gameID"].isin(games_f["gameID"])]
goals = shots_f[shots_f["shotResult"] == "Goal"]

if goals.empty:
    st.warning("No hay goles registrados para los filtros seleccionados.")
    st.stop()

goals_count = goals.groupby("shooterID").size()
top_id = goals_count.idxmax()
total_goals = int(goals_count.max())

name_match = players.loc[players["playerID"] == top_id, "name"].values
player_name = name_match[0] if len(name_match) > 0 else f"Jugador #{top_id}"

player_goals = goals[goals["shooterID"] == top_id].copy()
player_goals["x"] = player_goals["positionX"] * 105
player_goals["y"] = player_goals["positionY"] * 68

col1, col2, col3 = st.columns(3)
col1.metric("Goleador", player_name)
col2.metric("Goles", total_goals)
col3.metric("Liga", league_map[league_id])

fig = go.Figure()
add_football_field_scatter(fig)

fig.add_trace(
    go.Scatter(
        x=player_goals["x"],
        y=player_goals["y"],
        mode="markers",
        marker=dict(
            size=14,
            color="red",
            opacity=0.75,
            line=dict(color="darkred", width=1.5),
        ),
        customdata=player_goals[["minute", "situation"]].values,
        hovertemplate=(
            "Minuto: %{customdata[0]}<br>"
            "Situación: %{customdata[1]}<extra></extra>"
        ),
    )
)

fig.update_layout(
    title=dict(
        text=f"Goles de {player_name} — {league_map[league_id]} {season}",
        font=dict(size=18),
    ),
    showlegend=False,
    margin=dict(l=10, r=10, t=60, b=10),
)

st.plotly_chart(fig)
st.caption("Cada punto rojo representa un gol. Pasá el cursor para ver el minuto y situación.")
