from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

LAT = [49.299, 50.0413, 49.785, 50.0614, 50.2597, 50.7231, 50.8703,
       50.7965, 51.2506, 51.4025, 52.2298, 51.7706, 51.9355, 52.4069,
       52.5468, 52.7337, 53.1333, 53.3833, 53.7838, 53.8432, 54.1118,
       53.9105, 54.1756, 54.1944, 54.3523, 54.5189, 54.7909]

LON = [19.9489, 21.999, 22.7673, 19.9366, 19.0217, 23.252, 20.6275,
       19.1241, 22.5701, 21.1471, 21.0118, 19.4739, 15.5064, 16.9299,
       19.7064, 15.225, 23.1643, 14.6333, 20.4927, 22.9798, 22.9309,
       14.2471, 15.5834, 16.1722, 18.6491, 18.5319, 18.4009]

NAMES = ["Zakopane","Przemyśl","Bielsko-Biała","Kraków","Katowice",
         "Zamość","Kielce","Częstochowa","Lublin","Wrocław",
         "Radom","Łódź","Zielona Góra","Warszawa","Poznań",
         "Płock","Gorzów Wlkp.","Białystok","Szczecin","Olsztyn",
         "Augustów","Suwałki","Świnoujście","Kołobrzeg","Koszalin",
         "Gdańsk","Gdynia"]


def get_city(i):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LAT[i],
        "longitude": LON[i],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "is_day",
            "wind_speed_10m",
            "visibility"
        ],
        "hourly": [
            "wind_speed_10m",
            "precipitation_probability",
            "precipitation",
            "snow_depth",
            "uv_index",
            "uv_index_clear_sky",
            "sunshine_duration",
            "cloud_cover"
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset"
        ],
        "timezone": "Europe/Warsaw"
    }

    try:
        r = requests.get(url, params=params, timeout=5).json()

        return {
            "name": NAMES[i],
            "current": r.get("current", {}),
            "hourly": r.get("hourly", {}),
            "daily": r.get("daily", {})
        }

    except:
        return {"name": NAMES[i], "error": True}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data")
def data():
    return jsonify({
        "cities": [get_city(i) for i in range(len(NAMES))]
    })


@app.route("/eas/test", methods=["POST"])
def eas():
    print("🔥 EAS TRIGGER")
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
