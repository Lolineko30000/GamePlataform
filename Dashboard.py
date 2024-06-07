import streamlit as st
from google.cloud import bigquery
import pandas as pd
import altair as alt
import json

# Load credentials JSON file
with open('path/to/your/service-account-file.json') as f:
    credentials_info = json.load(f)

# Initialize BigQuery client using the credentials
client = bigquery.Client.from_service_account_info(credentials_info)

# Query data from BigQuery
@st.cache_data
def run_query(query):
    query_job = client.query(query)
    return query_job.result().to_dataframe()

# Define queries
games_query = """
SELECT * FROM `your_project.your_dataset.Juego`
"""

facts_query = """
SELECT * FROM `your_project.your_dataset.Hechos`
"""

users_query = """
SELECT * FROM `your_project.your_dataset.Usuario`
"""

platforms_query = """
SELECT * FROM `your_project.your_dataset.Plataforma`
"""

# Fetch data
games_df = run_query(games_query)
facts_df = run_query(facts_query)
users_df = run_query(users_query)
platforms_df = run_query(platforms_query)

# Dashboard layout
st.set_page_config(page_title='Gaming Dashboard', layout='wide')

st.title('Gaming Dashboard')

# Section: Game Information
st.sidebar.header('Game Information')
selected_game_title = st.sidebar.selectbox('Select a Game', games_df['Titulo'])
selected_game = games_df[games_df['Titulo'] == selected_game_title]

st.sidebar.subheader('Game Details')
st.sidebar.write(f"**Title:** {selected_game['Titulo'].values[0]}")
st.sidebar.write(f"**Price:** ${selected_game['Precio'].values[0]:.2f}")
st.sidebar.write(f"**Release Date:** {selected_game['FechaLanzamiento'].values[0]}")
st.sidebar.write(f"**Description:** {selected_game['Descripción'].values[0]}")
st.sidebar.write(f"**Classification:** {selected_game['Clasificacion'].values[0]}")
st.sidebar.write(f"**Score:** {selected_game['Puntuación'].values[0]:.1f}")

# Filter facts by selected game
selected_game_facts = facts_df[facts_df['IDJuego'] == selected_game['IDJuego'].values[0]]

# Section: Game Statistics
st.header('Game Statistics')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Sessions', selected_game_facts['TotalPartidas'].sum())
col2.metric('Average Session Duration', f"{selected_game_facts['PromedioDuracionPartida'].mean():.2f} min")
col3.metric('Max Session Duration', f"{selected_game_facts['MaxDuracionPartida'].max()} min")
col4.metric('Min Session Duration', f"{selected_game_facts['MinDuracionPartida'].min()} min")

# Section: User Information
st.header('User Information')
st.dataframe(users_df)

# Section: Platform Statistics
st.header('Platform Statistics')
platform_game_count_query = """
SELECT p.NombrePlataforma, COUNT(*) as GameCount
FROM `your_project.your_dataset.Hechos` as h
JOIN `your_project.your_dataset.Plataforma` as p ON h.IDPlataforma = p.IDPlataforma
GROUP BY p.NombrePlataforma
"""
platform_game_count_df = run_query(platform_game_count_query)

platform_chart = alt.Chart(platform_game_count_df).mark_bar().encode(
    x=alt.X('NombrePlataforma', sort='-y'),
    y='GameCount'
).properties(
    title='Number of Games per Platform',
    width=600,
    height=400
)
st.altair_chart(platform_chart, use_container_width=True)

# Section: Advanced Analysis
st.header('Advanced Analysis')

# Query for user activity over time
user_activity_query = """
SELECT u.NombreUsuario, f.IDFecha, SUM(f.TotalPartidas) as TotalSessions
FROM `your_project.your_dataset.Hechos` as f
JOIN `your_project.your_dataset.Usuario` as u ON f.IDUsuario = u.IDUsuario
GROUP BY u.NombreUsuario, f.IDFecha
ORDER BY f.IDFecha
"""
user_activity_df = run_query(user_activity_query)

user_activity_chart = alt.Chart(user_activity_df).mark_line().encode(
    x='IDFecha:O',
    y='TotalSessions:Q',
    color='NombreUsuario:N'
).properties(
    title='User Activity Over Time',
    width=800,
    height=400
)
st.altair_chart(user_activity_chart, use_container_width=True)

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
        <p>Created by Your Name - © 2024</p>
    </div>
""", unsafe_allow_html=True)
