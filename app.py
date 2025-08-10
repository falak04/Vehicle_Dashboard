import streamlit as st
import pandas as pd
import plotly.express as px
from data_processor import (
    get_connection,
    setup_database,
    get_filtered_data_from_sql,
    load_unique_values,
    calculate_manufacturer_growth,
    get_growth,
    calculate_market_share_over_time
)
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide",
)

# --- Database Connection and Setup ---
conn = get_connection()
setup_database(conn)

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Dashboard Filters")

    # Date Range Selection
    try:
        min_date_str, max_date_str = pd.read_sql("SELECT MIN(Date), MAX(Date) FROM vehicle_data", conn).iloc[0]
        min_date = datetime.strptime(min_date_str.split(" ")[0], '%Y-%m-%d').date()
        max_date = datetime.strptime(max_date_str.split(" ")[0], '%Y-%m-%d').date()
    except Exception as e:
        st.error("Could not load date range from data. Please check 'sample_vehicle_data.csv'.")
        st.stop()


    date_selection = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # --- ERROR FIX ---
    # The st.date_input can sometimes return a single date instead of a tuple.
    # This check ensures the app doesn't crash with a ValueError.
    if isinstance(date_selection, tuple) and len(date_selection) == 2:
        start_date, end_date = date_selection
    else:
        # If only one date is returned, use it for both start and end.
        start_date = date_selection
        end_date = date_selection


    # Vehicle Category Filter
    all_categories = load_unique_values(conn, 'Vehicle_Type')
    selected_categories = st.multiselect(
        "Select Vehicle Category",
        options=all_categories,
        default=all_categories
    )

    # Manufacturer Filter
    all_manufacturers = load_unique_values(conn, 'Manufacturer')
    default_manufacturers = all_manufacturers[:5] if len(all_manufacturers) > 5 else all_manufacturers
    selected_manufacturers = st.multiselect(
        "Select Manufacturer",
        options=all_manufacturers,
        default=default_manufacturers
    )

# --- Fetch Data using SQL ---
filtered_df = get_filtered_data_from_sql(conn, start_date, end_date, selected_categories, selected_manufacturers)

# --- Main Dashboard ---
st.title("Vehicle Registration Analysis 🇮�")
st.markdown("An interactive dashboard for analyzing vehicle registration trends from an investor's perspective.")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
else:
    # --- Key Metrics ---
    total_registrations = filtered_df['Registrations'].sum()
    yoy_growth_series = get_growth(filtered_df, 'YoY')
    qoq_growth_series = get_growth(filtered_df, 'QoQ')

    latest_yoy = yoy_growth_series.dropna().iloc[-1] if not yoy_growth_series.dropna().empty else 0
    latest_qoq = qoq_growth_series.dropna().iloc[-1] if not qoq_growth_series.dropna().empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registrations", f"{total_registrations:,.0f}")
    col2.metric("Overall YoY Growth (Latest Qtr)", f"{latest_yoy:.2f}%")
    col3.metric("Overall QoQ Growth (Latest Qtr)", f"{latest_qoq:.2f}%")

    st.markdown("---")

    # --- High-Level Market Trends ---
    st.subheader("High-Level Market Trends")
    tab1, tab2 = st.tabs(["Trends by Vehicle Type", "Market Share Evolution"])

    with tab1:
        category_trend_data = filtered_df.groupby(['Date', 'Vehicle_Type'])['Registrations'].sum().reset_index()
        fig_cat_trend = px.line(category_trend_data, x='Date', y='Registrations', color='Vehicle_Type',
                                title='Registration Volume by Vehicle Type',
                                labels={'Registrations': 'Number of Registrations'})
        st.plotly_chart(fig_cat_trend, use_container_width=True)

    with tab2:
        market_share_df = calculate_market_share_over_time(filtered_df)
        fig_market_share = px.area(market_share_df, x='Date', y='Market Share %', color='Manufacturer',
                                   title='Market Share Evolution Over Time',
                                   labels={'Market Share %': 'Market Share (%)'})
        st.plotly_chart(fig_market_share, use_container_width=True)

    st.markdown("---")
    
    # --- Manufacturer Performance Analysis ---
    st.subheader("Manufacturer Performance Analysis")
    
    col_pie, col_placeholder = st.columns([2, 1])
    with col_pie:
        market_share = filtered_df.groupby('Manufacturer')['Registrations'].sum().reset_index()
        fig_pie = px.pie(market_share, names='Manufacturer', values='Registrations', hole=0.4, 
                         title="Current Market Share Snapshot")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Growth Analysis by Manufacturer")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        yoy_manufacturer_growth = calculate_manufacturer_growth(filtered_df, 'YoY')
        fig_yoy = px.bar(yoy_manufacturer_growth, x='Manufacturer', y='Growth', 
                         title='Year-over-Year (YoY) Growth %', color='Growth', 
                         color_continuous_scale='Greens')
        st.plotly_chart(fig_yoy, use_container_width=True)

    with g_col2:
        qoq_manufacturer_growth = calculate_manufacturer_growth(filtered_df, 'QoQ')
        fig_qoq = px.bar(qoq_manufacturer_growth, x='Manufacturer', y='Growth', 
                         title='Quarter-over-Quarter (QoQ) Growth %', color='Growth', 
                         color_continuous_scale='Blues')
        st.plotly_chart(fig_qoq, use_container_width=True)

    with st.expander("View Raw Data Table (from SQL Query)"):
        st.dataframe(filtered_df)