# cis6930fa24-project3

# Project Description
This project involves fetching data from a given URL to a PDF file, extracting specific fields from the PDF, formatting the data, and inserting it into a database. A database named normanpd.db is created with a table called incidents to store the extracted data. The project also includes querying the table to generate a list of the nature of incidents and the number of times they have occurred. Additionally, this project now includes visualization of the data and a web interface for user interaction.

# How to run
streamlit run main.py

# video


#Function Description
### proj0_incidents.py
    fetchPDFData(url): This function takes the url as a parameter and fetches the pdf data from the url link as a stream
    extractPDFData(data): This function takes the above fetched data and extracts it to raw string format and then formats the data so that it can be inserted into a database table
    createdb(): This function created a database named normanpd.db and established a connection to that database and also created a table named 'incidents' in the database
    populatedb(data,db): This function takes the formatted data and db connection as parameters and populates the table 'incidents' with the provided data
    status(db): This function takes db connection as parameter and queries the 'incident' table to get a list of the nature of incidents and the number of times they have occured
    query_db(query,db_path): This function executes a given SQL query on the normanpd.db database and returns the result as a Pandas DataFrame. It establishes a connection to the database, runs the query, retrieves the data, and then closes the connection.
    fetch_all_data(): This function retrieves all records from the incidents table in the normanpd.db database. It determines the absolute path to the database file, executes a SQL query to fetch all data, and returns the results as a Pandas DataFrame.

### main.py
Main Functions

    main(): This is the main function that initializes the Streamlit web application. It provides a sidebar for users to either upload a PDF file or enter a URL to fetch incident data. Based on the input, it processes the data, populates the database, and calls the visualize_data() function to generate insights.
    visualize_data(data): This function takes the incident data as input and generates various visualizations, such as frequency of incident types, distribution by hour, top locations, nature of incidents by location, and responding agencies. It acts as a central hub for calling specific visualization functions.

Data Input Functions

    create_heatmap(data): Generates a heatmap showing the frequency of incidents by hour and day of the week. It processes the incident_time column to extract relevant time features and uses Seaborn to plot the heatmap.
    visualize_incident_types(data): Creates a bar chart using Plotly to display the frequency of different incident types (nature). This helps identify which types of incidents occur most frequently.
    visualize_incidents_over_time(data): Plots a line graph using Plotly to show how incidents are distributed across different hours of the day. It helps in understanding peak hours for incidents.
    visualize_top_locations(data): Displays a bar chart with the top 10 locations where incidents occurred most frequently. This visualization helps in identifying high-incident areas.
    visualize_nature_by_location(data): Generates a stacked bar chart using Plotly to show the distribution of different incident natures at the top 10 locations. This provides insights into the types of incidents occurring in specific areas.
    visualize_response_agencies(data): Creates a donut chart (pie chart with a hole) using Plotly to visualize the distribution of incidents handled by different responding agencies (incident_ori). It highlights which agencies are most active in responding to incidents.

# Database Development
Created a Database named 'normanpd.db' with the following fields : incident_time, incident_number, incident_location, nature, incident_ori

# Assumptions
It is assumed that the nature field in the dataset is not multi-line.