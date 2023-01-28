import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
import sys

def read_credentials(fpath):
    # reads first line of a path
    fo = open(fpath, "r")
    return fo.readline()
def sql_connection():
    credentials_file_name = 'python'
    username = credentials_file_name
    password = read_credentials(f'./credentials/{username}.txt')
    driver = '{ODBC Driver 17 for SQL Server}'
    # server = '34.88.195.162'
    server = '192.168.0.245'
    database = 'Spotify'

    connection_string = f"Driver={driver};Server={server}; Database={database}; UID={username};PWD={password}"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    sql_engine = create_engine(connection_url)
    conn = sql_engine.raw_connection()

    return conn
def spotify_connection():
    # Tells spotipy what to get
    scope = "user-read-recently-played"

    # Connection information for Spotify app setup: https://developer.spotify.com/dashboard/applications
    # https://www.section.io/engineering-education/spotify-python-part-1/
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.SPOTIPY_CLIENT_ID,
                                               client_secret=cred.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=cred.SPOTIPY_REDIRECT_URI,
                                               scope=scope))
    return sp

# Connection for the SQL database
conn = sql_connection()
cur = conn.cursor()

df_tracks = pd.read_sql_query("""
    SELECT top 100 track_id
    FROM Spotify.dbo.Track
    where energy is null
        """, conn)


# Connection to the Spotify API
sp = spotify_connection()
# shows tracks for the given artist

# usage: python tracks.py [artist name]

for i, track in df_tracks.iterrows():
    print(track[0])
    results = sp.audio_features(tracks=track)
    info = (results[0])
    #print(info['danceability'])

    cur.execute('''merge INTO
                            Track with (holdlock) t
                        using
                            (VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )) 
                                            s (track_id,
                                            danceability, 
                                                energy,
                                                loudness,
                                                speechiness,
                                                [key],
                                                mode,
                                                acousticness,
                                                instrumentalness,
                                                liveness,
                                                valence,
                                                tempo,
                                                time_signature)
                        on t.track_id = s.track_id
                        and t.danceability is null
                        when matched THEN UPDATE SET
                            t.danceability = s.danceability,
                            t.energy = s.energy,
                            t.loudness = s.loudness,
                            t.speechiness = s.speechiness,
                            t.[key] = s.[key],
                            t.mode = s.mode,
                            t.acousticness = s.acousticness,
                            t.instrumentalness = s.instrumentalness,
                            t.liveness = s.liveness,
                            t.valence = s.valence,
                            t.tempo = s.tempo,
                            t.time_signature = s.time_signature
                            ;
                        ''', (track[0],
                              info['danceability'],
                              info['energy'],
                              info['loudness'],
                              info['speechiness'],
                              info['key'],
                              info['mode'],
                              info['acousticness'],
                              info['instrumentalness'],
                              info['liveness'],
                              info['valence'],
                              info['tempo'],
                              info['time_signature']))

    conn.commit()