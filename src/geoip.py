import requests

def get_geoip(ip):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json")
        return resp.json().get("country", "Unknown")
    except Exception:
        return "Unknown"