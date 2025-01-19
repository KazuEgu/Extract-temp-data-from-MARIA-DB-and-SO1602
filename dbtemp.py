import time

import board
import busio

import adafruit_so1602

import requests
from datetime import datetime

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
SO1602 = adafruit_so1602.Adafruit_SO1602_I2C(i2c)

def fetch_data():
    # Data Import / IPは自身の環境に合わせて変更
    url = "http://192.168.X.Y/sensvalues.php" 
    try:
        response = requests.get(url, timeout=5)  # Setting Timeout
        response.raise_for_status()  # HTTP Error Check
        json_data = response.json()

        # Get Latest Data
        latest_entry = None
        if json_data:
            latest_entry = json_data[0]  # Get the last element from the list

        if latest_entry:
            # Extract datetime and temperature
            datetime_str = latest_entry.get("datetime", "Unknown datetime")
            latest_temp = latest_entry.get("temp", "Unknown temperature")

            # Format datetime to show only time
            if datetime_str != "Unknown datetime":
                try:
                    # Parse datetime string to a datetime object
                    dt_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                    time_str = dt_object.strftime("%H:%M:%S")  # Extract time as HH:MM:SS
                except ValueError:
                    time_str = "Invalid datetime format"
            else:
                time_str = datetime_str

            # Print Latest Data
            print("Latest Data:")
            print(f"Time: {time_str}")
            print(f"Temperature: {latest_temp}deg C")
            # Print SO1602
            SO1602.displayClear()
            SO1602.writeLine(f"Time: {time_str}",line=0,align="left")
            SO1602.writeLine(f"Temp: {latest_temp}deg C",line=1,align="left") 
        else:
            print("No data available.")
            SO1602.writeLine(str="No data available",line=0,align="left")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error for URL {url}: {e}")
    except (KeyError, TypeError, ValueError) as e:
        print(f"JSON Data Error: {e}")

# Run
if __name__ == "__main__":
    fetch_data()
