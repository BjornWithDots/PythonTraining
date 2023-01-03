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

df_album = pd.read_sql_query("""
        SELECT DISTINCT TOP 5 album.album_id
        FROM Album album
            inner join Track track
                on album.id = track.album_id
        WHERE   album.album_id is not null
				and track.track_id is null
        ORDER BY 1 DESC
        """, conn)


# Connection to the Spotify API
sp = spotify_connection()

track_names = []
track_ids = []

def getspinfo(type):


    for album in df_album["album_id"]:
        album_uri = 'spotify:album:'+album

        results = sp.artist_albums(album_uri, album_type='album')

        #results =  sp.artist_albums(artist_uri, album_type=type)

#[{'album_id':item['id'], 'album_name':item['name']} for item in results['items']]

        album_names = []
        album_ids = []
#    albumlist ={}

        albums = results['items']
    #print(albums)
        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        for album in albums:
            #print(album['name'], album['id'])
            album_name = album['name']
            album_id = album['id']

            cur.execute('''merge INTO
                            Album with (holdlock) t
                        using
                            (VALUES ( ?, ? )) s (album_title, album_id)
                        on t.album_title = s.album_title
                        and t.album_id is null

                        --when not matched then
                        --    insert values (s.album_title, s.album_id)
                        when matched THEN UPDATE SET
                            t.album_id = s.album_id;
                        ''', (album_name, album_id))
            try:
                cur.execute('SELECT id FROM Album WHERE album_title = ? ', (album_name,))
                album_key = cur.fetchone()[0]
                print('Albumname:', album_name, 'Albumid', album_id)
            except:
                print('Havent listen to:', album_name)

            conn.commit()

getspinfo('single')
getspinfo('album')
getspinfo('compilation')