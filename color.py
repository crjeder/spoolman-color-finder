import math
import sys
import argparse
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import requests


# Create argument parser
parser = argparse.ArgumentParser(description="Finds filaments in spoolman which match the color you specified.",
                                 prog="Spoolman-color-finder")
parser.add_argument("color", type=str, help="the color value in hex to search for")
parser.add_argument("--url", "-u", type=str, default="http://127.0.0.1")
parser.add_argument("-d", "--distance", type=int, default = 15, 
                    help="how different the colors are allowed to be. (high value means differs a lot)")

args = parser.parse_args()
url = args.url + "/api/v1/export/filaments"
max_distance = args.distance
hex_color = args.color
hex_color = hex_color.rstrip("#")

match_color_srgb = sRGBColor(int(hex_color[0:2], 16),
                            int(hex_color[2:4], 16),
                            int(hex_color[4:6], 16), True)

match_color_lab = convert_color(match_color_srgb, LabColor)
color_list = []
params = {"fmt": "json"}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises HTTPError if the response contains an error (4xx or 5xx)
except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
    sys.exit(errh)
except requests.exceptions.ConnectionError as errc:
    print("Connection Error: could not connect to ", url)
    sys.exit(errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
    sys.exit(errt)
except requests.exceptions.RequestException as err:
    print("Something went wrong:", err)
    sys.exit(err)

# Antwort prüfen und ausgeben
if response.status_code == 200:
    data = response.json()
    for row in data:
        hex_color = row["color_hex"]
        if hex_color is not None:
            hex_color = hex_color.lstrip('#')  # Remove '#' if present
            rgb = sRGBColor(int(hex_color[0:2], 16),
                            int(hex_color[2:4], 16),
                            int(hex_color[4:6], 16), True)
            lab = convert_color(rgb, LabColor)
            distance = math.sqrt((lab.lab_a - match_color_lab.lab_a)**2 +
                               (lab.lab_b - match_color_lab.lab_b)**2 +
                               (lab.lab_l - match_color_lab.lab_l)**2)

            if distance < max_distance:
                match = (row["id"], row["name"], distance)
                color_list.append(match)
else:
    print("Fehler:", response.status_code)
    print(response.json)

if len(color_list) > 0:
    sorted_list = sorted(color_list, key=lambda x: x[2])
    for item in sorted_list:
        print(item)
else:
    print("No filaments matching your color found")

