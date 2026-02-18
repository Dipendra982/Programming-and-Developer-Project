import matplotlib.pyplot as plt

def plot_path(itinerary):
    x = [s["lon"] for s in itinerary]
    y = [s["lat"] for s in itinerary]

    plt.plot(x, y, marker='o')
    for s in itinerary:
        plt.text(s["lon"], s["lat"], s["name"], fontsize=8)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Tourist Itinerary Path")
    # Save the figure so the result is available in headless environments
    safe_name = "itinerary_path.png"
    plt.savefig(safe_name, bbox_inches='tight')
    print(f"Saved itinerary plot to: {safe_name}")
    try:
        plt.show()
    except Exception:
        # In headless environments plt.show() may fail or block; saved file is available
        pass


if __name__ == "__main__":
    # Sample itinerary for demo/run
    itinerary = [
        {"name": "Start", "lon": 0.0, "lat": 0.0},
        {"name": "Point A", "lon": 1.0, "lat": 0.5},
        {"name": "Point B", "lon": 2.0, "lat": 0.0},
        {"name": "End", "lon": 3.0, "lat": 1.0},
    ]
    plot_path(itinerary)