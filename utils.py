from typing import Iterator

import matplotlib.pyplot as plt 
import cartopy
from cartopy.io import shapereader
import pandas as pd


GLOBAL_EXTEND_EXCLUDE_ANTACTICA = (-180, 180, -60, 90)


# some country names in WHO's csv data file is not the same as those in Cartopy
NAMES_DATA_TO_MAP = {
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

NAMES_MAP_TO_DATA = {value: key for (key, value) in NAMES_DATA_TO_MAP.items()}


# utils for cartopy
def add_basic_map_features(ax: plt.Axes) -> None:
    ax.coastlines()
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND)
    ax.add_feature(cartopy.feature.BORDERS)


def set_map_extend(ax: plt.Axes) -> None:
    ax.set_extent(GLOBAL_EXTEND_EXCLUDE_ANTACTICA, 
                  cartopy.crs.PlateCarree()) 


def countries_iterator() -> Iterator[shapereader.Record]:
    """return an iterator of countries"""
    shpfilename = shapereader.natural_earth(resolution='110m',
                                            category='cultural',
                                            name='admin_0_countries')
    reader = shapereader.Reader(shpfilename)
    countries = reader.records()
    return countries

# TODO: maybe this should not be in util
# utils for data
def get_country_suicide_rate(country_name: str, data: pd.DataFrame) -> float:
    """
    return suicide rate of a country 
    
    Note: 
    return -1, if the country name doesn't exist in data.
    """
    assert 'Location' in data.columns
    assert 'Value' in data.columns
    country_df = data[data.Location == country_name]
    if country_df.empty:
        return -1
    return country_df.Value.to_list()[0]

