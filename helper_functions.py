import sqlite3
import pandas as pd
import streamlit as st




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
        
def get_all_countries():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT ID AS country_id, Country AS country_name FROM Countries ORDER BY Country ASC", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching countries: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
        
def get_all_sports():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT ID AS sport_id, Sport AS sport_name FROM Sport_Types ORDER BY Sport ASC", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching sports: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
        
def get_all_medal_types():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT ID AS medal_type_id, Medal_Type AS medal_type_name FROM Medal_Types ORDER BY Medal_Type ASC", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching medal types: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
        
def get_all_olympic_events():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        df = pd.read_sql_query("SELECT ID AS olympic_event_id, Year AS event_year, Type_of_Games AS event_type FROM Olympic_Events ORDER BY Year DESC", conn)
        return df
    except Exception as e:
        st.error(f"Error fetching Olympic events: {e}")
        return pd.DataFrame()
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



def get_data_summary():
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        query = """SELECT mv.ID AS medal_victory_id,
                        a.Athlete AS athlete_name,
                        a.ID AS athlete_id,
                        c.Country AS country_name,
                        c.ID AS country_id,
                        oe.Year AS event_year,
                        oe.Type_of_Games AS event_type,
                        oe.ID AS olympic_event_id,
                        st.Sport AS sport_name,
                        st.ID AS sport_id,
                        mt.Medal_Type AS medal_type,
                        mt.ID AS medal_type_id,
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


def insert_athlete(name, country, sport, year_of_birth):
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Check if athlete already exists
        cursor.execute("SELECT COUNT(*) FROM Athletes WHERE Athlete = ?", (name,))
        exists = cursor.fetchone()[0]
        
        if exists > 0:
            st.warning(f"Athlete '{name}' already exists in the database.")
            return False
        
        # Get new ID for athlete
        cursor.execute("SELECT MAX(ID) FROM Athletes")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1
        # Insert athlete
        cursor.execute("INSERT INTO Athletes (ID, Athlete, Country, Athlete_Sport, Year_of_Birth) VALUES (?, ?, ?, ?, ?)",
                       (new_id, name, country, sport, year_of_birth))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error inserting athlete: {e}")
        return False
    finally:
        conn.close()

def insert_medal_victories(athleteID, countryID, olympic_event_id, sports_id, medal_type_id, age, number_of_medals):
    try:
        conn = sqlite3.connect('olympic_database.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Get new ID for medal victory
        cursor.execute("SELECT MAX(ID) FROM Medal_Victories")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1
        # Insert medal victory
        cursor.execute("INSERT INTO Medal_Victories (ID, Athlete_ID, Country_ID, Olympic_Event_ID, Sports_ID, Medal_Type_ID, Age_of_Athlete, Number_of_Medals_won) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (new_id, athleteID, countryID, olympic_event_id, sports_id, medal_type_id, age, number_of_medals))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error inserting medal victory: {e}")
        return False
    finally:
        conn.close()