# Note: 
# For some countries, the name in WHO's csv data file is not the same as  
# those in Cartopy, so the following mapping serve to solve the conflicts.

names_data_to_map = {
    'Bahamas': 'The Bahamas',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Brunei Darussalam': 'Brunei',
    'Congo': 'Republic of the Congo',
    'Czechia': 'Czech Republic',
    'Côte d’Ivoire': 'Ivory Coast',
    'China': "People's Republic of China",
    "Democratic People's Republic of Korea": 'North Korea',
    'Eswatini': 'Eswatini',
    'Gambia': 'The Gambia',
    'Iran (Islamic Republic of)': 'Iran',
    "Lao People's Democratic Republic": 'Laos',
    'Republic of Moldova': 'Moldova',
    'Russian Federation': 'Russia',
    'Republic of Korea': 'South Korea',
    'Syrian Arab Republic': 'Syria',
    'The former Yugoslav Republic of Macedonia': 'North Macedonia',
    'Timor-Leste': 'East Timor',
    'Türkiye': 'Turkey',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'United Republic of Tanzania': 'Tanzania',
    'United States of America': 'United States of America',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Viet Nam': 'Vietnam'
}

names_map_to_data = {value: key for (key, value) in names_data_to_map.items()}