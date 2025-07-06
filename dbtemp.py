import time
import board
import busio
import adafruit_so1602
import requests
from datetime import datetime

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
SO1602 = adafruit_so1602.Adafruit_SO1602_I2C(i2c)

def fetch_with_retry(url, retries=3, timeout=5, delay=2):
    """HTTP GET with retry mechanism."""
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt+1} to fetch data...")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    print("All fetch attempts failed.")
    return None

def fetch_data():
    url = "http://192.168.0.6/sensvalues.php"
    response = fetch_with_retry(url)

    if response is None:
        SO1602.displayClear()
        SO1602.writeLine(str="HTTP Error", line=0, align="left")
        return

    try:
        json_data = response.json()

        if not json_data or not isinstance(json_data, list):
            print("Invalid or empty JSON data.")
            SO1602.displayClear()
            SO1602.writeLine(str="No data", line=0, align="left")
            return

        latest_entry = json_data[0]

        datetime_str = latest_entry.get("datetime", "Unknown datetime")
        latest_temp = latest_entry.get("temp", "Unknown temperature")

        if datetime_str != "Unknown datetime":
            try:
                dt_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                time_str = dt_object.strftime("%H:%M:%S")
            except ValueError:
                time_str = "Invalid time"
        else:
            time_str = datetime_str

        print("Latest Data:")
        print(f"Time: {time_str}")
        print(f"Temperature: {latest_temp}deg C")

        SO1602.displayClear()
        SO1602.writeLine(f"Time: {time_str}", line=0, align="left")
        SO1602.writeLine(f"Temp: {latest_temp}deg C", line=1, align="left")

    except (KeyError, TypeError, ValueError) as e:
        print(f"JSON parsing error: {e}")
        SO1602.displayClear()
        SO1602.writeLine(str="JSON Error", line=0, align="left")

# Run
if __name__ == "__main__":
    fetch_data()
