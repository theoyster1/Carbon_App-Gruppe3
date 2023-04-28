from statistics import mean
from flask import render_template, Blueprint
import json
import requests

purpose = Blueprint("purpose", __name__)


@purpose.route("/purpose")
def purpose_home():
    # World mean temperature
    url = "https://global-temperature.p.rapidapi.com/api/temperature-api"

    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "3bede588c1mshf7e2c981e749cb5p1a3963jsncbac8fd70f21",
        "X-RapidAPI-Host": "global-temperature.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract the data for each year
    years = []
    temperatures = []
    for d in data["result"]:
        if d["time"] > "1920":
            year = int(float(d["time"]))
            temperature = mean([float(d["station"]), float(d["land"])])
            years.append(year)
            temperatures.append(temperature)

    return render_template(
        "purpose.html",
        title="Purpose",
        average_temperature=json.dumps(temperatures),
        yearLabels=json.dumps(years),
    )
