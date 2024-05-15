import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Load the dataset
    data = pd.read_csv('Final_ds.csv')
    return data

def plot_employment_status(df):
    status_description = {
        1: 'Employed - At Work',
        2: 'Employed - Absent',
        3: 'Unemployed - Looking',
        4: 'Unemployed - Not Looking',
        5: 'Not in Labor Force',
        6: 'Disabled - Not In Labor Force',
        7: 'Other - Not In Labor Force'
    }

    fig, ax = plt.subplots()
    df['employment status'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Employment Status Distribution')
    ax.set_xlabel('Employment Status')
    ax.set_ylabel('Frequency')

    legend_text = '\n'.join([f"{key}: {value}" for key, value in status_description.items()])
    plt.text(0.95, 0.95, legend_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', fontsize=8, bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))

    plt.tight_layout()
    return fig

def plot_work_absence_reason(df):
    reason_descriptions = {
        "3": "Waiting For A New Job To Begin",
        "12": "Civic/Military Duty",
        "13": "Does Not Work In The Business",
        "8": "Maternity/Paternity Leave",
        "7": "Other Family/Personal Obligation",
        "9": "Labor Dispute",
        "5": "Own Illness/Injury/Medical Problems",
        "2": "Slack Work/Business Conditions",
        "14": "Other (specify)",
        "-1": "Not in Universe",
        "6": "Child Care Problems",
        "10": "Weather Affected Job",
        "4": "Vacation/Personal Days",
        "11": "School/Training",
        "1": "On Layoff"
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    top_reasons = df['reason for work absence last week'].value_counts().nlargest(5)
    top_reasons.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Top 5 Reasons for Work Absence Last Week')
    ax.set_xlabel('Reason')
    ax.set_ylabel('Frequency')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    for i, value in enumerate(top_reasons.values):
        ax.text(i, value + 1, str(value), ha='center', va='bottom')

    legend_text = '\n'.join([f"{key}: {value}" for key, value in reason_descriptions.items()])
    plt.text(0.95, 0.95, legend_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', fontsize=8, bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))

    plt.tight_layout()
    return fig

def plot_college_credit_completed(df):
    credit_descriptions = {
        "1": "Less than 1 year (includes 0 years completed)",
        "5": "Four or more years",
        "4": "The third, or Junior year",
        "3": "The second, or Sophomore year",
        "-1": "Not in Universe",
        "2": "The first, or Freshman year"
    }

    fig, ax = plt.subplots()
    df['college credit completed'].value_counts().plot(kind='bar', color='lightcoral', ax=ax)
    ax.set_title('College Credit Completed Distribution')
    ax.set_xlabel('College Credit Completed')
    ax.set_ylabel('Frequency')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    legend_text = '\n'.join([f"{key}: {value}" for key, value in credit_descriptions.items()])
    plt.text(0.95, 0.95, legend_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', fontsize=8, bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', alpha=0.5))

    plt.tight_layout()
    return fig

def plot_layoff_cities(df):
    layoff_data = df[df['(layoff)from full-time job,y/n'] == 1]
    
    if layoff_data.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No layoff data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Top 10 Cities with Most Layoffs')
        ax.set_xlabel('City')
        ax.set_ylabel('Layoffs')
        ax.axis('off')
        return fig
    else:
        top_cities = layoff_data['First City'].value_counts().nlargest(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        top_cities.plot(kind='barh', color='orange', ax=ax)
        
        ax.set_title('Top 10 Cities with Most Layoffs')
        ax.set_xlabel('Number of Layoffs')
        ax.set_ylabel('City')

        for i, value in enumerate(top_cities.values):
            ax.text(value + 1, i, str(value), va='center')

        return fig

def plot_business_farm_distribution(df):
    descriptions = {
        "1": "Yes",
        "2": "No",
        "-3": "Refused",
        "-2": "Don't Know",
        "-1": "Blank"
    }

    if 'business/farm in hhld' not in df.columns or df['business/farm in hhld'].isna().all():
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No data available for Business/Farm in HHLD', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title('Business/Farm in Household Distribution')
        ax.axis('off')
        return fig
    else:
        fig, ax = plt.subplots(figsize=(8, 8))
        pie_data = df['business/farm in hhld'].value_counts()
        labels = [descriptions.get(str(index), index) for index in pie_data.index]
        wedges, texts, autotexts = plt.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('Business/Farm in Household Distribution')
        plt.ylabel('')

        plt.legend(wedges, labels, title="Status", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        return fig

def plot_job_search_time_series(df):
    if 'year-month' in df.columns and "unemployed)weeks on job search" in df.columns:
        df['year-month'] = pd.to_datetime(df['year-month'])

        time_data = df.groupby('year-month')["unemployed)weeks on job search"].mean()

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
