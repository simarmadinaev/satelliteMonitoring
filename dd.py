import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Set the page layout to wide to minimize gaps
st.set_page_config(layout="wide")

# Load the dataset 
file_path = 'data2.csv'
df = pd.read_csv(file_path)

# Combine the date and time into a single datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Set the datetime column as the index
df.set_index('datetime', inplace=True)

# Streamlit UI components
st.title("Interactive Monitoring Dashboard ")

# Get unique devices
unique_devices = df['device'].unique()

# Loop through all columns that are not 'datetime', 'date', 'time', or 'device' to create graphs
metrics_columns = [col for col in df.columns if col not in ['date', 'time', 'device']]

# Generate a color palette with enough colors for all metrics and convert them to hex
colors = plt.get_cmap('tab10').colors  # Get colors as tuples
hex_colors = [mcolors.rgb2hex(color) for color in colors]  # Convert to hex

# Loop through each metric and create a section for it
for metric in metrics_columns:
    # Create a section header for each metric
    st.header(f"{metric.capitalize()} over Time by Device")
    
    # Create a 2-column layout for the graphs of each device
    cols = st.columns(2)
    
    # Loop through each device and create a graph for the current metric
    for i, device in enumerate(unique_devices):
        # Filter data for the current device
        filtered_data = df[df['device'] == device]
        
        # Plot the data for the current metric and device
        with cols[i % 2]:
            fig = px.line(filtered_data, 
                          x=filtered_data.index, 
                          y=metric, 
                          title=f'{device} - {metric.capitalize()}',
                          color_discrete_sequence=[hex_colors[i % len(hex_colors)]])  # Assign color
            fig.update_layout(width=450, height=300)
            st.plotly_chart(fig)
