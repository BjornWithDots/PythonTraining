from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd


connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

df_loaded = pd.read_sql_query("""
    SELECT TOP 1000 played_at
    FROM Playlog
    ORDER BY 1 DESC
    """, engine)

print(df_loaded)