import pickle
import streamlit as st
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials


# UPDATE CLIENT ID AND SECRET FROM SPOTIFY API
CLIENT_ID = 'YOUR_ID'
CLIENT_SECRET = 'YOUR_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f'track:{song_name} artist:{artist_name}'
    results = sp.search(search_query, type='track', limit=1)

    if results and results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_cover_url = track['album']['images'][0]['url']
        print(album_cover_url)
        return album_cover_url
    
    else:
        return "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg"   

def recommender(song_name):
    index = music[music['song'] == song_name].index[0]
    distance = sorted(list(enumerate(similarity[index])) , reverse = True, key = lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []

    for i in distance[1:6]:

        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, music.iloc[i[0]].artist))

    return recommended_music_names, recommended_music_posters

st.title('Music Recommender System')
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox('Select a song', music_list)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommender(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)

    
    for i in range(5):
        st.image(recommended_music_posters[i])
        st.write(recommended_music_names[i])
