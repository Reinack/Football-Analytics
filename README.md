# Top 5 Ligas Europeas — Football Analytics

## Descripción
Análisis, limpieza y visualización interactiva de datos de fútbol de las 5 principales ligas europeas (2014–2020), utilizando Python, Streamlit y Tableau.

## Demo

🚀 **[Ver app en Streamlit]([https://bigdata-futbol.streamlit.app](https://bigdata-futbol-n8apt5auubtppwdpfr2bmr.streamlit.app/))**

**[Ver app en Render](https://bigdata-futbol-wbri.onrender.com/)

📊 **[Dashboard en Tableau](https://public.tableau.com/app/profile/fernando.torrres/viz/fin_17211741220640/Dashboard4?publish=yes)**

## Tabla de Contenidos
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Datasets](#datasets)
3. [Preguntas de Investigación](#preguntas-de-investigación)
4. [Metodología y Herramientas](#metodología-y-herramientas)
5. [Cómo ejecutar localmente](#cómo-ejecutar-localmente)

## Estructura del Proyecto

```
├── app.py                    # Página de inicio (Streamlit)
├── data_loader.py            # Carga de datos con caché
├── utils.py                  # Campo de fútbol en Plotly
├── pages/
│   ├── 1_Faltas_por_Posicion.py
│   ├── 2_Mejor_Goleador.py
│   ├── 3_Mapa_Ganadores.py
│   ├── 4_Mapa_Partidos.py
│   ├── 5_Evolucion_Faltas.py
│   ├── 6_Pelota_Quieta.py
│   ├── 7_Equipos_Visitante.py
│   └── 8_Situaciones_Gol.py
├── Analisis.ipynb            # Limpieza de datos (original)
├── Preguntas.ipynb           # Análisis exploratorio (original)
├── Raw/                      # Datos crudos
└── Clean/                    # Datos procesados
```

## Datasets
El proyecto incluye 7 datasets en formato CSV, siendo los más relevantes `games`, `shots`, `teamstats` y `appearances`.

| Dataset | Filas | Descripción |
|---------|-------|-------------|
| `appearances` | 356.513 | Estadísticas individuales por jugador y partido |
| `shots` | 324.543 | Detalles de cada tiro: posición, tipo, resultado, xGoal |
| `games` | 12.680 | Resultados, probabilidades y cuotas de apuestas |
| `teamstats` | 25.360 | Métricas por equipo y partido (xGoals, PPDA, corners) |
| `players` | 7.659 | Catálogo de jugadores |
| `teams` | 146 | Catálogo de equipos con geolocalización |
| `leagues` | 5 | Premier League, Serie A, Bundesliga, La Liga, Ligue 1 |

## Preguntas de Investigación

| # | Pregunta | Visualización |
|---|----------|---------------|
| 1 | ¿Cómo se distribuyen las tarjetas amarillas por posición? | Campo de fútbol interactivo |
| 2 | ¿Dónde anota el mejor goleador de cada temporada? | Scatter sobre campo |
| 3 | ¿Qué ciudades ganaron más torneos? | Mapa Folium con burbujas |
| 4 | ¿En qué ciudades se juegan más partidos? | Mapa Folium proporcional |
| 5 | ¿Cómo evolucionaron las faltas por liga a lo largo del tiempo? | Líneas por temporada |
| 6 | ¿Quiénes son los mejores en pelota quieta? | Evolución temporal de contribuciones |
| 7 | ¿Qué equipos dominan jugando de visitante? | Barras horizontales |
| 8 | ¿Qué equipos generan más tiros al arco? | Facet por liga |

## Metodología y Herramientas

### App interactiva — Streamlit
- Reemplaza los `input()` del notebook por filtros interactivos (sidebar)
- Gráficos con **Plotly** (zoom, hover, tooltips)
- Mapas con **Folium** embebidos
- Caché de datos con `@st.cache_data` para carga eficiente

### Análisis exploratorio — JupyterLab
- Limpieza de nulos, duplicados y valores inconsistentes
- Exploración con `pandas` y visualizaciones con `matplotlib` / `seaborn`

### Dashboard — Tableau
- 2 gráficos de barras, 1 mapa y 1 histograma filtrado por liga

### Bibliotecas Python

| Biblioteca | Uso |
|-----------|-----|
| `pandas` | Manipulación y análisis de datos |
| `streamlit` | App web interactiva |
| `plotly` | Gráficos interactivos |
| `folium` | Mapas interactivos |
| `matplotlib` | Gráficos estáticos (notebook) |
| `seaborn` | Visualizaciones estadísticas (notebook) |
| `numpy` | Operaciones numéricas |
| `geopandas` | Datos geoespaciales (notebook) |

## Cómo ejecutar localmente

### Opción 1 — Docker (recomendado)

No requiere instalar Python ni dependencias.

```bash
git clone https://github.com/Reinack/BIGDATA-Futbol.git
cd BIGDATA-Futbol
docker build -t football-analytics .
docker run -p 8501:8501 football-analytics
```

Abrí `http://localhost:8501` en el navegador.

### Opción 2 — Python local

```bash
git clone https://github.com/Reinack/BIGDATA-Futbol.git
cd BIGDATA-Futbol
pip install -r requirements.txt
streamlit run app.py
```
