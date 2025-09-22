import pygame
import sys
import random
from pygame.math import Vector2

# --- Game setup ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# snake cklass - handles movement and growth


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        if len(self.body) > 1:
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1, 0):
                self.head = self.head_left
            elif head_relation == Vector2(-1, 0):
                self.head = self.head_right
            elif head_relation == Vector2(0, 1):
                self.head = self.head_up
            elif head_relation == Vector2(0, -1):
                self.head = self.head_down
        else:
            self.head = self.head_right

    def update_tail_graphics(self):
        if len(self.body) > 1:
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1, 0):
                self.tail = self.tail_left
            elif tail_relation == Vector2(-1, 0):
                self.tail = self.tail_right
            elif tail_relation == Vector2(0, 1):
                self.tail = self.tail_up
            elif tail_relation == Vector2(0, -1):
                self.tail = self.tail_down
        else:
            self.tail = self.tail_left

    def move_snake(self):
        if self.direction == Vector2(0, 0):
            return
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

# fruit class - handles apple placement


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

# main game class _ contols game logic and screenflow


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_active = True

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        if not 0 <= head.x < cell_number or not 0 <= head.y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == head:
                self.game_over()

    def game_over(self):
        self.game_active = False

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_game_over(self):
        final_score = str(len(self.snake.body) - 3)
        game_over_surface = game_font.render("GAME OVER", True, (255, 0, 0))
        restart_surface = game_font.render(
            "Press ENTER to restart", True, (0, 0, 0))
        score_surface = game_font.render(
            f"Final Score: {final_score}", True, (0, 0, 0))

        game_over_rect = game_over_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 60))
        restart_rect = restart_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        score_rect = score_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 60))

        box_width = 400
        box_height = 180
        box_rect = pygame.Rect((screen.get_width() - box_width) // 2,
                               (screen.get_height() - box_height) // 2, box_width, box_height)
        pygame.draw.rect(screen, (240, 240, 240), box_rect)
        pygame.draw.rect(screen, (56, 74, 12), box_rect, 4)

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(restart_surface, restart_rect)

    def draw_start_screen(self):
        title_surface = game_font.render("SNAKE GAME", True, (0, 128, 0))
        message_surface = game_font.render(
            "Press ENTER to start", True, (0, 0, 0))

        title_rect = title_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 40))
        message_rect = message_surface.get_rect(
            center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 40))

        box_width = 400
        box_height = 140
        box_rect = pygame.Rect((screen.get_width() - box_width) // 2,
                               (screen.get_height() - box_height) // 2, box_width, box_height)
        pygame.draw.rect(screen, (240, 240, 240), box_rect)
        pygame.draw.rect(screen, (56, 74, 12), box_rect, 4)

        screen.blit(title_surface, title_rect)
        screen.blit(message_surface, message_rect)


main_game = MAIN()
game_state = "start"

# Main loop - handles events and updates
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "playing":
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
        elif game_state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_game.snake.reset()
                main_game.fruit.randomize()
                main_game.game_active = True
                game_state = "playing"
        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_game.snake.reset()
                main_game.fruit.randomize()
                main_game.game_active = True
                game_state = "playing"

    screen.fill((175, 215, 70))
    if game_state == "playing":
        main_game.draw_elements()
        if not main_game.game_active:
            game_state = "game_over"
    elif game_state == "start":
        main_game.draw_start_screen()
    elif game_state == "game_over":
        main_game.draw_game_over()

    pygame.display.update()
    clock.tick(60)
