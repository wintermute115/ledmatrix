#!/usr/bin/python3

from termcolor import cprint
import argparse
import numpy
import serial


def send_command(command_id, parameters, with_response=False):
  with serial.Serial("/dev/ttyACM0", 115200) as s:
      s.write([0x32, 0xAC, command_id] + parameters)

      if with_response:
          res = s.read(32)
          return res

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

    if (args.test):
        # Build the grid for diagnostic purposes
        grid.append(data)
    else:
        # Tell the matrix what this column should look like
        send_command(0x07, [i] + data)

# Display the data
if (args.test):
    # Print a display of the LED brightnesses, with errors (in gridsize, or in brightness out of bounds) marked in red
    cprint("LED Size:", "light_yellow", attrs=['underline'])
    if (len(grid)==9):
        cprint(str(len(grid)), end=":[")
    else:
        cprint(str(len(grid)), 'red', attrs=['bold'], end=":[")
    count = 0;
    for col in grid:
        count += 1
        if (len(col)==34):
            cprint(str(len(col)), end="")
        else:
            cprint(str(len(col)), 'red', attrs=['bold'], end="")
        if (count != len(grid)):
            print(":", end="")
    print("]")

    cprint("LED Pattern:", "light_yellow", attrs=['underline'])
    # Rotate the grid, so the pattern displayed is aligned with the phyiscal LED grid
    grid = numpy.fliplr(numpy.rot90(grid, 3))
    for row in grid:
        for led in row:
            if (led >= 1 and led <= 255):
                cprint(str(led).zfill(3), end=" ")
            elif (led == 0):
                cprint(str(led).zfill(3), 'dark_grey', end=" ");
            else:
                cprint(str(led).zfill(3), 'red', attrs=['bold'], end=" ");
        print("")

else:
    send_command(0x08, []);

