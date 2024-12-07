import csv
import math
from itertools import combinations

# Haversine formula to calculate the distance between two points on the Earth
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Distance in kilometers
    return R * c

# Read the CSV file and extract station coordinates
stations = []
with open('Relative_Data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        stations.append((row['Name'], float(row['Lat']), float(row['Lon'])))

# Calculate pairwise distances between all stations
distances = []
for (name1, lat1, lon1), (name2, lat2, lon2) in combinations(stations, 2):
    distance = haversine(lat1, lon1, lat2, lon2)
    distances.append(distance)

# Calculate total length of the network
total_length = sum(distances)

# Calculate the average distance
average_distance = total_length / len(distances)

# Calculate the standard deviation of the distances
variance = sum((d - average_distance) ** 2 for d in distances) / len(distances)
std_deviation = math.sqrt(variance)

# Print results
print(f"Total length of the transport network: {total_length:.2f} km")
print(f"Average distance between stations: {average_distance:.2f} km")
print(f"Standard deviation of distances: {std_deviation:.2f} km")
