import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import streamlit.components.v1 as components
import folium
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Mapa de Partidos", page_icon="🗺️", layout="wide")
st.title("🗺️ Dónde se Juegan más Partidos")
st.caption("Ciudades con mayor cantidad de partidos locales (2014-2020). Círculos más grandes = más partidos.")

games, shots, players, teams, teamstats, leagues, appearances, teams_with_geo, positions = load_data()

games_local = games.rename(columns={"homeTeamID": "teamID"})
merged = pd.merge(
    games_local,
    teams_with_geo[["teamID", "city", "longitude", "latitude"]],
    on="teamID",
    how="left",
)

city_count = merged["city"].value_counts().reset_index()
city_count.columns = ["city", "num_matches"]
city_coords = merged[["city", "latitude", "longitude"]].drop_duplicates(subset="city")
city_count = city_count.merge(city_coords, on="city", how="left").dropna(
    subset=["latitude", "longitude"]
)

m = folium.Map(
    location=[city_count["latitude"].mean(), city_count["longitude"].mean()],
    zoom_start=4,
    tiles="CartoDB positron",
)

max_matches = city_count["num_matches"].max()
for _, row in city_count.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5 + 22 * (row["num_matches"] / max_matches),
        popup=folium.Popup(
            f"<b>{row['city']}</b><br>Partidos: {row['num_matches']}",
            max_width=200,
        ),
        tooltip=f"{row['city']}: {int(row['num_matches'])} partidos",
        color="crimson",
        fill=True,
        fill_color="crimson",
        fill_opacity=0.6,
        weight=2,
    ).add_to(m)

components.html(m._repr_html_(), height=600)

with st.expander("Ver datos por ciudad"):
    st.dataframe(
        city_count[["city", "num_matches"]]
        .rename(columns={"city": "Ciudad", "num_matches": "Partidos"})
        .sort_values("Partidos", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
