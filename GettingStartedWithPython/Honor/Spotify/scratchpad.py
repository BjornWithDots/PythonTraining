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
    SELECT top 10 track_id
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
    print(results)

        # cur.execute('''merge INTO
        #                     Artist with (holdlock) t
        #                 using
        #                     (VALUES ( ?, ? )) s (artist_name, artist_id)
        #                 on t.artist_name = s.artist_name
        #                 and t.artist_id is null
        #                 when matched THEN UPDATE SET
        #                     t.artist_id = s.artist_id;
        #                 ''', (t2['name'], t2['id']))
        #
        # conn.commit()