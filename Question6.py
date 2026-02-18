import threading
from typing import Dict

try:
    import requests
except Exception:
    requests = None


def fetch_weather(city: str, results: Dict[str, Dict], lock: threading.Lock, api_key: str = None):
    """Fetch weather for city and store into results under lock.

    If requests is unavailable or api_key is None, return mock data to avoid network dependency.
    """
    if requests is None or api_key is None:
        # Return mock data for offline/demo mode
        mock = {"temp": 20.0 + hash(city) % 10, "humidity": 50, "pressure": 1013}
        with lock:
            results[city] = mock
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    with lock:
        results[city] = {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"]
        }


if __name__ == "__main__":
    # Demo threaded fetch using mock mode (no API key)
    cities = ["London", "Paris", "Tokyo"]
    results = {}
    lock = threading.Lock()
    threads = []
    for c in cities:
        t = threading.Thread(target=fetch_weather, args=(c, results, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(results)