#!/usr/bin/env python3
"""
GUI for Multi-threaded Weather Data Collection
Uses mock data to simulate weather API calls
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import random
from datetime import datetime
from queue import Queue


class WeatherDataCollector:
    """Mock weather data generator"""
    
    CITIES = [
        "New York", "London", "Tokyo", "Sydney", "Paris",
        "Berlin", "Mumbai", "Beijing", "Dubai", "Singapore"
    ]
    
    CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Windy"]
    
    def __init__(self):
        self.city = ""
        self.temperature = 0
        self.humidity = 0
        self.condition = ""
        self.wind_speed = 0
        self.timestamp = ""
    
    def generate_mock_data(self, city):
        """Generate mock weather data for a city"""
        self.city = city
        self.temperature = random.randint(-10, 40)
        self.humidity = random.randint(20, 100)
        self.condition = random.choice(self.CONDITIONS)
        self.wind_speed = random.randint(0, 50)
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        return self
    
    def to_string(self):
        return (f"{self.city}: {self.temperature}°C, "
                f"{self.condition}, Humidity: {self.humidity}%, "
                f"Wind: {self.wind_speed} km/h [{self.timestamp}]")


class WeatherGUI:
    """Main GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-threaded Weather Data Collector")
        self.root.geometry("700x500")
        
        self.collecting = False
        self.threads = []
        self.data_queue = Queue()
        self.city_vars = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="Weather Data Collection System",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # City selection frame
        select_frame = tk.LabelFrame(self.root, text="Select Cities", padx=10, pady=10)
        select_frame.pack(fill="x", padx=10, pady=5)
        
        # Create checkboxes for each city
        for city in WeatherDataCollector.CITIES:
            var = tk.BooleanVar(value=True)
            self.city_vars[city] = var
            cb = tk.Checkbutton(select_frame, text=city, variable=var)
            cb.pack(side="left", padx=5)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = tk.Button(
            control_frame, 
            text="Start Collection", 
            bg="green", 
            fg="white",
            command=self.start_collection,
            width=15
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(
            control_frame, 
            text="Stop Collection", 
            bg="red", 
            fg="white",
            command=self.stop_collection,
            width=15,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # Thread count control
        thread_frame = tk.Frame(self.root)
        thread_frame.pack(pady=5)
        
        tk.Label(thread_frame, text="Threads:").pack(side="left")
        self.thread_count = tk.Spinbox(thread_frame, from_=1, to=10, width=5)
        self.thread_count.set(3)
        self.thread_count.pack(side="left", padx=5)
        
        # Status display
        status_frame = tk.LabelFrame(self.root, text="Weather Data", padx=10, pady=10)
        status_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.data_text = scrolledtext.ScrolledText(
            status_frame, 
            width=80, 
            height=15,
            font=("Courier", 10)
        )
        self.data_text.pack(fill="both", expand=True)
        
        # Info label
        self.info_label = tk.Label(
            self.root, 
            text="Ready to collect weather data",
            fg="blue"
        )
        self.info_label.pack(pady=5)
        
        # Start the queue processor
        self.process_queue()
    
    def get_selected_cities(self):
        """Get list of selected cities"""
        return [city for city, var in self.city_vars.items() if var.get()]
    
    def collect_weather(self, city, delay=0):
        """Worker function to collect weather data for a city"""
        time.sleep(delay)  # Stagger the requests
        
        while self.collecting:
            collector = WeatherDataCollector()
            data = collector.generate_mock_data(city)
            self.data_queue.put(data.to_string())
            time.sleep(random.uniform(1, 3))  # Random delay between collections
    
    def start_collection(self):
        """Start the weather data collection"""
        cities = self.get_selected_cities()
        
        if not cities:
            self.info_label.config(text="Please select at least one city!", fg="red")
            return
        
        self.collecting = True
        self.data_text.delete(1.0, tk.END)
        
        num_threads = int(self.thread_count.get())
        
        # Create threads for each city
        for i, city in enumerate(cities):
            delay = i % num_threads * 0.5  # Stagger thread starts
            thread = threading.Thread(
                target=self.collect_weather, 
                args=(city, delay),
                daemon=True
            )
            self.threads.append(thread)
            thread.start()
        
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.info_label.config(text=f"Collecting data from {len(cities)} cities with {num_threads} threads...", fg="green")
    
    def stop_collection(self):
        """Stop the weather data collection"""
        self.collecting = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=1)
        
        self.threads = []
        
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.info_label.config(text="Collection stopped", fg="red")
    
    def process_queue(self):
        """Process data from the queue and display it"""
        try:
            while True:
                data = self.data_queue.get_nowait()
                self.data_text.insert(tk.END, f"{data}\n")
                self.data_text.see(tk.END)  # Auto-scroll to bottom
        except:
            pass
        
        # Schedule next queue check
        self.root.after(100, self.process_queue)
    
    def on_closing(self):
        """Handle window closing"""
        if self.collecting:
            self.stop_collection()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = WeatherGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
