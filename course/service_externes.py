import requests
from django.conf import settings


def get_place_details(place_id):
    """
    Retrieves the latitude and longitude of a place using the Google Places API.

    :param place_id: The unique identifier for the place to retrieve details for.
    :return: A tuple containing latitude and longitude if the request is successful, otherwise (None, None).
    """
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}"
        f"&key={settings.GOOGLE_API_KEY}"
    )
    resp = requests.get(url).json()
    if resp["status"] == "OK":
        loc = resp["result"]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None


def get_distance_and_duration(lat1, lng1, lat2, lng2):
    """

    """
    origin = f"{lat1},{lng1}"
    destination = f"{lat2},{lng2}"
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin}"
        f"&destinations={destination}"
        f"&key={settings.GOOGLE_API_KEY}"
        "&mode=driving"
    )
    resp = requests.get(url).json()
    if resp["status"] == "OK":
        elem = resp["rows"][0]["elements"][0]
        if elem["status"] == "OK":
            dist_m = elem["distance"]["value"]
            dur_s = elem["duration"]["value"]
            dist_km = round(dist_m / 1000, 2)
            dur_min = round(dur_s / 60, 1)
            return dist_km, dur_min
    return None, None


def get_weather(lat, lon):
    """

    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={settings.OPENWEATHER_API_KEY}"
        f"&units=metric"
        f"&lang=en"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return temp, interpret_weather(description)
    return None, None


def interpret_weather(description):
    """

    """
    if description:
        desc = description.lower()
        if "rain" in desc:
            return "rain"
        elif "snow" in desc:
            return "snow"
    return "clear"


def encoding_weather(description):
    """

    """
    if description == "rain":
        return 1, 0
    elif description == "snow":
        return 0, 1
    return 0, 0


def get_traffic_conditions(lat1, lng1, lat2, lng2):
    """

    """
    origin = f"{lat1},{lng1}"
    destination = f"{lat2},{lng2}"
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin}"
        f"&destinations={destination}"
        f"&key={settings.GOOGLE_API_KEY}"
        "&mode=driving"
        "&departure_time=now"
        "&traffic_model=best_guess"
    )
    resp = requests.get(url).json()
    print(resp)
    if resp["status"] == "OK":
        elem = resp["rows"][0]["elements"][0]
        if elem["status"] == "OK":
            return interpret_traffic_level(elem)
    return "Unknown"


def interpret_traffic_level(elem):
    """

    """
    dur = elem["duration"]["value"]
    dur_traffic = elem.get("duration_in_traffic", {}).get("value", dur)
    ratio = dur_traffic / dur

    if ratio < 1.10:
        return "Low"
    elif ratio < 1.30:
        return "Medium"
    return "High"


def encodage_traffic_conditions(level):
    """

    """
    if level == "Low":
        return 1, 0
    elif level == "Medium":
        return 0, 1
    return 0, 0
