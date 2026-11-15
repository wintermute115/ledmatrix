#!/usr/bin/python3

import controller
import argparse

parser = argparse.ArgumentParser(prog='LEDMatrix', description='Draw a stripe down the center of the LED board')
parser.add_argument('-t', '--test', action='store_true', help='Show output in the terminal, instead of sending to the LED board')
args = parser.parse_args()

grid = controller.empty_grid()

for i in range(3, 6):
    data = [];
    for j in range(34):
        if (i == 4):
            data.append(255)
        else:
            data.append(51)
    grid[i] = data


if (args.test):
    controller.test(grid)
else:
    controller.output(grid)