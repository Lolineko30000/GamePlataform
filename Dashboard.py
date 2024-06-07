import streamlit as st
from google.cloud import bigquery
import pandas as pd
import altair as alt
import plotly.express as px
import json

# Load credentials JSON file
with open('Clave-UwU.json') as f:
    credentials_info = json.load(f)

# Initialize BigQuery client using the credentials
client = bigquery.Client.from_service_account_info(credentials_info)

# Dashboard layout
st.set_page_config(page_title='Gaming Dashboard', layout='wide')

# Query data from BigQuery
@st.cache_data
def run_query(query):
    query_job = client.query(query)
    return query_job.result().to_dataframe()

# Define queries
games_query = """
SELECT * FROM `game-plataform.Tablas.Juego`
"""

facts_query = """
SELECT * FROM `game-plataform.Tablas.Hechos`
"""

users_query = """
SELECT * FROM `game-plataform.Tablas.Usuario`
"""

# Fetch data
games_df = run_query(games_query)
facts_df = run_query(facts_query)
users_df = run_query(users_query)



st.title('Gaming Dashboard')

# Section: Game Information
st.sidebar.header('Game Information')
selected_game_title = st.sidebar.selectbox('Select a Game', games_df['TITULO'])
selected_game = games_df[games_df['TITULO'] == selected_game_title]

st.sidebar.subheader('Game Details')
st.sidebar.write(f"**Title:** {selected_game['TITULO'].values[0]}")
st.sidebar.write(f"**Price:** ${selected_game['PRECIO'].values[0]:.2f}")
st.sidebar.write(f"**Release Date:** {selected_game['FECHALANZAMIENTO'].values[0]}")
st.sidebar.write(f"**Description:** {selected_game['DESCRIPCION'].values[0]}")
st.sidebar.write(f"**Classification:** {selected_game['CLASIFICACION'].values[0]}")
st.sidebar.write(f"**Score:** {selected_game['PUNTUACION'].values[0]:.1f}")

# Filter facts by selected game
selected_game_facts = facts_df[facts_df['int64_field_0'] == selected_game['IDJUEGO'].values[0]]

# Section: Game Statistics
st.header('Game Statistics')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Sessions', selected_game_facts['int64_field_9'].sum())
col2.metric('Average Session Duration', f"{selected_game_facts['double_field_5'].mean():.2f} min")
col3.metric('Max Session Duration', f"{selected_game_facts['int64_field_7'].max()} min")
col4.metric('Min Session Duration', f"{selected_game_facts['int64_field_8'].min()} min")

# Section: User Information
st.header('User Information')
st.dataframe(users_df)

# Section: Advanced Analysis
st.header('Advanced Analysis')

# Queries
popularidad_query = """
SELECT f.int64_field_2 AS Mes, j.TITULO AS Titulo, SUM(h.int64_field_9) AS TotalPartidas
FROM `game-plataform.Tablas.Hechos` AS h
JOIN `game-plataform.Tablas.Juego` AS j ON h.int64_field_0 = j.IDJUEGO
JOIN `game-plataform.Tablas.Fecha` AS f ON h.int64_field_4 = f.int64_field_0
GROUP BY Mes, Titulo
ORDER BY Mes DESC
"""

retencion_query = """
SELECT j.TITULO AS Titulo, u.string_field_1 AS Usuario, COUNT(h.int64_field_4) AS DiasJugados
FROM `game-plataform.Tablas.Hechos` AS h
JOIN `game-plataform.Tablas.Juego` AS j ON h.int64_field_0 = j.IDJUEGO
JOIN `game-plataform.Tablas.Usuario` AS u ON h.int64_field_3 = u.int64_field_0
GROUP BY Titulo, Usuario
ORDER BY DiasJugados DESC
"""

compras_query = """
WITH juegos_primera_vez AS (
    SELECT
        h.int64_field_0 AS IDJUEGO,
        h.int64_field_3 AS IDUSUARIO,
        f.int64_field_1 AS Anio,
        j.TITULO AS Titulo,
        j.PRECIO AS Precio,
        ROW_NUMBER() OVER (PARTITION BY h.int64_field_0, h.int64_field_3 ORDER BY f.int64_field_1) AS rn
    FROM 
        `game-plataform.Tablas.Hechos` AS h
    JOIN 
        `game-plataform.Tablas.Juego` AS j ON h.int64_field_0 = j.IDJUEGO
    JOIN 
        `game-plataform.Tablas.Fecha` AS f ON h.int64_field_4 = f.int64_field_0
)
SELECT 
    Anio, 
    Titulo, 
    SUM(Precio) AS Compras
FROM 
    juegos_primera_vez
WHERE 
    rn = 1
GROUP BY 
    Anio, 
    Titulo
ORDER BY 
    Anio;

"""

# Fetch data
popularidad_df = run_query(popularidad_query)
popularidad_df = popularidad_df[popularidad_df["Titulo"] == selected_game_title]
retencion_df = run_query(retencion_query)
retencion_df = retencion_df[retencion_df["Titulo"] == selected_game_title].head(10)
compras_df = run_query(compras_query)
compras_df = compras_df[compras_df["Titulo"] == selected_game_title]

# Popularidad de Juegos por Mes
st.header('Popularidad de Juegos por Mes')
# Crear el gráfico de pastel
fig = px.pie(popularidad_df, 
             names='Mes', 
             values='TotalPartidas',
             title='Popularidad de Juegos por Mes',
             hole=0.3)

st.plotly_chart(fig, use_container_width=True)

# Retención de Usuarios por Juego (Top 10)
st.header('Retención de Usuarios por Juego (Top 10)')
retencion_chart = alt.Chart(retencion_df).mark_bar().encode(
    x='Usuario:N',
    y='DiasJugados:Q',
    color='Titulo:N'
).properties(
    title='Retención de Usuarios por Juego (Top 10)',
    width=800
)
st.altair_chart(retencion_chart, use_container_width=True)

# Compras por Año
st.header('Ganacias por Año')
compras_chart = alt.Chart(compras_df).mark_bar().encode(
    x='Anio:O',
    y='Compras:Q'
).properties(
    title='Compras por Año',
    width=800
)
st.altair_chart(compras_chart, use_container_width=True)

# Footer
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p></p>
    </div>
""", unsafe_allow_html=True)
