from typing import Iterator

import matplotlib.pyplot as plt 
import cartopy
from cartopy.io import shapereader
import pandas as pd


GLOBAL_EXTEND_EXCLUDE_ANTACTICA = (-180, 180, -60, 90)


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

