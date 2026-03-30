import sqlite3


conn = sqlite3.connect('Olympic_database.db')

cursor = conn.cursor()


# query = """SELECT mv.ID AS medal_victory_id,
#                   a.Athlete AS athlete_name,
#                   c.Country AS country_name,
#                   oe.Year AS event_year,
#                   oe.Type_of_Games AS event_type,
#                   st.Sport AS sport_name,
#                   mt.Medal_Type AS medal_type,
#                   mv.Age_of_Athlete AS athlete_age,
#                   mv.Number_of_Medals_won AS number_of_medals
#            FROM Medal_Victories mv
#            LEFT JOIN Countries c ON mv.COUNTRY_ID = c.ID
#            LEFT JOIN Olympic_Events oe ON mv.OLYMPIC_EVENT_ID = oe.ID
#            LEFT JOIN Medal_Types mt ON mv.MEDAL_TYPE_ID = mt.ID
#            LEFT JOIN Sport_Types st ON mv.SPORTS_ID = st.ID
#            LEFT JOIN Athletes a ON mv.ATHLETE_ID = a.ID
#            ORDER BY oe.Year DESC, c.Country ASC, a.Athlete ASC
# """
# cursor.execute(query).fetchone()

tables = ['Athletes', 'Countries', 'Medal_Types', 'Olympic_Events', 'Sport_Types', 'Medal_Victories']
for table in tables:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Table '{table}' has {count} rows.")
# Repeat for other tables