import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import proj0_incidents
import matplotlib.pyplot as plt
import seaborn as sns
import io

def create_heatmap(data):
    # Ensure `date_time` is parsed correctly
    data["incident_time"] = pd.to_datetime(data["incident_time"], errors="coerce")
    data = data.dropna(subset=["incident_time"])
    
    # Extract day of the week and hour
    data["Day of Week"] = data["incident_time"].dt.day_name()
    data["Hour"] = data["incident_time"].dt.hour
    
    # Create a pivot table
    heatmap_data = data.pivot_table(
        index="Day of Week", 
        columns="Hour", 
        values="incident_number",  # Use a non-null column to count occurrences
        aggfunc="count"
    ).fillna(0)
    
    # Reorder days of the week
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = heatmap_data.reindex(days_order)
    
    # Plot the heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", cbar=True)
    plt.title("Incident Frequency by Time of Day and Day of Week", fontsize=16)
    plt.xlabel("Hour of Day", fontsize=12)
    plt.ylabel("Day of Week", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(plt)
def main():
    st.title("NormanPD Incident Data Viewer")

    # Sidebar: Upload file or enter URL
    st.sidebar.header("Data Input")
    option = st.sidebar.radio("Choose Input Method:", ("Upload PDF", "Enter URL"))
    
    if option == "Upload PDF":
        uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file:
            pdf_data = uploaded_file.read()
            pdf_stream=io.BytesIO(pdf_data)
            incidents = proj0_incidents.extractPDFData(pdf_stream)
            db = proj0_incidents.createdb()
            proj0_incidents.populatedb(incidents,db)
            data = proj0_incidents.fetch_all_data()
            visualize_data(data)
    
    elif option == "Enter URL":
        url = st.sidebar.text_input("Enter the URL of the incident PDF:")
        if url:
            pdf_data = proj0_incidents.fetchPDFData(url)
            incidents = proj0_incidents.extractPDFData(pdf_data)
            db = proj0_incidents.createdb()
            proj0_incidents.populatedb(incidents,db)
            data = proj0_incidents.fetch_all_data()
            visualize_data(data)

def visualize_data(data):
    st.header("Incident Report Insights")

    # Visualize incident types
    st.subheader("Frequency of Incident Types")
    visualize_incident_types(data)

    # Visualize incidents over time
    st.subheader("Incident Distribution by Hour")
    visualize_incidents_over_time(data)

    # Visualize top locations
    st.subheader("Top 10 Locations for Incidents")
    visualize_top_locations(data)

    # Visualize incident nature by location
    st.subheader("Incident Nature by Location")
    visualize_nature_by_location(data)

    # Visualize responding agencies
    st.subheader("Responding Agencies")
    visualize_response_agencies(data)


def visualize_incident_types(data):
    nature_counts = data["nature"].value_counts().reset_index()
    nature_counts.columns = ["Nature", "Count"]

    fig = px.bar(
        nature_counts,
        x="Nature",
        y="Count",
        title="Frequency of Incident Types",
        labels={"Nature": "Incident Type", "Count": "Number of Incidents"},
        height=600
    )
    st.plotly_chart(fig)

def visualize_incidents_over_time(data):
    data["incident_time"] = pd.to_datetime(data["incident_time"], errors="coerce")
    hourly_data = data.groupby(data["incident_time"].dt.hour).size().reset_index(name="Count")
    hourly_data.columns = ["Hour", "Count"]

    fig = px.line(
        hourly_data,
        x="Hour",
        y="Count",
        title="Incident Distribution by Hour",
        labels={"Hour": "Hour of Day", "Count": "Number of Incidents"},
        height=600
    )
    st.plotly_chart(fig)

def visualize_top_locations(data):
    location_counts = data["incident_location"].value_counts().head(10).reset_index()
    location_counts.columns = ["Location", "Count"]

    fig = px.bar(
        location_counts,
        x="Location",
        y="Count",
        title="Top 10 Locations for Incidents",
        labels={"Location": "Incident Location", "Count": "Number of Incidents"},
        height=600
    )
    st.plotly_chart(fig)

def visualize_nature_by_location(data):
    # Get top 10 locations
    top_locations = data["incident_location"].value_counts().head(10).index
    filtered_data = data[data["incident_location"].isin(top_locations)]

    # Group by location and nature
    grouped_data = filtered_data.groupby(["incident_location", "nature"]).size().reset_index(name="Count")

    # Plot the stacked bar chart
    fig = px.bar(
        grouped_data,
        x="incident_location",  # Use the correct column name
        y="Count",
        color="nature",
        title="Incident Nature by Top Locations",
        labels={
            "incident_location": "Incident Location",
            "Count": "Number of Incidents",
            "nature": "Incident Nature"
        },
        barmode="stack",
        height=600
    )
    st.plotly_chart(fig)


def visualize_response_agencies(data):
    agency_counts = data["incident_ori"].value_counts().reset_index()
    agency_counts.columns = ["Agency", "Count"]

    fig = px.pie(
        agency_counts,
        names="Agency",
        values="Count",
        title="Distribution of Incidents by Responding Agency",
        hole=0.4  # Creates a donut chart
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
