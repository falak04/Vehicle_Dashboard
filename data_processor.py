import pandas as pd
import streamlit as st
import sqlite3
from sqlite3 import Connection

# --- Database Setup ---
@st.cache_resource
def get_connection() -> Connection:
    """Creates a connection to an in-memory SQLite database."""
    # The 'check_same_thread=False' is needed for Streamlit's multithreading.
    return sqlite3.connect(":memory:", check_same_thread=False)

def setup_database(conn: Connection):
    """Loads the CSV data into a SQL table if it doesn't exist."""
    try:
        # Check if table already exists
        pd.read_sql("SELECT 1 FROM vehicle_data LIMIT 1", conn)
    except (pd.io.sql.DatabaseError, sqlite3.OperationalError):
        # If table doesn't exist, load it from CSV
        df = pd.read_csv('sample_vehicle_data.csv')
        df.to_sql('vehicle_data', conn, if_exists='replace', index=False)

# --- Data Processing Functions ---
def get_filtered_data_from_sql(conn: Connection, start_date, end_date, categories, manufacturers) -> pd.DataFrame:
    """Constructs and executes a SQL query to fetch filtered data."""
    # Build the WHERE clause dynamically to prevent SQL injection risks
    conditions = ["Date BETWEEN ? AND ?"]
    params = [str(start_date), str(end_date)]

    if categories:
        conditions.append(f"Vehicle_Type IN ({','.join(['?']*len(categories))})")
        params.extend(categories)
    
    if manufacturers:
        conditions.append(f"Manufacturer IN ({','.join(['?']*len(manufacturers))})")
        params.extend(manufacturers)

    query = f"SELECT * FROM vehicle_data WHERE {' AND '.join(conditions)}"
    
    df = pd.read_sql(query, conn, params=params)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@st.cache_data
def load_unique_values(_conn: Connection, column: str, table: str = 'vehicle_data') -> list:
    """Fetches unique values for a given column from the database."""
    query = f"SELECT DISTINCT {column} FROM {table}"
    df = pd.read_sql(query, _conn)
    return df[column].tolist()

def get_growth(df, period_type):
    """Calculates YoY or QoQ growth using the recommended 'QE' frequency."""
    if df.empty:
        return pd.Series(dtype='float64')
    
    df_indexed = df.set_index('Date')

    if period_type == 'QoQ':
        quarterly_data = df_indexed['Registrations'].resample('QE').sum()
        return quarterly_data.pct_change(periods=1) * 100
    elif period_type == 'YoY':
        quarterly_data = df_indexed['Registrations'].resample('QE').sum()
        return quarterly_data.pct_change(periods=4) * 100
    return pd.Series(dtype='float64')

def calculate_manufacturer_growth(df, period_type):
    """Calculates YoY or QoQ growth for each manufacturer."""
    if df.empty:
        return pd.DataFrame({'Manufacturer': [], 'Growth': []})

    all_manufacturers = df['Manufacturer'].unique()
    growth_data = []

    for manufacturer in all_manufacturers:
        m_df = df[df['Manufacturer'] == manufacturer]
        growth_series = get_growth(m_df, period_type)
        
        if not growth_series.dropna().empty:
            latest_growth = growth_series.dropna().iloc[-1]
            growth_data.append({'Manufacturer': manufacturer, 'Growth': latest_growth})

    growth_df = pd.DataFrame(growth_data)
    
    # --- ERROR FIX ---
    # If the growth_df is empty (no growth could be calculated), 
    # return an empty DataFrame with the correct columns to prevent a crash.
    if growth_df.empty:
        return pd.DataFrame({'Manufacturer': [], 'Growth': []})

    return growth_df.sort_values(by='Growth', ascending=False).reset_index(drop=True)

def calculate_market_share_over_time(df):
    """Calculates the market share percentage of each manufacturer over time."""
    if df.empty:
        return pd.DataFrame()

    monthly_df = df.groupby([pd.Grouper(key='Date', freq='MS'), 'Manufacturer'])['Registrations'].sum().reset_index()
    total_monthly_registrations = monthly_df.groupby('Date')['Registrations'].transform('sum')
    monthly_df['Market Share %'] = (monthly_df['Registrations'] / total_monthly_registrations) * 100
    
    return monthly_df
