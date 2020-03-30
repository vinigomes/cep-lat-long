import googlemaps
import pandas as pd
import os

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def convert_csv_with_cep_to_latitude_longitude(df):
    return pd.concat(
        (
            df,
            df['CEP'].apply(lambda cell: pd.Series(convert_cep_to_latitude_longitude(cell), index=['lat', 'long']))
        )
        , axis=1
    )


def convert_cep_to_latitude_longitude(cep):
    if cep:
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(address=cep, region="BR")
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            return lat, lng
    return 0, 0
