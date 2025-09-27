import pandas as pd
import sqlite3

df = pd.read_csv("data/online_retail_II.csv", encoding="latin1")

conn = sqlite3.connect("database.db")

df.to_sql("retail_data",conn,if_exists="replace",index=False)

print("Data saved to SQLite DB successfully!")