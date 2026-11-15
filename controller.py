#!/usr/bin/python3

from termcolor import cprint
import numpy
import serial

def send_command(command_id, parameters, with_response=False):
  with serial.Serial("/dev/ttyACM0", 115200) as s:
      s.write([0x32, 0xAC, command_id] + parameters)

      if with_response:
          res = s.read(32)
          return res

def empty_grid():
    grid = []
    for i in range(9):
        row = []
        for j in range(34):
            row.append(0)
        grid.append(row)
    return grid

def output(grid):
    #Send the data to the LED matrix
    for row in range(9):
        send_command(0x07, [row] + grid[row])
    send_command(0x08, []);


def test(grid):
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