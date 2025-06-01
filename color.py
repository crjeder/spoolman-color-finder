import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import requests
import json
import argparse

# parameter defaults
url = "http://127.0.0.1" # API-base url
match_color_srgb = sRGBColor(255, 144, 0, True)
max_distance = 1200

# Create argument parser
parser = argparse.ArgumentParser(description="Finds filaments in spoolman which match the color you specified.",
                                 prog="Spoolman-color-finder")
parser.add_argument("--api-url", "-u", type=str, description="URL of the Spoolman API (whitout '/api/v1/')")  # Optional argument
parser.add_argument("--color-hex", "-c", type=str, description="the color value in hex to search for")
parser.add_argument("-d", "--distance", type=int, description="how different the colors are allowed to be. (high value means differs a lot)")
url.append("/api/v1/export/filaments")

match_color_lab = convert_color(match_color_srgb, LabColor)
list = []
params = {"fmt": "json"}
response = requests.get(url, params=params)

# Antwort prüfen und ausgeben
if response.status_code == 200:
    data = response.json()
    for row in data:
        hex_color = row["color_hex"]
        if hex_color != None:
            hex_color = hex_color.lstrip('#')  # Remove '#' if present
            rgb = sRGBColor(int(hex_color[0:2], 16),
                            int(hex_color[2:4], 16),
                            int(hex_color[4:6], 16), True)
            lab = convert_color(rgb, LabColor)
            square_distance = ((lab.lab_a - match_color_lab.lab_a)**2 +
                               (lab.lab_b - match_color_lab.lab_b)**2 +
                               (lab.lab_l - match_color_lab.lab_l)**2)

            if square_distance < max_distance:
                match = (row["id"], row["name"], square_distance)
                list.append(match)
else:
    print("Fehler:", response.status_code)
    print(response.json)

sorted_list = sorted(list, key=lambda x: x[2])
for id in sorted_list:
    print(id, name, distance)

