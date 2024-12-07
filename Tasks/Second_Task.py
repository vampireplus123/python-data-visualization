import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Function to calculate Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Load data
csv_path = 'Relative_Data.csv'
df = pd.read_csv(csv_path)

# Create new graph
G = nx.Graph()

# Define stations and lines
lines = {
    "piccadilly": ["Hyde Park Corner", "Green Park", "Piccadilly Circus", 
                   "Leicester Square", "Holborn", "Covent Garden"],
    "central": ["White City", "Notting Hill Gate", "Oxford Circus", 
                "Tottenham Court Road", "Holborn", "Liverpool Street"],
    "victoria": ["Brixton","Stockwell","Vauxhall","Green Park","Oxford Circus","Warren Street","Euston"],
    "bakerloo": ["Baker Street", "Oxford Circus", "Piccadilly Circus", 
                 "Charing Cross", "Waterloo", "Elephant & Castle"],
    "northern": ["Euston", "Goodge Street", 
                "Tottenham Court Road", "Leicester Square", 
                "Charing Cross", "Embankment"]
}

station_positions = {
    "Hyde Park Corner": (0, -1),
    "Green Park": (1, 0),
    "Piccadilly Circus": (2, 0),
    "Leicester Square": (3, 0),
    "Covent Garden": (4, 1),
    "Holborn": (5, 2),
    "Oxford Circus": (1.5, 1),
    "Tottenham Court Road": (3, 1),
    "Liverpool Street": (7, 1),
    "Baker Street": (0, 2),
    "Waterloo": (4, -1),
    "Elephant & Castle": (5, -2),
    "Notting Hill Gate": (0, 0.5),
    "White City": (-1.5, 0.5),
    "Vauxhall": (1,-2),
    "Stockwell": (1,-3),
    "Brixton": (1,-4),
    "Euston": (3, 4),
    "Warren Street": (3, 3),
    "Goodge Street": (3, 2),
    "Charing Cross": (3, -1),
    "Embankment": (3, -2)
}

# Custom label positions for each station
label_positions = {}
for station, (x, y) in station_positions.items():
    if "Street" in station:
        label_positions[station] = (x - 0.4, y)  # Move labels left for streets
    elif "Square" in station:
        label_positions[station] = (x + 0.4, y)  # Move labels right for squares
    elif y > 0:
        label_positions[station] = (x, y - 0.4)  # Labels below for northern stations
    else:
        label_positions[station] = (x, y + 0.4)  # Labels above for southern stations

# Add edges with distances
for line_name, stations in lines.items():
    for i in range(len(stations) - 1):
        station1, station2 = stations[i], stations[i + 1]
        s1_data = df[df['Name'] == station1].iloc[0]
        s2_data = df[df['Name'] == station2].iloc[0]
        distance = round(haversine_distance(s1_data['Lat'], s1_data['Lon'], 
                                         s2_data['Lat'], s2_data['Lon']), 2)
        G.add_edge(station1, station2, distance=distance, line=line_name)

# Drawing function
def draw_graph():
    plt.figure(figsize=(15, 10))
    
    # Draw edges for each line
    for line_name, color in zip(lines.keys(), ['blue', 'red', 'lightblue', 'brown', 'black']):
        edge_list = [(u, v) for u, v, d in G.edges(data=True) if d['line'] == line_name]
        nx.draw_networkx_edges(G, pos=station_positions, edgelist=edge_list, 
                             edge_color=color, label=line_name.capitalize(),
                             width=2)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos=station_positions, 
                          node_color='white', 
                          node_size=700,
                          edgecolors='black')
    
    # Draw labels with custom positions
    nx.draw_networkx_labels(G, pos=label_positions, 
                          font_size=8,
                          font_weight='bold')

    # Add edge labels
    edge_labels = nx.get_edge_attributes(G, 'distance')
    nx.draw_networkx_edge_labels(G, station_positions, 
                               edge_labels,
                               font_size=7,
                               label_pos=0.3)

    plt.legend(loc="upper left", title="Lines")
    plt.title("London Underground Lines (Distances in km)", pad=20, fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# Run the visualization
draw_graph()



# Print distances for all lines
for line_name, stations in lines.items():
    print(f"\n{line_name.capitalize()} Line distances:")
    for u, v, d in G.edges(data=True):
        if d['line'] == line_name:
            print(f"{u} -> {v}: {d['distance']} km")

print("New task")
victoria_stations = []
for u, v, d in G.edges(data=True):
    # print(u, v, d)
    # print("-------------------")
    if d['line'] == 'victoria':
        # print(u,v,d)
        victoria_stations.append(u)
        victoria_stations.append(v)
print(set(victoria_stations))



