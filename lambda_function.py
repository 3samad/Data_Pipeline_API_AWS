# import json
# import pandas as pd
# import os
# import sqlalchemy
# import weather_functions

# def lambda_handler(event, context):
    
#     con = os.environ["con"]
#     cities = pd.read_sql("cities", con=con, index_col = "id")
#     weather = weather_functions.get_weather(cities)
#     weather.to_sql("weather", if_exists="append", con=con, index=False)
    
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

import json
import pandas as pd
import os
import sqlalchemy

def lambda_handler(event, context):
  import weathers_function
  con = os.environ["con"]
  cities = pd.read_sql("cities", con=con, index_col = "city_id")
  weathers = weathers_function.get_weather(cities.iloc[0:1])
  
  weathers = weathers.rename(columns={"country": "country_id"})
  weathers["city_id"] = ""
  weathers.loc[weathers["city"]=="Leipzig", "city_id"] = 1
  weathers.loc[weathers["city"]=="Dresden", "city_id"] = 2
  weathers.loc[weathers["city"]=="Frankfurt am Main", "city_id"] = 3
  weathers = weathers.drop('city', axis=1) 
  weathers['forecast_time'] = pd.to_datetime(weathers['forecast_time'])
  weathers['info_retrieved_at'] = pd.to_datetime(weathers['info_retrieved_at'], dayfirst=True)
  weathers.to_sql("weathers", if_exists='append', con=con, index=False)
  
  
  return {
      'statusCode': 200,
      'body': json.dumps('Hello from Lambda!')
  }
  