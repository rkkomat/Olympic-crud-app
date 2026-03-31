import sqlite3
import pandas as pd

# Connect to the SQLite database (or create it if it doesn't exist)

# Path to your Excel file
excel_file = 'OlympicGamesDataset.xlsx'  # Replace with your actual file name

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('Olympic_database.db')  # Replace with your desired DB name
cursor = conn.cursor()
print("Connected to SQLite database: 'Olympic_database.db'")



print("Creating table 'Athletes'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Athletes
                     (ID INTEGER PRIMARY KEY, 
                     Athlete TEXT,
                     Country TEXT,
                     Athlete_Sport TEXT,
                     Year_of_birth INTEGER)''')						 	

conn.commit()
print("Table 'Athletes' created successfully.")

# Load from Excel
try:
    athletes_df = pd.read_excel(excel_file, sheet_name='Athletes')
    athletes_df.to_sql('Athletes', conn, if_exists='append', index=False)
    print("Data from 'Athletes' sheet loaded successfully.")
except Exception as e:
    print(f"Error loading 'Athletes' sheet: {e}")
    
# ============================================================
# Sheet 3: Countries Data    
# ============================================================

print("Creating table 'Countries'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Countries
                     (ID INTEGER PRIMARY KEY, 
                     Country TEXT,
                     Region TEXT,
                     Population INTEGER,
                     Area INTEGER,
                     Pop_Density FLOAT,
                     Coastline FLOAT,
                     Net_migration FLOAT,
                     GDP INTEGER,
                     Literacy FLOAT,
                     Birthrate FLOAT)''')

conn.commit()
print("Table 'Countries' created successfully.")

# Load from Excel
try:
    countries_df = pd.read_excel(excel_file, sheet_name='Country Data')
    countries_df.to_sql('Countries', conn, if_exists='append', index=False)
    print("Data from 'Countries' sheet loaded successfully.")
except Exception as e:
    print(f"Error loading 'Countries' sheet: {e}")
    

# ============================================================
# Sheet 4: Medal_Types
# ============================================================

print("Creating table 'Medal_Types'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Medal_Types
                     (ID INTEGER PRIMARY KEY, 
                     Medal_Type TEXT)''')

conn.commit()

medal_types_data = [
    (1, 'Gold'),
    (2, 'Silver'),
    (3, 'Bronze')]

cursor.executemany("INSERT OR IGNORE INTO Medal_Types (ID, Medal_Type) VALUES (?, ?)", medal_types_data)
conn.commit()   
print("Table 'Medal_Types' created and populated successfully.")

# ============================================================
# Sheet 5: Olympic_Events
# ============================================================

print("Creating table 'Olympic_Events'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Olympic_Events
                     (ID INTEGER PRIMARY KEY,
                     Year INTEGER,
                     Type_of_Games TEXT,
                     Location TEXT,
                     Country TEXT,
                     Ceremony_Date DATE)''')

conn.commit()
print("Table 'Olympic_Events' created successfully.")

# Load from Excel
try:
    olympic_events_df = pd.read_excel(excel_file, sheet_name='Olympic Events')
    olympic_events_df.to_sql('Olympic_Events', conn, if_exists='append', index=False)
    print("Data from 'Olympic_Events' sheet loaded successfully.")
except Exception as e:
    print(f"Error loading 'Olympic_Events' sheet: {e}")
    
# ============================================================
# Sheet 6: Sport_Types
# ============================================================

print("Creating table 'Sport_Types'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Sport_Types
                     (ID INTEGER PRIMARY KEY, 
                     Sport TEXT)''')

conn.commit()
print("Table 'Sport_Types' created successfully.")

# Load from Excel
try:
    sport_types_df = pd.read_excel(excel_file, sheet_name='Sport Types')
    sport_types_df.to_sql('Sport_Types', conn, if_exists='append', index=False)
    print("Data from 'Sport_Types' sheet loaded successfully.")
except Exception as e:
    print(f"Error loading 'Sport_Types' sheet: {e}")

# ============================================================
# Sheet 1: Medal_Victories
# ============================================================

print("Creating table 'Medal_Victories'...")
cursor.execute('''CREATE TABLE IF NOT EXISTS Medal_Victories (
                    ID INTEGER PRIMARY KEY,
                    ATHLETE_ID INTEGER,
                    COUNTRY_ID INTEGER,
                    OLYMPIC_EVENT_ID INTEGER,
                    SPORTS_ID INTEGER,
                    MEDAL_TYPE_ID INTEGER,
                    Age_of_Athlete INTEGER,
                    Number_of_Medals_won INTEGER,
                    FOREIGN KEY (ATHLETE_ID) REFERENCES Athletes(ID),
                    FOREIGN KEY (COUNTRY_ID) REFERENCES Countries(ID),
                    FOREIGN KEY (OLYMPIC_EVENT_ID) REFERENCES Olympic_Events(ID),
                    FOREIGN KEY (SPORTS_ID) REFERENCES Sport_Types(ID),
                    FOREIGN KEY (MEDAL_TYPE_ID) REFERENCES Medal_Types(ID)
                    )''')


conn.commit()
print("Table 'Medal_Victories' created successfully.")

# Load from Excel
try:
    medal_victories_df = pd.read_excel(excel_file, sheet_name='Medal Victories')
    medal_victories_df.to_sql('Medal_Victories', conn, if_exists='append', index=False)
    print("Data from 'Medal_Victories' sheet loaded successfully.")
except Exception as e:
    print(f"Error loading 'Medal_Victories' sheet: {e}")
    


# Close the database connection

conn.close()
print("Database connection closed.")
print("All 6 tables created and populated successfully. Databe: 'Olympic_database.db' is ready for use.")


