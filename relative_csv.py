import pandas as pd
import os
from input_path import InputPath

# Create an instance of the InputPath class
input_path_instance = InputPath()

# Dictionary containing lines and corresponding station names
line_stations = {
    # Piccadilly Line (navy blue)
    'Piccadilly': [
        'Hyde Park Corner',
        'Green Park',
        'Piccadilly Circus',
        'Leicester Square',
        'Covent Garden',
        'Holborn'
    ],

    # Central Line (Red)
    'Central': [
        'Oxford Circus',
        'Tottenham Court Road',
        'Holborn',
        'Liverpool Street',
        'Notting Hill Gate',
        'White City'
    ],
    
    # Victoria Line (Light blue)
    'Victoria': [
        'Green Park',
        'Oxford Circus',
        'Warren Street',
        'Euston',
        'Vauxhall',
        'Brixton',
        'Stockwell'
    ],

    # Bakerloo Line (Brown)
    'Bakerloo': [
        'Oxford Circus',
        'Piccadilly Circus',
        'Charing Cross',
        'Waterloo',
        'Elephant & Castle',
        'Baker Street'
    ],
    #Nothern Line (Black)
    'Nothern':[
        'Charing Cross',
        'Goodge Street',
        'Tottenham Court Road',
        'Leicester Square',
        'Embankment'
    ]
}

try:
    # Retrieve the path to the input CSV
    input_path =input_path_instance.StationCSVPath()
    if not os.path.exists(input_path):
        print(f"File Do Not Exist: {input_path}")
        exit()

    # Read the CSV file
    df = pd.read_csv(input_path)
    print(f"Read {len(df)} lines from file input")
    
    # Combine all station names from the dictionary
    all_stations = [name for line in line_stations.values() for name in line]

    # Filter the dataframe based on station names
    stations = df.loc[df['Name'].isin(all_stations)]
    print(f"Cleaned Stations: {len(stations)}")

    # Write the filtered data to a new CSV file
    output_path = os.path.join(os.getcwd(), 'Relative_Data.csv')
    stations.to_csv(output_path, index=False)
    print(f"Output Succed: {output_path}")

except Exception as e:
    print(f"Error: {str(e)}")
