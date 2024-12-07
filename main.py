import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import project0


# Function to create a clustering
def create_cluster(df):
     # Sidebar for cluster configuration
        st.sidebar.header("Clustering Configuration")
        num_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=5)

        # Perform clustering
        clustered_df = cluster_data(df, num_clusters=num_clusters)

        # Display clustered data table
        st.subheader("Clustered Data")
        st.dataframe(clustered_df[['date_time', 'location', 'nature', 'Cluster']])

        # Create and display cluster chart
        st.subheader("Clustering Visualization")
        cluster_chart = create_cluster_chart(clustered_df)
        st.plotly_chart(cluster_chart)

def create_line_chart(data):
    data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
    data_grouped = data.groupby(pd.Grouper(key='date_time', freq='H')).size().reset_index(name='Count')
    fig = px.line(data_grouped, x='date_time', y='Count',
                  title='Incidents Over Time',
                  labels={'date_time': 'Date/Time', 'Count': 'Number of Incidents'})
    return fig
# Main Streamlit app function
def main():
    st.title("Norman PD Incident Data Visualizer")

    url = st.text_input("Enter the URL of the incident PDF:")
    if url:
        df = load_data(url)
        # Count incidents by nature for bar and Clusterings
        nature_counts = df['nature'].value_counts().reset_index()
        nature_counts.columns = ['Nature', 'Count']

        # Chart selection toggle
        chart_type = st.radio(
            "Select Chart Type:",
            ('Bar Chart', 'Clustering', 'Line Chart')
        )

        if chart_type == 'Bar Chart':
            st.subheader("Incident Counts by Nature")
            bar_fig = create_bar_chart(nature_counts)
            st.plotly_chart(bar_fig)

        elif chart_type == 'Clustering':
                st.subheader("Incident Distribution by Nature")
                create_cluster(df)


        elif chart_type == 'Line Chart':
            st.subheader("Incidents Over Time")
            line_fig = create_line_chart(df)
            st.plotly_chart(line_fig)


if _name_ == "_main_":
    main()
