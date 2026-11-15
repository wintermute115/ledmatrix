#!/usr/bin/python3

import controller
import argparse

parser = argparse.ArgumentParser(prog='LEDMatrix', description='Lights rows of LEDs to indicate how many podcasts are waiting to be copied over')
parser.add_argument('-t', '--test', action='store_true', help='Show output in the terminal, instead of sending to the LED board')
parser.add_argument('-r', '--rows', type=int, help='How many rows to light. This overrides the actual number of podcasts');
args = parser.parse_args()

if (args.rows is None):
    with open("/home/ross/Downloads/New_Podcasts/Playlists/Podcasts.m3u8") as file:
        lines = sum(1 for _ in file)
else:
    lines = args.rows

if (args.test):
    if (lines == 1) :
        noun = "podcast"
    else :
        noun = "podcasts"
    print(str(lines) + " " + noun);

grid = []

# Step through each column
for i in range(0, 9, 1):
    data = []
    # Reduce the level of brightness as you move from the center
    lit = (min([i, 8 - i]) + 1) * 51

    # Make sure it fits in the appropriate range
    lit = min([255, max([0, lit])])

    # Set the number of lit rows to the number of items in the file
    for j in range(0, 34, 1):
        if (j < lines):
            data.append(lit)
        else:
            data.append(0)

    grid.append(data)

if (args.test):
    controller.test(grid)
else:
    controller.output(grid)
