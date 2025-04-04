from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Инициализация базового класса.
    От него будут создаваться дочерние.
    """

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс, который отвечает за яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = Apple.randomize_position(self)

    def randomize_position(self):
        """Установка случайного положения яблока."""
        SCREEN_WIDTH = (randint(0, 31)) * 20
        SCREEN_HEIGHT = (randint(0, 23)) * 20
        return SCREEN_WIDTH, SCREEN_HEIGHT

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, отвечающий за змейку."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновление направляения движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        head = self.get_head_position()
        if head[0] == SCREEN_WIDTH:
            head = (-20, head[1])
        elif head[0] == -20:
            head = (SCREEN_WIDTH, head[1])
        elif head[1] == SCREEN_HEIGHT:
            head = (head[0], -20)
        elif head[1] == -20:
            head = (head[0], SCREEN_HEIGHT)

        list.insert(
            self.positions,
            0,
            (head[0] + 20 * self.direction[0],
             head[1] + 20 * self.direction[1]),
        )

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возврат головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в первоначальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        return self.length, self.positions, self.direction


def handle_keys(game_object):
    """Обработка нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описание основного цикла игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(10)
        apple.draw()
        snake.draw()
        pygame.display.update()
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            snake.move()
            apple = Apple()
            apple.draw()
            pygame.display.update()
        elif list.count(snake.positions, snake.get_head_position()) > 1:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            pygame.display.update()


if __name__ == "__main__":
    main()
