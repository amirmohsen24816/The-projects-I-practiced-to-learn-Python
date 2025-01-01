import requests
from twilio.rest import Client

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
api_key = "your API key"
account_sid = "your account SID"
auth_token = 'your outh token'

weather_params = {
    "lat": "your lat",
    "lon": "your lon",
    "appid": api_key,
}

response = requests.get(url=OWN_Endpoint, params=weather_params)
weather_data = response.json()
weather_slice = weather_data["weather"][0]["id"]
print()
cold_weather = False 

if weather_slice <= 800:
    cold_weather = True

if cold_weather:
   client = Client(account_sid, auth_token)

   message = client.messages.create(
       body="The weather is cold today, don't forget to wear appropriate clothes🧥🧣🧤.",
       from_='your twilio number test',
       to='any number you have or you want to send SMS'
       )
