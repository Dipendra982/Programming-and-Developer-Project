import time
import threading
from typing import List, Dict, Tuple

try:
    from Question6 import fetch_weather
except Exception:
    try:
        from .Question6 import fetch_weather  # type: ignore
    except Exception:
        # fallback mock
        def fetch_weather(city, results, lock):
            with lock:
                results[city] = {"temp": 20.0 + hash(city) % 10, "humidity": 50, "pressure": 1013}


def fetch_parallel(cities: List[str]) -> Tuple[float, Dict[str, Dict]]:
    """Fetch weather for cities in parallel threads.

    Returns (elapsed_seconds, results_dict).
    """
    start = time.time()
    threads = []
    results: Dict[str, Dict] = {}
    lock = threading.Lock()

    for city in cities:
        t = threading.Thread(target=fetch_weather, args=(city, results, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return time.time() - start, results


if __name__ == "__main__":
    elapsed, results = fetch_parallel(["London", "Paris", "Tokyo"])
    print(f"Elapsed (parallel): {elapsed:.6f}s")
    for city, data in results.items():
        print(f"{city}: temp={data['temp']}, humidity={data['humidity']}, pressure={data['pressure']}")