import requests
import csv
import json

def get_place_ids(api_key, keyword, lat, lng, radius, next_page_token=None):
    """
    This function returns a list of place IDs of the places matching the given keyword
    within the specified radius of the given latitude and longitude
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "key": api_key,
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword
    }

    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data:
        return [result["place_id"] for result in data["results"]], data.get("next_page_token", None)
    else:
        return [], None

api_key = "" #put your own API Key here
keyword = "Cafe"
lat = 42.375801
lng = -72.519867
radius = 50000  # in meters

place_ids = []
next_page_token = None
while True:
    result, next_page_token = get_place_ids(api_key, keyword, lat, lng, radius, next_page_token)
    place_ids.extend(result)
    if not next_page_token:
        break

print(place_ids)


with open('places.csv', 'w', newline='') as file:
    # Create a writer object for the CSV file
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['Place ID', 'Name', 'Phone number', 'Website'])

    for place_id in place_ids: 
        # Construct the URL for the Places API request
        url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'

        # Send the API request and get the response
        response = requests.get(url)

        # Check the status code of the response
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Extract the name, phone number, and website from the data
            name = data['result'].get('name', '')
            phone_number = data['result'].get('formatted_phone_number', '')
            website = data['result'].get('website', '')

            writer.writerow([place_id, name, phone_number, website])
        else:
            # If the status code is not 200, there was an error with the API request
            print(f'Error: API request failed with status code {response.status_code}')
