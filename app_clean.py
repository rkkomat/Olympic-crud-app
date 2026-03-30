import sqlite3
import streamlit as st
import pandas as pd
from helper_functions import get_data_summary, get_all_athletes, insert_athlete, insert_medal_victories    


st.set_page_config(page_title="Olympic Data Manager", page_icon="🏅", layout="wide")

col1, col2 = st.columns([1, 6])

with col1:
    st.image("image.png", width=1000)

with col2:
    st.markdown(
        """
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <h1 style="margin-bottom: 0;">Olympic Games Data Manager</h1>
            <p style="color: gray; font-size: 18px;">
                Explore, filter, and manage Olympic athletes and medal victories
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )



# =========================================================================================================

#page = st.sidebar.radio("Select a page:", ["View Data", "Add Data"])

with st.sidebar:
    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "Go to",
        ["View Data", "Add Data"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("Olympic Data Manager v1.0")

# =========================================================================================================
# Page: View Data
# =========================================================================================================



if page == "View Data":
    #st.header("View Olympic Data")
    
    df_summary = get_data_summary()
    
    if len(df_summary) == 0:
        st.warning("No data available to display.")
    else:
        st.success(f"Data loaded successfully! Total records: {len(df_summary)}")
        
        
        st.markdown("### Filters")
        
        with st.container():
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                athlete_names = [name for name in df_summary['athlete_name'].unique() if name is not None]
                athlete_filter = st.multiselect("Athlete", options=sorted(athlete_names), default=[])
                #athlete_filter = st.multiselect("Athlete", options = sorted(df_summary['athlete_name'].unique()), default=[])
            with col2:
                country_names = [name for name in df_summary['country_name'].unique() if name is not None]
                country_filter = st.multiselect("Country", options=sorted(country_names), default=[])
            with col3:
                sport_names = [name for name in df_summary['sport_name'].unique() if name is not None]
                sport_filter = st.multiselect("Sport", options=sorted(sport_names), default=[])
            with col4:
                year_filter = st.multiselect("Filter by Year", options=sorted(df_summary['event_year'].unique()))
                
            st.markdown("</div>", unsafe_allow_html=True)
            
        df_filtered = df_summary[['athlete_name', 'country_name', 'sport_name', 'event_year', 'medal_type', 'athlete_age', 'number_of_medals']].copy()
        
        if athlete_filter:
            df_filtered = df_filtered[df_filtered['athlete_name'].isin(athlete_filter)]
        if country_filter:
            df_filtered = df_filtered[df_filtered['country_name'].isin(country_filter)]
        if sport_filter:
            df_filtered = df_filtered[df_filtered['sport_name'].isin(sport_filter)]
        if year_filter:
            df_filtered = df_filtered[df_filtered['event_year'].isin(year_filter)]
            
        #Display filtered data
        st.write(f"Showing {len(df_filtered)} records after applying filters.")
        st.dataframe(df_filtered, width = 'stretch')
        
        #Stats
        st.markdown("### Summary Statistics")   
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_medals = df_filtered['number_of_medals'].sum()
            st.metric("Total Medals", total_medals)
        with col2:
            unique_athletes = df_filtered['athlete_name'].nunique()
            st.metric("Unique Athletes", unique_athletes)
        with col3:
            unique_countries = df_filtered['country_name'].nunique()
            st.metric("Unique Countries", unique_countries)
        with col4:
            unique_sports = df_filtered['sport_name'].nunique()
            st.metric("Unique Sports", unique_sports)
        
elif page == "Add Data":
    st.header("Add New Olympic Data")
    #st.warning("This feature is under development. Please check back later.")   
    
    tab1, tab2 = st.tabs(["Add Athlete", "Add Medal Victory"])
    df = get_data_summary()

                
    with tab1:
        st.subheader("Add Athlete")
        st.info("This form will allow you to add a new athlete record.")
        
        with st.form("athlete_form"):
        
            sel_athlete_name = st.text_input("Athlete Name", placeholder="Enter athlete's full name. E.g. 'Usain Bolt'")
            sel_athlete_country = st.selectbox("Country", options=["--select--"] + list(df['country_name'].unique()))
            sel_athlete_sport = st.selectbox("Sport Type", options=["--select--"] + list(df['sport_name'].unique()))
            sel_athlete_DOY = st.number_input("Year of Birth", placeholder="Enter athlete's year of birth. E.g. 1986", min_value=1900, max_value=2024, step=1)
        
            submitted_athlete = st.form_submit_button("Add Athlete")
            
            if submitted_athlete:
                
                if not sel_athlete_name.strip():
                    st.warning("Please enter a valid athlete name.")
                elif sel_athlete_country == "--select--":
                    st.warning("Please select a country for the athlete.")
                elif sel_athlete_sport == "--select--":
                    st.warning("Please select a sport type for the athlete.")
                else:
                    success = insert_athlete(name=sel_athlete_name.strip(), 
                                             country=sel_athlete_country, 
                                             sport=sel_athlete_sport,
                                             year_of_birth=sel_athlete_DOY)
                    if success:
                        st.success(f"Athlete '{sel_athlete_name}' added successfully!")
                        
    with tab2:
        st.subheader("Add Medal Victory")
        st.info("This form will allow you to add a new medal victory record.")
        
        df_athletes = get_all_athletes()
        
        sel_athlete =st.selectbox("Athlete",  options=["--select--"] + list(df_athletes['Athlete'].unique()))
        sel_country  = st.selectbox("Country",  options=["--select--"] + list(df_athletes[df_athletes['Athlete'] == sel_athlete]['Country'].unique()))        
        event_years = sorted(df['event_year'].dropna().astype(int).unique().tolist())
        sel_event_year = st.selectbox("Olympic Event Year", options=["--select--"] + event_years)
        sel_sport = st.selectbox("Sport Type", options=["--select--"] + list(df['sport_name'].unique()), key="medal_sport")
        sel_medal_type = st.selectbox("Medal Type", options=["--select--"] + list(df['medal_type'].unique())) 
        
        if sel_athlete != "--select--":
            sel_athleteID = int(df_athletes[df_athletes['Athlete'] == sel_athlete]['ID'].iloc[0])
        else:
            sel_athleteID = None
            
        if sel_country != "--select--":
            sel_countryID = int(df[df['country_name'] == sel_country]['country_id'].iloc[0])
        else:
            sel_countryID = None
            
        if sel_event_year != "--select--":
            sel_event_yearID = int(df[df['event_year'] == sel_event_year]['olympic_event_id'].iloc[0])
        else:
            sel_event_yearID = None
        
        if sel_sport != "--select--":
            sel_sportID = int(df[df['sport_name'] == sel_sport]['sport_id'].iloc[0])
        else:
            sel_sportID = None
            
        if sel_medal_type != "--select--":
            sel_medal_typeID = int(df[df['medal_type'] == sel_medal_type]['medal_type_id'].iloc[0])  
        else:
            sel_medal_typeID = None
            
        
        
        
        with st.form("medal_victory_form"):

            sel_age =st.number_input("Age of Athlete", min_value=0, max_value=100, step=1)
            sel_medals_won =st.number_input("Number of Medals Won", min_value=1, max_value=10, step=1)
            
            submitted = st.form_submit_button("Add Medal Victory")
            
            if submitted:
                
                if sel_athlete == "--select--":
                    st.warning("Please select an athlete.")
                elif sel_country == "--select--":
                    st.warning("Please select a country.")
                elif sel_event_year == "--select--":
                    st.warning("Please select an Olympic event year.")
                elif sel_sport == "--select--":
                    st.warning("Please select a sport type.")
                elif sel_medal_type == "--select--":
                    st.warning("Please select a medal type.")
                else:
                    success_medals = insert_medal_victories(athleteID=sel_athleteID,
                                                            countryID=sel_countryID,
                                                            olympic_event_id=sel_event_yearID,
                                                            sports_id=sel_sportID,
                                                            medal_type_id=sel_medal_typeID,
                                                            age=sel_age,
                                                            number_of_medals=sel_medals_won)
                    
                    if success_medals:
                        st.success(f"Medal victory for athlete **{sel_athlete}** added successfully!")
                        
                        


