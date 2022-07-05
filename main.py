import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("C:\Python\env data.env")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
API_KEY = os.getenv("API_KEY")
MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

# Setting up and requesting from the API.
response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

# Looping through 12 hours from weather_slice
will_rain = False
for hour_data in weather_slice:
    if hour_data["weather"][0]["id"] < 700:
        will_rain = True

# If it is going to rain in the next 12 hours, you will receive an email to bring an umbrella.

if will_rain:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:Don't forget to bring an umbrella!\n\nDont get wet, stay dry!")
    print("Bring an umbrella!")


