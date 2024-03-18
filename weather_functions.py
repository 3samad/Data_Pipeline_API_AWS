import json
import pandas as pd
import requests
import os

def clean_weather_df(df):    
    numeric_columns = ['temp', 'rain_3_hours_past_mm','snow_3_hours_past_mm']
    datetime_columns = ['forecast_time', 'updated']

    for measure in numeric_columns:
        df[measure] = pd.to_numeric(df[measure])
    for dt in datetime_columns:
        df[dt] = pd.to_datetime(df[dt])
    print("The weather has been forcast and cleaned!")
    return df
    
def get_weather(df):
    key = os.environ["open_weather_API_key"]
    from datetime import datetime
    import pytz
    df_out = pd.DataFrame()
    for i, series in df.iterrows():
        parameters = {
            "lat": series["latitude"],
            "lon": series["longitude"],
            "appid": key,
            "units": "metric"
            }
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        weather = requests.get(url, params=parameters)
        if weather.status_code == 200:
            weather_json = weather.json()
            tz = pytz.timezone('Europe/Berlin')
            now = datetime.now().astimezone(tz)
            temp_dict = {}
            # the .name attribute accesses the index of the row, allowing us to carry the city_id forward to our weather table
            temp_dict["city_id"] = [series.name for time in weather_json["list"]]  
            temp_dict["forecast_time"] = [time.get("dt_txt") for time in weather_json["list"]]
            temp_dict["temp"] = [time["main"].get("temp") for time in weather_json["list"]]
            temp_dict["description"] = [time["weather"][0].get("description") for time in weather_json["list"]]
            temp_dict["rain_3_hours_past_mm"] = [time.get("rain", {'3h': 0.0})["3h"] for time in weather_json["list"]]
            temp_dict["snow_3_hours_past_mm"] = [time.get("snow", {'3h': 0.0})["3h"] for time in weather_json["list"]]
            temp_dict["updated"] = [now for time in weather_json["list"]]
            temp_df = pd.DataFrame(temp_dict).pipe(clean_weather_df)
            df_out = pd.concat([df_out, temp_df])
        else:
            print(f"Error: no weather data for {series['city']}")
    return df_out