import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Load the dataset
    data = pd.read_csv('Final_ds.csv')
    return data

def plot_employment_status(df):
    fig, ax = plt.subplots()
    df['employment status'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Employment Status Distribution')
    ax.set_xlabel('Employment Status')
    ax.set_ylabel('Frequency')
    return fig

def plot_work_absence_reason(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_reasons = df['reason for work absence last week'].value_counts().nlargest(5)
    top_reasons.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Top 5 Reasons for Work Absence Last Week')
    ax.set_xlabel('Reason')
    ax.set_ylabel('Frequency')

    # Add values on top of the bars for better readability
    for i, value in enumerate(top_reasons.values):
        ax.text(i, value + 1, str(value), ha='center', va='bottom')

    return fig

def plot_college_credit_completed(df):
    fig, ax = plt.subplots()
    df['college credit completed'].value_counts().plot(kind='bar', color='lightcoral', ax=ax)
    ax.set_title('College Credit Completed Distribution')
    ax.set_xlabel('Credits')
    ax.set_ylabel('Frequency')
    return fig

def plot_layoff_cities(df):
    # Filter and count layoffs
    layoff_data = df[df['(layoff)from full-time job,y/n'] == 1]
    
    if layoff_data.empty:
        # Handle the case where no data matches the filter
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No layoff data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Top 10 Cities with Most Layoffs')
        ax.set_xlabel('City')
        ax.set_ylabel('Layoffs')
        ax.axis('off')  # Turn off axis if no data
        return fig
    else:
        top_cities = layoff_data['First City'].value_counts().nlargest(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        top_cities.plot(kind='barh', color='orange', ax=ax)
        
        ax.set_title('Top 10 Cities with Most Layoffs')
        ax.set_xlabel('Number of Layoffs')
        ax.set_ylabel('City')

        # Add values at the end of the bars for better readability
        for i, value in enumerate(top_cities.values):
            ax.text(value + 1, i, str(value), va='center')

        return fig
    
def plot_business_farm_distribution(df):
    # Check if the column has enough data to plot
    if 'business/farm in hhld' not in df.columns or df['business/farm in hhld'].isna().all():
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No data available for Business/Farm in HHLD', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Business/Farm in Household Distribution')
        ax.axis('off')
        return fig
    else:
        fig, ax = plt.subplots(figsize=(8, 8))
        df['business/farm in hhld'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title('Business/Farm in Household Distribution')
        ax.set_ylabel('')
        return fig
def plot_job_search_time_series(df):
    # Ensure the column names are corrected as per your dataset's actual column names
    if 'year-month' in df.columns and "unemployed)weeks on job search" in df.columns:
        # Convert date column to datetime
        df['year-month'] = pd.to_datetime(df['year-month'])

        # Group by Year-Month and calculate the average
        time_data = df.groupby('year-month')["unemployed)weeks on job search"].mean()

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        time_data.plot(kind='line', marker='o', color='purple', ax=ax)
        ax.set_title('Average Weeks on Job Search Over Time')
        ax.set_xlabel('Year-Month')
        ax.set_ylabel('Average Weeks on Job Search')
        ax.grid(True)
        return fig
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Required data columns are missing', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Data Error')
        ax.axis('off')
        return fig

def main():
    st.title("Data Analysis Dashboard")

    df = load_data()

    # First row of plots
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_employment_status(df))
    with col2:
        st.pyplot(plot_work_absence_reason(df))

    # Second row of plots
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_college_credit_completed(df))
    with col2:
        st.pyplot(plot_layoff_cities(df))

    # Third row of plots
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_business_farm_distribution(df))
    with col2:
        st.pyplot(plot_job_search_time_series(df))

if __name__ == "__main__":
    main()