import pandas as pd
import networkx as nx
import numpy as np
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Bán kính trái đất (km)
    return c * r


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

def calculate_network_statistics():

    df = pd.read_csv('Relative_Data.csv')
    
  
    G = nx.Graph()
    
    total_distance = 0
    distances = []
    
    for line_name, stations in lines.items():
        for i in range(len(stations)-1):
            station1 = stations[i]
            station2 = stations[i+1]
            
            try:
                # station position
                s1_data = df[df['Name'] == station1].iloc[0]
                s2_data = df[df['Name'] == station2].iloc[0]
                
                # Calculate distance
                distance = haversine_distance(
                    s1_data['Lat'], s1_data['Lon'],
                    s2_data['Lat'], s2_data['Lon']
                )
                
                # Adding edge
                G.add_edge(station1, station2, distance=distance, line=line_name)
                distances.append(distance)
                total_distance += distance
                
            except IndexError:
                print(f"Không tìm thấy dữ liệu cho trạm {station1} hoặc {station2}")
                continue
    
    # calculate
    avg_distance = np.mean(distances) if distances else 0
    std_distance = np.std(distances) if distances else 0
    
    # result
    print(f"Total length of the transport network: {total_distance:.2f} km")
    print(f"Average distance between stations: {avg_distance:.2f} km")
    print(f"Standard deviation of distances: {std_distance:.2f} km")
    
    return G

def main():
    G = calculate_network_statistics()

if __name__ == "__main__":
    main()
