import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import pandas as pd
import sqlite3


debug = 0
# Tells spotipy what to get
scope = "user-read-recently-played"

# Connection information for Spotify app setup: https://developer.spotify.com/dashboard/applications
# https://www.section.io/engineering-education/spotify-python-part-1/
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.SPOTIPY_CLIENT_ID,
                                               client_secret=cred.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=cred.SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# print(results)

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()


def create_tables():
    # Make some fresh tables using executescript()
    cur.executescript('''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;
    DROP TABLE IF EXISTS Playlog;
    
    CREATE TABLE Artist (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );
    
    CREATE TABLE Album (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id  INTEGER,
        title   TEXT UNIQUE
    );
    
    CREATE TABLE Track (
        id  INTEGER NOT NULL PRIMARY KEY 
            AUTOINCREMENT UNIQUE,
        title TEXT  UNIQUE,
        album_id  INTEGER,
        duration INTEGER, 
        popularity INTEGER, 
        count INTEGER,
        last_played TEXT
    );
    
    CREATE TABLE Playlog (
        id INTEGER NOT NULL PRIMARY KEY
           AUTOINCREMENT UNIQUE,
        track_id INTEGER,
        popularity INTEGER,
        played_at TEXT UNIQUE
    );
    ''')


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Kolla om dataframe är tom
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    # Kolla så att primary key är unik
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated")

    # Kolla efter nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    return True


if __name__ == "__main__":

    results = sp.current_user_recently_played()

    # print(data)

    song_names = []
    artist_names = []
    album_names = []
    played_at_list = []
    timestamps = []
    popularity = []
    duration_ms = []

    # Extracting only the relevant bits of data from the json object
    for song in results["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        album_names.append(song["track"]["album"]["name"])
        popularity.append(song["track"]["popularity"])
        duration_ms.append(song["track"]["duration_ms"])

    # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
        "album_name": album_names,
        "popularity": popularity,
        "duration": duration_ms
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp", "album_name",
                                               "popularity", "duration"])

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

    if debug == 1:
        print(song_df)

for index, row in song_df.iterrows():
    name = row['song_name']
    artist = row['artist_name']
    album = row['album_name']
    played_at = row['played_at']
    timestamp = row['timestamp']
    duration = row['duration']
    rating = row['popularity']
    count = 1

    if name is None or artist is None or album is None :
        continue

    if debug == 1:
        print(name, artist, album, played_at, timestamp, duration, rating)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    try:
        cur.execute('''INSERT INTO Track
            (title, album_id, duration, popularity, count, last_played) 
            VALUES ( ?, ?, ?, ?, ?, ?)''',
            ( name, album_id, (duration/1000)/60, rating, count, played_at) )
        cur.execute('SELECT id FROM Track WHERE title = ? ', (name,))
        track_id = cur.fetchone()[0]

    except:
        cur.execute(''' UPDATE Track
                    SET count = count+1,
                    popularity = ?,
                    last_played = ?
                    WHERE title = ?
                    AND last_played != ? ''',
                (rating, played_at ,name, played_at))
        cur.execute('SELECT id FROM Track WHERE title = ? ', (name,))
        track_id = cur.fetchone()[0]


    cur.execute('''INSERT OR REPLACE INTO Playlog
        (track_id, popularity, played_at) 
        VALUES ( ?, ?, ?)''',
        (track_id, rating, played_at))

    conn.commit()