import sqlite3
import streamlit as st
import pandas as pd




#print(fetch_athletes("Athletes", "ID", "Athlete").values())

def get_data_summary():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        query = """SELECT mv.ID AS medal_victory_id,
                        a.Athlete AS athlete_name,
                        c.Country AS country_name,
                        oe.Year AS event_year,
                        oe.Type_of_Games AS event_type,
                        st.Sport AS sport_name,
                        mt.Medal_Type AS medal_type,
                        mv.Age_of_Athlete AS athlete_age,
                        mv.Number_of_Medals_won AS number_of_medals
                FROM Medal_Victories mv
                LEFT JOIN Countries c ON mv.COUNTRY_ID = c.ID
                LEFT JOIN Olympic_Events oe ON mv.OLYMPIC_EVENT_ID = oe.ID
                LEFT JOIN Medal_Types mt ON mv.MEDAL_TYPE_ID = mt.ID
                LEFT JOIN Sport_Types st ON mv.SPORTS_ID = st.ID
                LEFT JOIN Athletes a ON mv.ATHLETE_ID = a.ID
                ORDER BY oe.Year DESC, c.Country ASC, a.Athlete ASC
        """
    
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
            conn.close()

def get_all_medal_victories():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM Medal_Victories", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching medal victories: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def get_all_athletes():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM Athletes", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching athletes: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
        
                
df = get_data_summary()
df_medals = get_all_medal_victories()
df_athletes = get_all_athletes()



print(df_medals.tail(10))
#print(df_athletes.tail(10))


import sqlite3


conn = sqlite3.connect('olympic_database.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print(table[0])

conn.close()

# Print entire Olympic_Events table
conn = sqlite3.connect('olympic_database.db')
df_events = pd.read_sql_query("SELECT * FROM Olympic_Events", conn)
print("\nOlympic_Events table:")
print(df_events)
conn.close()
