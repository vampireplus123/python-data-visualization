import pandas as pd

df = pd.read_csv('Deduplicated_Merged_Stations.csv')
stations = df.loc[df['Name'].isin(['Hyde Park Corner', 'Green Park', 
                                   'Piccadilly Circus', 'Leicester Square', 
                                   'Convent Garden', 'Holborn'])]

print(df.columns)
print(stations)
stations.to_csv('Relative_Data.csv',index=False)

