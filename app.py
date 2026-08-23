import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Churn Presentation", layout="wide")

st.title("📉 Customer Churn Analysis Presentation")

@st.cache_data
def load_data():
    return pd.read_excel("customer_churn_business_dataset.xlsx")

try:
    df = load_data()
    st.success("Successfully connected to customer_churn_business_dataset.xlsx!")
    
    
    # SIDEBAR FILTERS
    
    st.sidebar.header("Filter Options")
    
    segment_options = ["All"] + list(df['customer_segment'].unique())
    selected_segment = st.sidebar.selectbox("Select Customer Segment", segment_options)
    
    country_options = ["All"] + list(df['country'].unique())
    selected_country = st.sidebar.selectbox("Select Country", country_options)
    
    # Apply Filters
    filtered_df = df.copy()
    if selected_segment != "All":
        filtered_df = filtered_df[filtered_df['customer_segment'] == selected_segment]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
        
    
    # SECTION 1: KEY PERFORMANCE INDICATORS
    
    st.subheader(f"1. Executive Overview ({selected_segment} Segment | {selected_country})")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Customers", f"{len(filtered_df):,}")
    col2.metric("Avg Tenure (Months)", f"{filtered_df['tenure_months'].mean():.1f}")
    col3.metric("Avg Monthly Logins", f"{filtered_df['monthly_logins'].mean():.1f}")
    col4.metric("Avg Session Time (Min)", f"{filtered_df['avg_session_time'].mean():.1f}")
    
    st.markdown("---")
    
    
    # SECTION 2: ACQUISITION & CONTRACT BREAKDOWN
    
    st.subheader("2. Contract & Acquisition Channels")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("**Customer Distribution by Contract Type**")
        st.bar_chart(filtered_df['contract_type'].value_counts())
        
    with col_chart2:
        st.write("**Customer Distribution by Signup Channel**")
        st.bar_chart(filtered_df['signup_channel'].value_counts())
        
    st.markdown("---")
    
    
    # SECTION 3: DEMOGRAPHICS & ENGAGEMENT INSIGHTS
    
    st.subheader("3. Customer Demographics & Loyalty Duration")
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.write("**Average Tenure (Months) by Customer Segment**")
        tenure_by_seg = filtered_df.groupby('customer_segment')['tenure_months'].mean()
        st.bar_chart(tenure_by_seg)
        
    with col_chart4:
        st.write("**Average Weekly Active Days by Signup Channel**")
        active_days_by_channel = filtered_df.groupby('signup_channel')['weekly_active_days'].mean()
        st.bar_chart(active_days_by_channel)
        
    st.markdown("---")
    
    
    # SECTION 4: DATA TABLE PREVIEW
    
    st.subheader("4. Filtered Dataset Explorer")
    st.dataframe(filtered_df.head(15))
    
except Exception as e:
    st.error(f"Error loading file: {e}")