# Olympic Games Data Manager

A Streamlit web application for managing, viewing, and analyzing Olympic Games data using a local SQLite database. Easily add athletes, record medal victories, and filter or summarize Olympic data. The project is also ready for integration with Power BI for advanced analytics and visualization.

## Features
- View, filter, and summarize Olympic athletes and medal victories
- Add new athletes and medal records via user-friendly forms
- Data stored in a local SQLite database (`olympic_database.db`)
- Ready for Power BI integration (via ODBC or Python script)

## Requirements
- Python 3.8+
- pip
- Streamlit
- pandas
- sqlite3 (standard library)

## Setup
1. **Clone the repository or copy the project files.**
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install streamlit pandas
   ```
4. **Ensure your SQLite database (`olympic_database.db`) is present in the project folder.**

## Running the App
Start the Streamlit app with:
```bash
streamlit run app_clean.py
```

The app will open in your browser. Use the sidebar to navigate between viewing data and adding new records.

## Power BI Integration
You can connect your data to Power BI in two ways:

### 1. Using ODBC (Recommended for most users)
- Install the free [SQLite ODBC driver](https://www.ch-werner.de/sqliteodbc/)
- Set up a DSN pointing to your `olympic_database.db`
- In Power BI Desktop: Get Data > ODBC > Select your DSN

### 2. Using Python Script
- In Power BI Desktop: Get Data > Python script
- Use a script like:
  ```python
  import pandas as pd
  import sqlite3
  conn = sqlite3.connect(r"F:/Olympics/olympic_database.db")
  df = pd.read_sql_query("SELECT * FROM Athletes", conn)
  conn.close()
  ```
- Adjust the query/table as needed

## Project Structure
- `app_clean.py` — Main Streamlit application
- `olympic_database.db` — SQLite database (not included in repo)
- `env/` — (Optional) Python virtual environment

## Troubleshooting
- If you see float IDs in Power BI, ensure you cast IDs to `int` in your Python code before inserting or displaying.
- For Power BI Python integration errors, check that your Python version matches Power BI's bitness (both 64-bit recommended) and that `pandas` is installed.

## License
This project is for educational and demonstration purposes.

---

**Developed with Streamlit, pandas, and SQLite.**
