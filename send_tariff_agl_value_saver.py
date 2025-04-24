"""
Shelly AGL Tariff Sync Script
-----------------------------

This script calculates the current electricity tariff based on AGL’s time-of-use rates
(peak, shoulder, and off-peak) and pushes the appropriate rate to your Shelly device
using its HTTP API. This enables real-time cost tracking and accurate reporting within
the Shelly Cloud app, particularly when using PV Setup (Alpha) for energy analysis.

Setup:
- Requires a `.env` file with SHELLY_API_URL pointing to the correct webhook from your Shelly app.
- Intended to be run periodically (e.g. via cron) to keep the tariff updated throughout the day.

Author: James Flores
GitHub: https://github.com/jamesflores/Shelly-Scripts

"""
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Use .env file with SHELLY_API_URL with your tokenized URL from the Shelly app
load_dotenv()  # Loads from .env in the current directory
SHELLY_API_URL = os.getenv("SHELLY_API_URL")
if not SHELLY_API_URL:
    print("SHELLY_API_URL is not set in your .env file.")
    exit(1)

# Tariff values (AUD/kWh)
TARIFFS = {
    "peak": 0.3826,
    "shoulder": 0.3718,
    "off_peak": 0.2437
}

def get_tariff():
    now = datetime.now()  # pytz.timezone("Australia/Sydney"))
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    hour = now.hour

    if weekday < 5:  # Mon–Fri
        if (7 <= hour < 9) or (17 <= hour < 20):
            return TARIFFS["peak"]
        elif (9 <= hour < 17) or (20 <= hour < 22):
            return TARIFFS["shoulder"]
    return TARIFFS["off_peak"]

def send_tariff():
    current_price = get_tariff()
    payload = { "price": round(current_price, 4) }
    response = requests.post(SHELLY_API_URL, json=payload)
    print(f"[{datetime.now()}] Sent price: {payload['price']} | Status: {response.status_code}")

if __name__ == "__main__":
    send_tariff()
