def build_gui():
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
        # Insert mock data into the table for demo purposes
        for row in table.get_children():
            table.delete(row)
        sample = [
            ("London", "21.5", "55", "1012"),
            ("Paris", "20.0", "50", "1013"),
            ("Tokyo", "23.0", "60", "1010"),
        ]
        for r in sample:
            table.insert("", "end", values=r)

    tk.Button(root, text="Fetch Weather", command=on_fetch).pack()
    return root


def _cli_demo():
    # Headless fallback: print a small table to stdout
    print("City | Temp (°C) | Humidity (%) | Pressure (hPa)")
    print("London | 21.5 | 55 | 1012")
    print("Paris  | 20.0 | 50 | 1013")
    print("Tokyo  | 23.0 | 60 | 1010")


if __name__ == "__main__":
    try:
        app = build_gui()
        app.mainloop()
    except Exception as e:
        print("GUI unavailable or failed to start; running CLI demo.")
        print("Error:", e)
        _cli_demo()