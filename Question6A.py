import threading
import sys

# Try to import fetch_weather from package or local module; fall back to a mock implementation
try:
    # preferred when package is used or running as script in repo root
    from Question6 import fetch_weather
except Exception:
    try:
        # relative import when module is inside a package
        from .Question6 import fetch_weather  # type: ignore
    except Exception:
        # fallback mock (no network)
        def fetch_weather(city, results, lock, api_key=None):
            with lock:
                results[city] = {"temp": 20.0 + hash(city) % 10, "humidity": 50, "pressure": 1013}


def build_gui(fetch_callback=None):
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Multi-threaded Weather Data Collector")

    columns = ("City", "Temp (°C)", "Humidity (%)", "Pressure (hPa)")
    table = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)

    table.pack()

    def on_fetch():
        cities = ["London", "Paris", "Tokyo"]
        results = {}
        lock = threading.Lock()
        threads = []
        for c in cities:
            t = threading.Thread(target=fetch_callback or fetch_weather, args=(c, results, lock))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        for row in table.get_children():
            table.delete(row)
        for city, data in results.items():
            table.insert("", "end", values=(city, data["temp"], data["humidity"], data["pressure"]))

    tk.Button(root, text="Fetch Weather", command=on_fetch).pack()
    return root


def _cli_demo(fetch_callback=None):
    # Run a headless demo that prints results
    cities = ["London", "Paris", "Tokyo"]
    results = {}
    lock = threading.Lock()
    threads = []
    for c in cities:
        t = threading.Thread(target=fetch_callback or fetch_weather, args=(c, results, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    for city, data in results.items():
        print(f"{city}: temp={data['temp']}, humidity={data['humidity']}, pressure={data['pressure']}")


if __name__ == "__main__":
    # Try to start GUI; if tkinter is unavailable or fails (headless), run CLI demo instead
    try:
        app = build_gui()
        app.mainloop()
    except Exception:
        _cli_demo()