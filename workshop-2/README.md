# Workshop Two

## Catching up

If you missed part one of this workshop, click [here](https://github.com/gdscwm/snake/tree/main/workshop-1) to get
things set up. You can skip creating the virtual environment, and copy and paste the code from snake.py into a file on
your system.

## Snake!

Last time, we finished our `Cube` class, which is what our snake and snacks are going to be made out of. Let's put some
cubes together to make our `Snake` class.

The snake has two important things to keep track of: the cubes it's made up of, and where it's moving. Let's represent
these two things with a list of cubes called `body`, and a dictionary called `turns`. We need to know at what position
on the board the player made the snake turn, so that the rest of the snake body can follow suit. Turns is therefore
going to store the position on the board as a key, and the direction to turn as that key's value.

```python
class Snake():

    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
```

Our init method for our snake creates that `body` list and `turns` dict, then initializes a couple other important
things.
Line by line:

- Assign a color to the snake, passed in when the snake is declared in `main`
- Create a cube object to act as the head of the snake, and place it at `pos` on the game board (an array with the x and
  y coordinates of the starting position, passed in when the snake is declared in `main`)
- Add the head cube to our snake

Let's also write the `draw` method for our snake. Again, since he's made up of cubes, we just have to call the `draw`
method of our `Cube` class for each cube in the body of our snake:

```python
class Snake:
    # ... some other code here
    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)
```

---

### Optional excursion: the snakes have eyes

It would be nice if we had some way of differentiating the head of the snake from the rest of the body, so we're clear
on where it's headed. Add some logic to `Cube`'s `draw` method so that the head is distinguishable from the body when
the `eyes` parameter is True. You could make it a different color, or try exploring some
of [Pygame's draw methods](https://www.pygame.org/docs/ref/draw.html) to add
some eyes to your snake.

---

### Heads, no tails

Let's see our lil guy in action!!

First, let's update our `redraw_surface` function to call our snake's new `draw` method:

```python
def redraw_surface(surface, snake):
    surface.fill(SURFACE_COL)
    draw_grid(surface)
    snake.draw(surface)  # line added here
    pygame.display.update()
```

And then slither on down to `main`, where we're going to initialize our snake, and also add
a `if __name__ == '__main__'`
safeguard for running our program:

```python
def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))
    snake = Snake(SNAKE_COL, (10, 10))  # line added here

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        redraw_surface(surface, snake)


if __name__ == '__main__':
    main()
```

Run

```shell
python3 snake.py
```

in your terminal or IDE's built-in shell. (If this doesn't work, try just `python snake.py`.) The game board should pop
up with a colored cube (the head of our snake!) at position (10, 10) on the screen.

### Look at him go!

Next on the agenda is to get our snake to slither around the screen. Let's start by writing a `get_input` method for our
snake class to have our snake respond to the player pressing the arrow keys.

```python
class Snake:
    # ... init code here
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # see which keys are being pressed

            if keys[pygame.K_LEFT]:
                # mark this space on the board with how the body should turn
                self.turns[self.head.pos] = [-1, 0]
            elif keys[pygame.K_RIGHT]:
                self.turns[self.head.pos] = [1, 0]
            elif keys[pygame.K_UP]:
                self.turns[self.head.pos] = [0, -1]
            elif keys[pygame.K_DOWN]:
                self.turns[self.head.pos] = [0, 1]
```

Line by line:

- The first three lines we move out of main and into the `get_input` function, to keep user input checking all in the
  same place. These aren't important to our game, but Pygame requires them to run the game.
- `keys = pygame.key.get_pressed()`: `key.get_pressed` is a Pygame function returning a sequence of boolean values
  representing the state of every key on the keyboard. If a button is pressed, the corresponding boolean is True.
- `if keys[pygame.K_LEFT]` indexes our `keys` array to get the boolean value for the left arrow button on the keyboard.
  If True, it
- `self.turns[self.head.pos] = [-1, 0]` adds the position of the head of the snake to our `turns` dictionary as a key,
  and
  sets its value to [-1, 0], the [x, y] values to make our snake move left. What this is actually doing is marking the
  snake's head position on the board with the turning direction, so every subsequent body cube turns there as well.
- These two lines repeat to cover all directional cases.

Next, our `move` method. Big picture: we go through every cube in the snake body, and tell it where to move.
Line-by-line below.

```python
class Snake:
    # __init__ ...
    # get_input() ...

    def move(self):
        self.get_input()

        for i, cube, in enumerate(self.body):
            p = cube.pos
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                cube.move(cube.dirx, cube.diry)
```

- We call `self.get_input()` to check our key presses. Our snake can only move a single space in a single direction at a
  time, so it's sufficient to check for key presses just once each time the snake moves.
- `for i, cube, in enumerate(self.body):`: `enumerate` is a nice succinct little function that takes an iterable as a
  parameter (here, our snake body list) and returns an iterator with index and element pairs from the original iterable.
  I.e., we are making a for loop that keeps track if `i`, the numerical index of where we are in the list, and `cube`,
  the
  actual cube object stored in the list at that index.
- `p = cube.pos` makes a variable `p` to store the position of the cube we're on.
- If the cube's current position is in our `turns` dictionary, that means the cube should change direction (turn) now.
    - `turn = self.turns[p]` gets the directional [x, y] pair stored at that position on the board
    - `cube.move(turn[0], turn[1])` calls the Cube class's `move` method to move it one space in the direction of the
      turn. Cube movement is explained in workshop-1's README.
    - `if i == len(self.body) - 1` checks if the cube is the tail of the snake, i.e. the last cube in the list. If it
      is,
      we pop that turn from the dictionary so the snake doesn't turn on that square every time it hits it in the future.
- If the cube's current position is not in our `turns` dictionary, we move the cube one space in whatever direction it
  was already heading.

While we're here, let's also fill in the `reset` method of our `Snake` class. This spawns a new snake when something
happens to make the old one die. It looks a lot like our initializer, because we're keeping all the variables the same,
just emptying out our `body` and `turns` collections and making a new snake head.

```python
class Snake:
    # __init__ ...
    # get_input() ...
    # move ...

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
```

Down in main, we now want to call `snake.move()` to get him slithering. If you ran your game now, you'd see a little
streak of purple that quickly disappears and leaves you with a blank grid. This is because we haven't added any time
constraints to our game that tell the snake how fast it can move. We add those with Pygame's `time.delay` function.

```python
def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))
    snake = Snake(SNAKE_COL, (10, 10))

    while True:
        # notice our for event loop is gone since we moved that up to get_input()

        pygame.time.delay(80)  # this sets an 80 millisecond interval between snake moves
        snake.move()  # get the snake moving

        redraw_surface(surface, snake)
```

Try running the game now. Our little cube moves around the screen when you press the arrow buttons! We do still need to
add some logic about what to do when the snake hits the edges of the screen, though.

We can do this by getting the position of the head of the snake, and checking to see if either the x or y positional
values are outside the game board, i.e. greater than or equal to the number of rows or less than 0. If they are, we give
the user their score (how long the snake was), and reset the game.

```python
def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))
    snake = Snake(SNAKE_COL, (10, 10))

    while True:
        pygame.time.delay(80)
        snake.move()

        head_pos = snake.head.pos
        if head_pos[0] >= 20 or head_pos[0] < 0 or head_pos[1] >= 20 or head_pos[1] < 0:
            print("Score:", len(snake.body))
            snake.reset((10, 10))

        redraw_surface(surface, snake)
```

---

### Optional excursion: infinite snake

Some versions of the snake game allow the snake to loop around the edges of the screen, i.e., when it hits the edge of
the board, it reappears in the same row or column but on the opposite side of the board. How would you change the `move`
function for `Snake` to let this happen?

---

### Snake snack

We have a board! We have a snake! To make this a working game, the last thing we need to do is add a snack somewhere on
the board for the snake to eat and grow.

To take care of the snake growing when it eats a snack, we need to fill in the `add_cube` function in our `Snake` class.

```python
class Snake:
    # ... some code here
    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy
```

Line-by-line:

- Find the tail of the snake, i.e. the last cube in the body
- Assign `dx` and `dy` to the (x, y) direction of the tail cube
- Our if/elif block checks which direction the tail was going in, and creates a new cube adjacent to the tail in the
  opposite direction
- The last two lines assign the newly added tail cube its (x, y) direction pair

Next, we'll fill in our `random_snack` function:

```python
def random_snack(snake):
    positions = snake.body

    while True:
        x = random.randrange(0, ROWS - 1)
        y = random.randrange(0, ROWS - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y
```

Line-by-line:

- Copy the snake body list into a new list `positions` that we can manipulate
- Start a while loop that will run until we find a valid place to put a snack
    - Choose a random number between 0 and ROWS - 1 (the indexes of our rows and columns) for x and y
    - Our `if` statement line checks to see if the random (x, y) position we chose is also the position of a cube
      somewhere in the snake body. Click the links if you're interested in learning more about Python'
      s [filter](https://www.geeksforgeeks.org/filter-in-python/)
      and [lambda](https://www.w3schools.com/python/python_lambda.asp) functions.
    - If the snack position corresponds to a snake position, loop again. Otherwise, break the loop and return `x, y`.

To get the snack to appear on the screen, we have to update `redraw_surface`:

```python
def redraw_surface(surface, snake, snack):  # change in parameters
    surface.fill(SURFACE_COL)
    draw_grid(surface)
    snake.draw(surface)
    snack.draw(surface)  # line added
    pygame.display.update()
```

Finally, let's go back to `main` and finish out our game loop.

First, we want to initialize a snack after we do our snake, and update our `redraw_surface` function call to reflect the
new parameter.

Then, after we check if the snake went off the edges of the board, we also want to check and see if the snake runs into
itself. We use a similar lambda function as above, as well as
Python's [map](https://www.w3schools.com/python/ref_func_map.asp) function.

Finally, if the head of the snake is at the same position as the snack (i.e. the snake eats the snack), we make the
snake grow by one cube, and drop a snack somewhere else on the board.

```python
def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))
    snake = Snake(SNAKE_COL, (10, 10))
    snack = Cube(random_snack(snake), color=SNACK_COL)  # line added

    while True:
        pygame.time.delay(80)
        snake.move()

        # check if snake hits the edge of the screen
        head_pos = snake.head.pos
        if head_pos[0] >= ROWS or head_pos[0] < 0 or head_pos[1] >= ROWS or head_pos[1] < 0:
            print("Score:", len(snake.body))
            snake.reset((10, 10))

        # check if snake tries to eat itself
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print("Score:", len(snake.body))
                snake.reset((10, 10))
                break

        # check if snake eats the snack
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(snake), color=SNACK_COL)

        redraw_surface(surface, snake, snack)  # param added here
```


