# Workshop One

Welcome to DSC

## Setup

We have to do a couple things before we can get into coding the game.

### Virtual Environment

1. Create a directory for your code by opening the command line (if you're using Mac/Linux, open Terminal, if you're on
   Windows, use Powershell) and enter the following commands:

```
mkdir snake
cd snake
```

You should now be in the directory `snake`.  
\

2. Now we want to create a virtual environment in the `snake` directory. Run the following command:

```
python3 -m venv [venvname]
```

Where you replace `[venvname]` with what you want your virtual environment to be called. _We strongly recommend calling
it `.snake-venv`._  If `python3` doesn't work for you, try just `python`.
\

3. Activate your virtual environment with the following command:

```
source [venvname]/bin/activate
```

So if you named your virtual environment `.snake-venv`, the full command will look like:

```
source .snake-venv/bin/activate
```

If you're on a non-Linux system (eg Windows), consult this table to activate your virtual environment:
<img width="1379" alt="Screenshot 2023-09-19 at 3 45 01 PM" src="https://github.com/gdscwm/fastapi-workshop-series/assets/102433378/09451c6e-6280-46d4-82fc-9e567c270460">

If this command does not work for you, refer
to [the python documentation](https://docs.python.org/3/library/venv.html#how-venvs-work) for further options, and raise
your hand.  
\

4. Confirm that things are set up correctly using the following command:

```
pip list
```

you should see two packages: `pip` and `setuptools`. If it doesn't work, try replacing `pip` with `pip3`.
If you see these packages, you're ready to move on to the next section!

### File structure

In your `snake` directory, create two new files: `snake.py` and `requirements.txt`.

A requirements file tells python what dependencies it needs to install in order to run your program.
We'll be using the pygame library, so in `requirements.txt`, add the line `pygame`.

To install the things listed in `requirements.txt`, run `pip install -r requirements.txt`.
(Think about how useful this would be if we had a long list of dependencies.)

___

### Optional Excursion: pygame

If you get here before the rest of the workshop, take a moment to get familiar with the `pygame` library. Here are
their [docs](https://www.pygame.org/docs/). We'll be using these functions: `draw`, `quit`, `key.get_pressed`,
`display`, and `time`.
___

## First steps

We're familiar with the classic snake game: snake that gets longer every time it eats a snack, and dies if it runs into
itself. What functions, classes, etc would we need to implement this?

# STOP! don't scroll yet, spoilers ahead

Here's the skeleton file for our snake game.

```python
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube():
    def __init__(self):
        pass

    def move(self):
        pass

    def draw(self):
        pass


class Snake():
    def __init__(self):
        pass

    def move(self):
        pass

    def reset(self):
        pass

    def add_cube(self):
        pass

    def draw(self):
        pass


def random_snack():
    pass


def message_box():
    pass


def redraw_surface():
    pass


def draw_grid():
    pass


def main():
    pass
```

Let's start by getting our game board set up. First, we have to decide how big it's going to be – let's make it a 20x20
board with size 500. Feel free to play around with these values, but make sure for whatever values you choose, `WIDTH`
is divisible by `ROWS`.
Let's also define a few color constants we'll need - the game surface, grid, snake, and snack colors.

Add all these to the top of your file, below the import lines but outside of any functions, so we can access
them from anywhere:

```python
WIDTH = 500
ROWS = 20

SURFACE_COL = (255, 0, 0)
GRID_COL = (255, 255, 255)
SNAKE_COL = (255, 0, 255)
SNACK_COL = (0, 255, 0)
```

Quick aside: pygame recognizes colors in RGB format, which is the amount of Red, Blue, and Green in the color on a 0-255
scale. (0, 0, 0) is black, (255, 255, 255) is white, (255, 0, 0) is red, and so on.

We're going to write quite a bit of code here, but don't worry, we'll explain what it all means in a second.

```python
def redraw_surface(surface):
    surface.fill(SURFACE_COL)
    pygame.display.update()


def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        redraw_surface(surface)


main()
```

Okay, that's a lot of code. A lot of it is pygame-specific, which we won't delve too deep into, but here's what you need
to know:

- `redraw_surface` renders our game screen. It takes the `surface` object we initialize in main as a parameter.
    - `surface.fill(WIN_COL)` sets the color of our game screen to black. It uses the constant `SURFACE_COL` we defined
      at
      the very top of our file.
    - `pygame.display.update()` updates the screen. We'll get more into how this works later.
- `main` is the engine of our game. We initialize all our objects and get the game running from here.
    - We initialize `surface` to be a pygame display with dimensions `WIDTH` x `WIDTH`
    - A `while True` loop runs forever, unless something makes it `False`. Nothing does here yet, so it'll repeat the
      code in there indefinitely
    - The `for` loop here is just so that pygame is okay with us running our game. Without it, the game board wouldn't
      show up. Basically, it's looking for a sign from the game that the user quit the game, and if they do, the game
      exits.
    - `redraw_surface(surface)` calls `redraw_surface` and passes it the surface object we made
- `main()` calls our main function so that it'll run when we run the file

Let's see what this looks like! Run

```shell
python snake.py
```

in your terminal. (If that doesn't work, try replacing `python` with `python3`). A black screen should pop up. If it
doesn't, raise your hand.

It would be nice to see the grid that our snake will be able to move on, so let's add that in too:

```python
def redraw_surface(surface):
    surface.fill(SURFACE_COL)
    draw_grid(surface)  # line added here
    pygame.display.update()


def draw_grid(surface):
    square_size = WIDTH // ROWS

    x = 0
    y = 0
    for _ in range(ROWS):
        x = x + square_size
        y = y + square_size

        pygame.draw.line(surface, GRID_COL, (x, 0), (x, WIDTH))  # vertical lines
        pygame.draw.line(surface, GRID_COL, (0, y), (WIDTH, y))  # horizontal lines
```

And let's break down what `draw_grid` is doing:

- `square_size = WIDTH // ROWS` is defining how dense we want our grid to be. If you want more or less squares, try
  increasing or decreasing the `rows` variable.
- Our for loop draws two lines, vertical and horizontal, spanning the length of the surface each time it loops
    - `x` and `y` are offset by the size of our grid square
    - `pygame.draw.line(surface, GRID_COL, (x, 0), (x, WIDTH))` draws a line on the surface in white (`GRID_COL`),
      starting at the top of the surface `(x,0)` and going to the bottom `(x,WIDTH)`
    - It does the same for horizontal lines using `y`

Run `python snake.py` in your terminal again - you should see a black screen with a 20x20 white grid.
