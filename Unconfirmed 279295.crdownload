import streamlit as st
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

# Query data from BigQuery
@st.cache
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

# Fetch data
games_df = run_query(games_query)
facts_df = run_query(facts_query)

# Dashboard layout
st.title('Gaming Dashboard')

# Section: Game Information
st.header('Game Information')
st.dataframe(games_df)

# Section: Game Statistics
st.header('Game Statistics')

# Select game
game_title = st.selectbox('Select a Game', games_df['Titulo'])

# Filter facts by selected game
selected_game_facts = facts_df[facts_df['IDJuego'] == games_df[games_df['Titulo'] == game_title]['IDJuego'].values[0]]

# Display statistics
st.subheader(f'Statistics for {game_title}')
st.write('Total Sessions:', selected_game_facts['TotalPartidas'].sum())
st.write('Average Session Duration:', selected_game_facts['PromedioDuracionPartida'].mean())
st.write('Max Session Duration:', selected_game_facts['MaxDuracionPartida'].max())
st.write('Min Session Duration:', selected_game_facts['MinDuracionPartida'].min())

# Additional visualizations can be added here