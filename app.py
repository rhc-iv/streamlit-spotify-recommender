# Import statement(s):
import os

import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Save credentials for Spotify API as environment variables; load via the
# Python-Dotenv library:
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up the Streamlit app:
st.set_page_config(
    page_title='Spotify Recommender',
    page_icon='🎧',
    layout='wide'
)

# Create a Streamlit for to collect user music data input:
with st.form('Artist and Song to search by:'):
    artist_input = st.text_input('Enter the name of an artist.')
    song_input = st.text_input('Enter the name of a song.')
    submit_button = st.form_submit_button(label='Submit')

# Retrieve recommendations from Spotify based on user input:
if submit_button:
    query = f"{artist_input} {song_input}"
    result = sp.search(query, limit=1, type='track')
    track_id = result['tracks']['items'][0]['id']
    recommendations = sp.recommendations(seed_tracks=[track_id])['tracks']
    st.write('Here are your recommendations:')
    for track in recommendations:
        link = f"<a href='spotify:track:{track['id']}' target='_blank'>{track['name']} by {track['artists'][0]['name']}</a>"
        st.write(link, unsafe_allow_html=True)
