import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd

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

df_artist = pd.read_sql_query("""
        SELECT DISTINCT TOP 10 artist.artist_id
        FROM Album album
            inner join Artist artist
                on album.artist_id = artist.id
        WHERE  album_id is null
            and artist.artist_id is not null
        ORDER BY 1 DESC
        """, conn)


# Connection to the Spotify API
sp = spotify_connection()

album_names = []
album_ids = []

for artist in df_artist["artist_id"]:
    artist_uri = 'spotify:artist:'+artist

    results = sp.artist_albums(artist_uri, album_type='album')

    album_names = []
    album_ids = []

    albums = results['items']
    #print(albums)
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in results["items"]:
        album_names.append(album["name"])
        album_ids.append(album["id"])

    print(album_names)

    #for album in albums:
    #    print(album['name'], album['id'])

        # cur.execute('''merge INTO
        #                     AlbumsUpdate with (holdlock) t
        #                 using
        #                     (VALUES ( ?, ? )) s (album_title, album_id)
        #                 on t.album_id = s.album_id
        #
        #                 when not matched then
        #                     insert values (s.album_title, s.album_id)
        #                 when matched THEN UPDATE SET
        #                     t.album_id = s.album_id;
        #                 ''', (album_name, album_id))
        # cur.execute('SELECT album_id FROM AlbumsUpdate WHERE album_title = ? ', (album_name,))
        # album_key = cur.fetchone()[0]
        #
        # print('Albumname:',album_name, 'Albumid',album_id )