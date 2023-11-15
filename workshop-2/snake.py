import random
import pygame

WIDTH = 500
ROWS = 20

SURFACE_COL = (0, 0, 0)
GRID_COL = (255, 255, 255)
SNAKE_COL = (255, 0, 255)
SNACK_COL = (0, 255, 0)


class Cube:
    def __init__(self, start, dirx=1, diry=0, color=SNAKE_COL):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, head=False):
        dis = WIDTH // ROWS
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 1, dis - 2))

        if head:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class Snake:

    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)

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
                if cube.dirx == -1 and cube.pos[0] <= 0:
                    cube.pos = (ROWS, cube.pos[1])
                elif cube.dirx == 1 and cube.pos[0] >= ROWS - 1:
                    cube.pos = (-1, cube.pos[1])
                elif cube.diry == 1 and cube.pos[1] >= ROWS - 1:
                    cube.pos = (cube.pos[0], -1)
                elif cube.diry == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], ROWS)

                cube.move(cube.dirx, cube.diry)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}

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

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


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


def redraw_surface(surface, snake, snack):
    surface.fill(SURFACE_COL)
    draw_grid(surface)
    snake.draw(surface)
    snack.draw(surface)
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


def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))
    snake = Snake(SNAKE_COL, (10, 10))
    snack = Cube(random_snack(snake), color=SNACK_COL)

    while True:
        pygame.time.delay(80)
        snake.move()

        head_pos = snake.head.pos
        if head_pos[0] >= 20 or head_pos[0] < 0 or head_pos[1] >= 20 or head_pos[1] < 0:
            print("Score:", len(snake.body))
            snake.reset((10, 10))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print("Score:", len(snake.body))
                snake.reset((10, 10))
                break

        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(snake), color=SNACK_COL)

        redraw_surface(surface, snake, snack)


if __name__ == '__main__':
    main()
