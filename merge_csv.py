import pandas as pd

# Load csv files
station_point = pd.read_csv('StationPoints.csv')
stations = pd.read_csv('Stations.csv')

# Ensure that the key columns are of type string
station_point['StationUniqueId'] = station_point['StationUniqueId'].astype(str)
stations['UniqueId'] = stations['UniqueId'].astype(str)

# Select relevant columns from StationPoints and Stations
station_points_subset = station_point[['StationUniqueId', 'AreaName', 'Lat', 'Lon']].astype(str)
stations_subset = stations[['UniqueId', 'Name']].astype(str)

# Merge the datasets: Match StationUniqueId from StationPoints with UniqueId in Stations
merged_data = pd.merge(
    station_points_subset,
    stations_subset,
    left_on='StationUniqueId',
    right_on='UniqueId',
    how='inner'
).drop(columns=['UniqueId'])

# Remove duplicates by keeping the first occurrence of each StationUniqueId
duplicated_data = merged_data.drop_duplicates(subset=['StationUniqueId'], keep='first')

# Save the deduplicated dataset to a new CSV file
duplicated_data.to_csv('Deduplicated_Merged_Stations.csv', index=False)

print("Processing complete. The deduplicated dataset is saved as 'Deduplicated_Merged_Stations.csv'.")
