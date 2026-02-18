import threading
from typing import Dict, Any, Optional

lock = threading.Lock()
results: Dict[str, Dict[str, Any]] = {}


def update_table(table: Optional[Any] = None) -> None:
    """Update the provided table (ttk.Treeview) with the current `results`.

    If `table` is None, print the results to stdout (useful in headless/demo mode).
    """
    with lock:
        if table is None:
            # No GUI available — print results for debugging
            for city, data in results.items():
                print(city, data)
            return

        # Clear existing rows
        for row in table.get_children():
            table.delete(row)

        for city, data in results.items():
            table.insert("", "end", values=(city, data.get("temp"), data.get("humidity"), data.get("pressure")))


if __name__ == "__main__":
    # Demo: populate results with mock data and call update_table in CLI mode
    results["London"] = {"temp": 21.5, "humidity": 55, "pressure": 1012}
    results["Paris"] = {"temp": 20.0, "humidity": 50, "pressure": 1013}
    update_table(None)