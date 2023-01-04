import matplotlib.pyplot as plt
import numpy as np
import requests
import requests

from loguru import logger 

# Set the API endpoint and your API key
endpoint = "https://api.weather.gov/radar/latest"

params = {
    "product": "N0R",  # Base reflectivity data
    "radars": "KABR",  # Aberdeen, SD radar
}

# Add the API key to the request headers
headers = {"User-Agent": "WeatherPro - https://github.com/kerryhatcher/WeatherPro"}

# Send the request to the API
response = requests.get(endpoint, params=params, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    # The request was successful, so parse the warning data
    radar_data = response.json()
    #print(f"warning Data { warning_data}")
    logger.debug(f"warning Data received")
else:
    # The request was unsuccessful, so print an error message
    #print(f"Error {response.status_code}: {response.reason}")
    logger.error((f"Error {response.status_code}: {response.reason}"))

# Get the radar image data and metadata
image_url = radar_data["product"]["image"]["url"]
image_response = requests.get(image_url)
image_data = image_response.content

# Decode the image data
image = np.frombuffer(image_data, np.uint8)
image = image.reshape(radar_data["product"]["image"]["size"]["height"], radar_data["product"]["image"]["size"]["width"])

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(image, cmap="Greys_r")

# Set the map title and axis labels
ax.set_title("NWS Radar Image")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Show the plot
plt.show()