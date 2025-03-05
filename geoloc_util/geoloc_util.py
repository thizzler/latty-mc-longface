import argparse
import requests
import time

COUNTRY_CODE = "US"
API_KEY = "f897a99d971b5eef57be6fafa0d83239"
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
}


def main():
    parser = argparse.ArgumentParser(
        description="Fetch lat/long ddata for US city/state or zip codes"
    )
    parser.add_argument(
        "--locations",
        required=True,
        nargs="*",
        help="One or more locations in the form of 'City, State' or ZipCode' (no flag needed)."
    )

    args = parser.parse_args()
    location_list = args.locations

    results = parse_locations(location_list)
    print_output(results)

def parse_locations(location_list):
    output_data = {}

    for location in location_list:
        # quick check - if it has digits, we assume it's a zip
        if any(char.isdigit() for char in location):
            parse_zip_location(location, output_data)
        else:
            # attempt City, State parse
            if "," in location:
                parts = [x.strip() for x in location.split(",")]
                if len(parts) == 2:
                    city_capitalized = parts[0].title()
                    state_capitalized = parts[1].upper()
                    if state_capitalized not in US_STATES:
                        output_data[location] = {"Error": "Invalid State abbreviation."}
                    else:
                        parse_city_state_location(city_capitalized, state_capitalized, output_data)
                else:
                    output_data[location] = {"Error": "Invalid City/State format. Expect 'City, State'."}
            else:
                output_data[location] = {"Error": "Invalid City/State format. No comma found."}

    return output_data

def parse_zip_location(zip_code, output):
    # check if zip contains 5 characters
    if len(zip_code) != 5:
        output[zip_code] = {"Error": "Invalid zip format (must be 5 digits)."}
        return
    output[zip_code] = (get_zip_data(zip_code))

def parse_city_state_location(city, state, output):
    output[f"{city}, {state}"] = (get_city_state_data(city, state))

def get_zip_data(zip_code):
    return api_request_location(zip_code=zip_code, city=None, state=None)

def get_city_state_data(city, state):
    return api_request_location(zip_code=None, city=city, state=state)

def api_request_location(zip_code, city, state):
    max_tries = 3
    attempts = 0

    if zip_code:
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{COUNTRY_CODE}&appid={API_KEY}"
        location = zip_code
    else:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{COUNTRY_CODE}&appid={API_KEY}"
        location = f"{city}, {state}"

    while attempts < max_tries:
        try:
            response = requests.get(url, timeout=5)
            # if the response is an HTTP error, raise_for_status() will throw
            response.raise_for_status()
            
            response_data = response.json()
            
            if isinstance(response_data, list) and response_data:
                return response_data[0]
            else:
                return response_data
            
        except requests.exceptions.RequestException as err:
            # this could be timeout, connection error, HTTP error, etc.
            attempts += 1
            if attempts < max_tries:
                # wait a bit before retrying
                time.sleep(2)
            else:
                # If it's the last attempt, return an error
                return {f"{location}": f"HTTP request failed after {max_tries} attempts: {err}"}

def print_output(results):
    for input_location, data in results.items():
        # If there's an error key, just show the error
        if "Error" in data:
            print(f"{input_location} -> ERROR: {data['Error']}")
        else:
            # otherwise, assume it's a successful response from the api
            lat = data.get("lat", "N/A")
            lon = data.get("lon", "N/A")
            place_name = data.get("name", "Unknown place")
            state = data.get("state", "Unknown state")
            print(f"{input_location} -> Lat: {lat}, Lon: {lon}, Name: {place_name}, State: {state}")

if __name__ == "__main__":
    main()