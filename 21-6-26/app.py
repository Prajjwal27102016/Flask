from flask import Flask, render_template, request
import requests


app = Flask(__name__)


# ✅ WeatherAPI.com key
API_KEY = "db94ca4b23b54a0689c110013262106"


@app.route("/")
def home():
   return render_template("index.html")


@app.route("/get_weather", methods=["POST"])
def get_weather():
   city = request.form.get("city")


   if not city or not validate_city_name(city):
       return render_template("index.html", error="Please enter a valid city name!")


   # ✅ WeatherAPI Request URL
   base_url = "http://api.weatherapi.com/v1/current.json"
   params = {
       "key": API_KEY,
       "q": city,
       "aqi": "no"
   }


   response = requests.get(base_url, params=params)


   if response.status_code == 200:
       data = response.json()
       weather = {
           "city": data["location"]["name"],
           "description": data["current"]["condition"]["text"],
           "temperature": data["current"]["temp_c"],
           "humidity": data["current"]["humidity"],
           "wind_speed": data["current"]["wind_kph"],
           "icon": "http:" + data["current"]["condition"]["icon"]
       }
       return render_template("index.html", weather=weather)
   else:
       return render_template("index.html", error="City not found or API Error.")


def validate_city_name(city):
   """Only alphabets and spaces allowed."""
   return all(part.isalpha() for part in city.split()) and len(city) > 1


if __name__ == "__main__":
   app.run(debug=True)
