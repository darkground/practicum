from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 80
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
SPEED = 4

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка - Очки: 1 (Рекорд: 0)')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Игровой объект"""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Нарисовать игровой объект на экране"""


class Apple(GameObject):
    """Класс для яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def randomize_position(self, snake):
        """Случайно изменить позицию яблока"""
        position = snake.positions[0]
        while position in snake.positions:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
        self.position = position

    def draw(self):
        """Отрисовать яблоко на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self):
        """Обновить направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку на экране"""
        head_pos = self.get_head_position()
        ofs_pos = (
            (self.direction[0] * GRID_SIZE),
            (self.direction[1] * GRID_SIZE)
        )
        new_pos = (
            (ofs_pos[0] + head_pos[0]) % (GRID_WIDTH * GRID_SIZE),
            (ofs_pos[1] + head_pos[1]) % (GRID_HEIGHT * GRID_SIZE)
        )
        self.positions.insert(0, new_pos)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовать змейку на экране"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Получить позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбросить состояние змейки"""
        self.length = 1
        self.last = None
        self.positions = [
            ((GRID_SIZE // 2) * GRID_WIDTH, (GRID_SIZE // 2) * GRID_HEIGHT)
        ]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обработка клавиш"""
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
    """Главная функция Pygame"""
    # Инициализация PyGame:
    pygame.init()

    best_score = 0
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            pygame.display.set_caption(
                f'Змейка - Очки: {snake.length} (Рекорд: {best_score})'
            )
            apple.randomize_position(snake)

        if snake.positions[0] in snake.positions[1:]:
            best_score = max(best_score, snake.length)
            snake.reset()
            pygame.display.set_caption(
                f'Змейка - Очки: 1 (Рекорд: {best_score})'
            )

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
