import requests
from django.utils import timezone
from ..api.models import Country, NameNationality

NATIONALIZE_URL = "https://api.nationalize.io"
RESTCOUNTRIES_URL = "https://restcountries.com/v3.1/alpha"


def fetch_nationality(name):
    try:
        response = requests.get(f"https://api.nationalize.io/?name={name}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching nationality: {str(e)}")
        return None


def fetch_country_details(country_code):
    try:
        response = requests.get(f"{RESTCOUNTRIES_URL}/{country_code.lower()}")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            data = data[0]

        return {
            "country_code": country_code.upper(),
            "name": data.get("name", {}).get("common", ""),
            "full_name": data.get("name", {}).get("official", ""),
            "region": data.get("region", ""),
            "subregion": data.get("subregion", ""),
            "is_independent": data.get("independent", True),
            "capital": data.get("capital", [""])[0] if data.get("capital") else None,
            "capital_latitude": (
                data.get("latlng", [None, None])[0] if data.get("latlng") else None
            ),
            "capital_longitude": (
                data.get("latlng", [None, None])[1] if data.get("latlng") else None
            ),
            "flag_png": data.get("flags", {}).get("png", ""),
            "flag_svg": data.get("flags", {}).get("svg", ""),
            "flag_alt": data.get("flags", {}).get("alt", ""),
            "coat_of_arms_png": data.get("coatOfArms", {}).get("png", ""),
            "coat_of_arms_svg": data.get("coatOfArms", {}).get("svg", ""),
            "borders": data.get("borders", []),
        }

    except (requests.RequestException, IndexError, KeyError) as e:
        return None
