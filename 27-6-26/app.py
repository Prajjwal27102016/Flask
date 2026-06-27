from flask import Flask, render_template, request
import json
import urllib.parse
import urllib.request


app = Flask(__name__)


# Free geocoding API from Photon (Komoot)
PHOTON_API_URL = "https://photon.komoot.io/api/"


@app.route("/", methods=["GET", "POST"])
def index():
   """Handle both displaying the form and processing location search."""
   if request.method == "GET":
      
       return render_template("index.html")


   # Handle POST request (form submission)
   location = request.form.get("location", "").strip()
   if not location:
       return render_template("index.html", error="Please enter a location.")


   try:
       # URL-encode the location string
       encoded_location = urllib.parse.quote(location)
       url = f"{PHOTON_API_URL}?q={encoded_location}&limit=1"


       # Photon expects a User-Agent header
       req = urllib.request.Request(url, headers={"User-Agent": "FlaskGeocoder/1.0"})
       with urllib.request.urlopen(req) as response:
           data = json.loads(response.read().decode())


       features = data.get("features", [])
       if not features:
           return render_template(
               "index.html",
               error=f"Could not find coordinates for '{location}'. Please try another name."
           )


       # Photon returns coordinates as [longitude, latitude]
       lon, lat = features[0]["geometry"]["coordinates"]


       result = {
           "latitude": lat,
           "longitude": lon,
           "name": features[0]["properties"].get("name", location),
       }


       return render_template("index.html", data=result)


   except urllib.error.URLError:
       return render_template(
           "index.html",
           error="Network error. Please check your internet connection and try again."
       )
   except json.JSONDecodeError:
       return render_template(
           "index.html",
           error="Invalid response from geocoding service. Please try again later."
       )
   except Exception:
       return render_template(
           "index.html",
           error="An unexpected error occurred. Please try again."
       )


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080, debug=True)
