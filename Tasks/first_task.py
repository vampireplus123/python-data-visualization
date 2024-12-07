import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    The result is returned in kilometers.
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Earth's radius in kilometers
    r = 6371
    
    return c * r


# Read the CSV file
df = pd.read_csv('Relative_Data.csv')

# Creating a graph for the Piccadilly line
G = nx.Graph()
NewNodeGraph = nx.Graph()
# Adding stations as nodes
stations = [
    "Hyde Park Corner",
    "Green Park",
    "Piccadilly Circus",
    "Leicester Square",
    "Covent Garden", 
    "Holborn",
]


# Calculate edges with actual distances from the CSV data
edges = []
for i in range(len(stations)-1):
    station1 = stations[i]
    station2 = stations[i+1]
    
    # Get coordinates for station1
    s1_data = df[df['Name'] == station1].iloc[0]
    lat1, lon1 = s1_data['Lat'], s1_data['Lon']
    
    # Get coordinates for station2
    s2_data = df[df['Name'] == station2].iloc[0]
    lat2, lon2 = s2_data['Lat'], s2_data['Lon']
    
    # Calculate the distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    # Round to 2 decimal places
    distance = round(distance, 2)
    
    edges.append((station1, station2, distance))

# Adding nodes and edges to the graph
G.add_nodes_from(stations)
for u, v, distance in edges:
    G.add_edge(u, v, distance=distance)

# Adjusting positions to match the desired layout
final_positions = {
    "Hyde Park Corner": (0, -1),  # Below Green Park
    "Green Park": (1, 0),
    "Piccadilly Circus": (2, 0),
    "Leicester Square": (3, 0),
    "Covent Garden":(4,1),
    "Holborn": (5, 2)
}

label_positions = {
    "Hyde Park Corner": (0.5, -1),      
    "Green Park": (1, 0.3),             
    "Piccadilly Circus": (2, 0.3), 
    "Leicester Square": (3, 0.3),       
    "Covent Garden":(4.5,1),
    "Holborn": (5.5, 2),
}


plt.figure(figsize=(12, 8))

# Draw edges
nx.draw_networkx_edges(G, pos=final_positions, edge_color='blue')

# Draw nodes
nx.draw_networkx_nodes(G, pos=final_positions, node_color='blue', node_size=700)

# Draw labels with custom positions
nx.draw_networkx_labels(G, pos=label_positions, font_size=10, font_color='black')

# Adding edge labels (distances)
edge_labels = nx.get_edge_attributes(G, 'distance')
nx.draw_networkx_edge_labels(G, pos=final_positions, edge_labels=edge_labels)

# Adding the legend
plt.gca().add_patch(plt.Rectangle((4.5, -2.5), 2, 1, edgecolor='black', facecolor='white', lw=1))
plt.text(5.5, -1.8, "Key", fontsize=10, color="black", ha='center')
plt.plot([4.7, 5.7], [-2.2, -2.2], color="blue", lw=2)
plt.text(5.8, -2.3, "Piccadilly", fontsize=10, color="blue", ha='left')

# Final adjustments
plt.title("Piccadilly Line (Distances in km)", fontsize=12)
plt.axis("off")
plt.tight_layout()
plt.show()

# Output the distances between stations for verification
print("\nDistances between stations:")
for edge in edges:
    print(f"{edge[0]} -> {edge[1]}: {edge[2]} km")
