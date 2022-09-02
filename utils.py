from typing import Iterator, List, Union

import matplotlib as mpl
import matplotlib.pyplot as plt 
import cartopy
from cartopy.io import shapereader
from cartopy.crs import CRS
import pandas as pd



# cartopy constants
GLOBAL_EXTEND_EXCLUDE_ANTACTICA = (-180, 180, -60, 90)




# data cleaning and preprocessing utils
NAMES_DATA_TO_MAP = {
    # some country names in WHO's csv data file is not the same as those in Cartopy
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


def extract_value(value_and_range: str) -> float:
    """
    extract float value from Value column

    for example:
    input: "0.16 [0.11 - 0.22]"
    output: 0.16
    """
    return float(value_and_range.split(maxsplit=1)[0])

assert extract_value("0.16 [0.11 - 0.22]") == 0.16
assert extract_value("0 [0 – 0]") == 0




# visualizing utils
def make_scalar_colorbar(bounds: List[int], 
                         color_names: List[str], 
                         ax: plt.Axes, 
                         **kwargs) -> None:
    assert bounds == sorted(bounds)
    assert len(color_names) >= (len(bounds) - 1) 
    cmap = mpl.colors.ListedColormap(color_names)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    plt.colorbar(sm, ax=ax, **kwargs) 

# color_bound_obj = ColorBound(100)
# ax = plt.subplot()
# make_scalar_colorbar(color_bound_obj.get_bounds(), color_bound_obj.get_colors(), ax)
# plt.show()




# cartopy utils
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


def apply_color_to_country(color: str, country: shapereader.Record, ax: plt.Axes, crs: CRS) -> None:
    ax.add_geometries([country.geometry],  # NOTE: expecting a sequence of geometry, so use list
                      crs(),
                      facecolor=color,
                      label=country.attributes['ADM0_A3'])


class ColorBounder:
    """a helper class to match a color for a certain value"""
    def __init__(self, colors: List[str], bounds: List[int]) -> None:
        """
        colors - color names
        bounds - in increasing order

        note:
        for values below the lower bound, the color is 'silver' 
        """
        assert len(colors) == len(set(colors))
        assert len(bounds) == len(set(bounds))
        assert len(colors) == len(bounds)
        assert bounds == sorted(list(bounds))
        assert 'silver' not in set(colors)
        self._colors = ['silver'] + list(colors)
        self._bounds = pd.Series(bounds)

    def find_color(self, x: Union[float, int]) -> str:
        """
        if x < bounds[0], matches 'silver'
        if bounds[i] <= x < bounds[i+1], matches color[i] 
        if bounds[-1] <= x, matches color[-1]
        """
        return self._colors[self._bounds.searchsorted(x, side='right')]

cs = ['green', 'yellow', 'red']
bs = [0, 10, 20]
color_bounder = ColorBounder(cs, bs)
assert color_bounder.find_color(-1) == 'silver'
assert color_bounder.find_color(0) == 'green'
assert color_bounder.find_color(10) == 'yellow'
assert color_bounder.find_color(15) == 'yellow'
assert color_bounder.find_color(100) == 'red'




# data utils
def get_country_name_in_data(name_in_map: str, data: pd.DataFrame) -> str:
    assert 'Location' in data.columns
    result = ''
    if name_in_map in set(data.Location.unique()):
        result = name_in_map 
    # if name_in_map in names_map_to_data:
    if name_in_map in NAMES_MAP_TO_DATA:
        result = NAMES_MAP_TO_DATA[name_in_map] 
    return result


def get_suicide_rate(country_name: str, data: pd.DataFrame) -> float:
    assert 'Location' in data.columns
    assert 'Float_Value' in data.columns
    result = -1 # dummy value for non-existing result
    row = data[data.Location == country_name]
    if not row.empty:
        result = row.Float_Value.to_list()[0]
    return result
