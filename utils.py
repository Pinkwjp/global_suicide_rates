import pandas as pd


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


