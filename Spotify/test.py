import pyodbc

def read_credentials(fpath):
    #reads first line of a path
    fo = open(fpath, "r")
    return fo.readline()

credentials_file_name = 'python'
username = credentials_file_name
password = read_credentials(f'./credentials/{username}.txt')
driver = '{ODBC Driver 17 for SQL Server}'
server = '192.168.0.245'
database = 'Spotify'

cnxn = f"Driver={driver};Server={server}; Database={database}; UID={username};PWD={password}"

conn = pyodbc.connect(cnxn)

cur = conn.cursor()