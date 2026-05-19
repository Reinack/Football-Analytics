import streamlit as st

st.set_page_config(
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚽ Football Analytics Dashboard")
st.markdown("Análisis de datos de las **5 principales ligas europeas** — temporadas **2014 a 2020**.")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Partidos", "12,680")
col2.metric("Jugadores", "7,659")
col3.metric("Tiros", "324,543")
col4.metric("Apariciones", "356,513")

st.divider()

st.markdown("""
### Ligas cubiertas
| Bandera | Liga | País |
|---------|------|------|
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 | Premier League | Inglaterra |
| 🇮🇹 | Serie A | Italia |
| 🇩🇪 | Bundesliga | Alemania |
| 🇪🇸 | La Liga | España |
| 🇫🇷 | Ligue 1 | Francia |

### Preguntas analizadas
Navegá por el menú lateral para explorar cada análisis:

| # | Pregunta |
|---|----------|
| 1 | Distribución de tarjetas amarillas por posición |
| 2 | Dónde anota el mejor goleador de una temporada |
| 3 | Mapa de ciudades ganadoras de torneos |
| 4 | Mapa de ciudades con más partidos |
| 5 | Evolución de faltas a lo largo del tiempo |
| 6 | Mejores jugadores en situaciones de balón parado |
| 7 | Equipos más dominantes jugando de visitante |
| 8 | Equipos que generan más tiros al arco |
""")
