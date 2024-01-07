import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def collab_breakdown_timeseries(df):
    # Convert month and year to a datetime object for plotting
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))

    # Sort by date for time series plotting
    df = df.sort_values('date')

    # Plotting
    plt.figure(figsize=(15, 6))
    sns.lineplot(data=df, x='date', y='count', hue='collaborative_working')
    plt.title('Collaborative Working Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Collaborations')
    plt.yscale('log')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
