
# spoolman-color-finder

This is just a little tool for the [spoolman](https://github.com/Donkie/Spoolman) API. It finds filaments with a color close enough to the one you specified.
It uses Delta E CIEDE2000 to calculate the color distance.

## usage

```
Spoolman-color-finder [-h] [--url URL] [-d DISTANCE] color


positional arguments:
  color                 the color value in hex to search for

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     base URL of the spoolman API 
  -d DISTANCE, --distance DISTANCE
                        how different the colors are allowed to be. (high value means differs a lot)

```
