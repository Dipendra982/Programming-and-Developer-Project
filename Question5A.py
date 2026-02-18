import time
from typing import List
from Question6 import fetch_weather
import threading


def fetch_sequential(cities: List[str]) -> float:
    start = time.time()
    results = {}
    lock = threading.Lock()
    for city in cities:
        fetch_weather(city, results, lock)
    return time.time() - start


if __name__ == "__main__":
    print(fetch_sequential(["London", "Paris"]))