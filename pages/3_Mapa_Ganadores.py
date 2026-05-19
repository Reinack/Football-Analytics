import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import streamlit.components.v1 as components
import folium
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Mapa Ganadores", page_icon="🏆", layout="wide")
st.title("🏆 Ciudades Campeonas")
st.caption("Ciudades que acumularon más títulos entre 2014 y 2020. Círculos más grandes = más campeonatos.")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

# Season standings
seasons_df = (
    teamstats.groupby(["teamID", "season"])
    .agg(gamesPlayed=("gameID", "count"), totalGoals=("goals", "sum"))
)
wins = teamstats[teamstats["result"] == "W"].groupby(["teamID", "season"]).size().rename("Wins")
draws = teamstats[teamstats["result"] == "D"].groupby(["teamID", "season"]).size().rename("Draws")
seasons_df = seasons_df.join(wins).join(draws).fillna(0)
seasons_df["Points"] = seasons_df["Wins"] * 3 + seasons_df["Draws"]
seasons_df = seasons_df.reset_index()

league_info = pd.concat([
    games[["homeTeamID", "season", "leagueID"]].rename(columns={"homeTeamID": "teamID"}),
    games[["awayTeamID", "season", "leagueID"]].rename(columns={"awayTeamID": "teamID"}),
]).drop_duplicates()

seasons_df = seasons_df.merge(league_info, on=["teamID", "season"], how="left")
seasons_df = seasons_df.merge(
    teams_with_geo[["teamID", "name", "city", "longitude", "latitude"]], on="teamID", how="left"
)
seasons_df = seasons_df.merge(
    leagues[["leagueID", "name"]].rename(columns={"name": "League"}), on="leagueID", how="left"
)

winners = (
    seasons_df.sort_values(["Points", "totalGoals"], ascending=False)
    .groupby(["leagueID", "season"])
    .first()
    .reset_index()
)

title_counts = (
    winners.groupby(["name", "city", "latitude", "longitude"])
    .size()
    .reset_index(name="titles")
    .dropna(subset=["latitude", "longitude"])
)

m = folium.Map(
    location=[title_counts["latitude"].mean(), title_counts["longitude"].mean()],
    zoom_start=4,
    tiles="CartoDB dark_matter",
)

for _, row in title_counts.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6 + row["titles"] * 5,
        popup=folium.Popup(
            f"<b>{row['name']}</b><br>{row['city']}<br>Títulos: {row['titles']}",
            max_width=200,
        ),
        tooltip=f"{row['name']} — {int(row['titles'])} título(s)",
        color="gold",
        fill=True,
        fill_color="gold",
        fill_opacity=0.7,
        weight=2,
    ).add_to(m)

components.html(m._repr_html_(), height=600)

with st.expander("Ver tabla de ganadores por temporada"):
    display = (
        winners[["League", "season", "name", "city", "Points", "totalGoals"]]
        .rename(columns={
            "League": "Liga", "season": "Temporada", "name": "Equipo",
            "city": "Ciudad", "Points": "Puntos", "totalGoals": "Goles",
        })
        .sort_values(["Liga", "Temporada"])
    )
    st.dataframe(display, use_container_width=True, hide_index=True)
