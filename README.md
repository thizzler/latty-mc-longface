# latty-mc-longface
*A delightfully unnecessary but totally necessary app to fetch your latitude, longitude, and other tidbits!*

![Gob](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGdvc3BsODc1ZjBtcWszMDBzdjM1cHM4cHhhbzE2amU1YW9mdjBsNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/F38LjRkZmQwww/giphy.gif)

## ✨ Overview
**latty-mc-longface** is a lightweight CLI tool that uses the [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api) to fetch geolocation details (like **lat & long**) for US city/state or ZIP inputs.

## ⚡ Quick Start
1. **Clone** the repo:
   ```bash
   git clone https://github.com/YourUser/latty-mc-longface.git
   cd latty-mc-longface
2. **Set up** a virtual environment (recommended):
   ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
3. **Install** dependencies:
    ```bash
    pip install -r requirements.txt

## 🚀 Usage
From the repo root, run:
```bash
python -m geoloc_util.geoloc_util --locations "Seattle, WA" "98101" "Nopeville, XX"
```
- Multiple inputs are supported: city/state combos ("City, ST") and/or ZIP codes.
- If there’s an error (invalid format, invalid state, etc.), the tool will alert you instead of returning lat/long.

**Example response**
```bash
python -m geoloc_util.geoloc_util --locations "New York, NY" 10001
New York, NY -> Lat: 40.7306, Lon: -73.9352, Name: Manhattan, State: NY
10001 -> Lat: 40.7128, Lon: -74.0060, Name: New York, State: NY
```

## 🧪 Testing
I've written integration tests for the utility. 

To run them with pytest:
```bash
pytest tests/
```
You’ll see output confirming each scenario (valid city/state, valid ZIP, invalid inputs, etc.).

## 🗺️ License / Disclaimer
- This is a fun side project using the OpenWeather Geocoding API.
- It’s meant for demonstration and is neither bulletproof nor intended for production.