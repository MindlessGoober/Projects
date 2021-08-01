"""
This is a complete pong game file.
"""

import random
import sys

import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
FPS = 120


class Ball:
    """
    This is a class that defines everything related to ball.
    """

    def __init__(self, speed):
        self.object = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
        self.velocity = pygame.Vector2((speed * random.choice((1, -1)),
                                        speed * random.choice((1, -1))))

    def move(self, player_right, player_left):
        """
        This is a function for move ball game mechanics.
        """
        self.object.x += self.velocity.x
        self.object.y += self.velocity.y
        if self.object.top <= 0 or self.object.bottom >= screen_height:
            self.velocity.y *= -1.0
        if self.object.colliderect(player_right.object):
            self.velocity.x *= -1.01
        elif self.object.colliderect(player_left.object):
            self.velocity.x *= -1.01
        elif self.object.left <= 0:
            self.velocity.x *= -0.99
            player_right.score += 1
        elif self.object.right >= screen_width:
            self.velocity.x *= -0.99
            player_left.score += 1


class Paddle:
    """
    This is a class that defines everything related to paddle.
    """

    def __init__(self, dimensions, speed, score, position):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.speed = speed
        self.score = score
        self.object = pygame.Rect(position[0], position[1], dimensions[0], dimensions[1])

    def move(self, ball=None):
        """
        This is a function for move paddle game mechanics.
        """
        self.object.top = max(self.object.top, 0)
        self.object.bottom = min(self.object.bottom, screen_height)


class Player(Paddle):
    """
    This is a class that defines everything related to player.
    """

    def move(self, ball=None):
        """
        This is a function for move player game mechanics.
        """
        self.object.y += self.speed
        super().move()


class AI(Paddle):
    """
    This is a class that defines everything related to AI.
    """

    def __init__(self, dimensions, speed, score):
        position = (0, (screen_height - dimensions[1]) // 2)
        super().__init__(dimensions, speed, score, position)

    def move(self, ball=None):
        """
        This is a function for AI game mechanics.
        """
        self.object.y += int(self.object.top < ball.object.y) * self.speed
        self.object.y -= int(self.object.bottom > ball.object.y) * self.speed
        super().move()


def display_menu_text(title, text_options):
    """
    This is a function to display menu text for title & options.
    """
    screen.fill(pygame.Color('black'))
    cur_y = screen_height // 1024
    screen.blit(title, ((screen_width - title.get_width()) // 2, cur_y))
    prev = title
    for text_option in text_options:
        cur_y += prev.get_height()
        screen.blit(text_option, ((screen_width - text_option.get_width()) // 2, cur_y))
        prev = text_option
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


def create_menu_text(title, selected, options):
    """
    This is a function to create menu text for tile & options.
    """
    text_title = pygame.font.Font(None, screen_height // 2).render(title, True,
                                                                   pygame.Color('white'))
    text_options = []
    for option in options:
        text_options.append(pygame.font.Font(None, screen_height // (len(options) + 1)).render(
            option, True, pygame.Color('yellow' if selected == option else 'white')))
    return text_title, text_options


def versus_menu(speed, mode):
    """
    This is a function for versus menu options.
    """
    selected = 0
    options = ('ai', 'player', 'quit')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_BACKSPACE:
                    main_menu()
                if event.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = min(2, selected + 1)
                if event.key == pygame.K_RETURN:
                    if options[selected] == 'quit':
                        pygame.quit()
                        sys.exit()
                    else:
                        ball = Ball(speed)
                        dimensions = (16, 128)
                        player_right_x = screen_width - dimensions[0]
                        player_left_x = 0
                        player_right_y = (screen_height - dimensions[1]) // 2
                        player_left_y = player_right_y
                        player_right = Player(dimensions, 0, 0, (player_right_x, player_right_y))
                        player_left = Player(dimensions, 0, 0, (player_left_x, player_left_y))
                        if options[selected] == 'ai':
                            player_left = AI((16, 128), speed, 0)
                        if mode == 'arcade':
                            arcade(ball, player_right, player_left, speed, options[selected])
                        else:
                            endless(ball, player_right, player_left, speed, options[selected])
        title, text_options = create_menu_text('VERSUS', options[selected], options)
        display_menu_text(title, text_options)


def main_menu():
    """
    This is a function for main menu window.
    """
    selected = 0
    options = ('arcade', 'endless', 'quit')
    speed = 7
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = min(2, selected + 1)
                if event.key == pygame.K_RETURN:
                    if options[selected] == 'quit':
                        pygame.quit()
                        sys.exit()
                    else:
                        versus_menu(speed, options[selected])
        title, text_options = create_menu_text('PONG', options[selected], options)
        display_menu_text(title, text_options)


def game_event(ball1, player_right, player_left, speed, versus):
    """
    This is a function to handle game events like key press.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_BACKSPACE:
                main_menu()
            if event.key == pygame.K_UP:
                player_right.speed -= speed
            if event.key == pygame.K_DOWN:
                player_right.speed += speed
            if versus != 'ai':
                if event.key == pygame.K_w:
                    player_left.speed -= speed
                if event.key == pygame.K_s:
                    player_left.speed += speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_right.speed += speed
            if event.key == pygame.K_DOWN:
                player_right.speed -= speed
            if versus != 'ai':
                if event.key == pygame.K_w:
                    player_left.speed += speed
                if event.key == pygame.K_s:
                    player_left.speed -= speed
    ball1.move(player_right, player_left)
    player_right.move()
    if versus == 'ai':
        player_left.move(ball1)
    else:
        player_left.move()
    screen.fill(pygame.Color('grey12'))
    pygame.draw.rect(screen, pygame.Color('yellow'), player_right.object)
    pygame.draw.rect(screen, pygame.Color('yellow'), player_left.object)
    pygame.draw.ellipse(screen, pygame.Color('white'), ball1.object)
    pygame.draw.aaline(screen, pygame.Color('white'), (screen_width // 2, 0),
                       (screen_width // 2, screen_height))
    font = pygame.font.Font(None, 60)
    player_right_name = 'Our' if versus == 'ai' else 'Player Right'
    player_left_name = 'AI' if versus == 'ai' else 'Player Left'
    text_player_right_score = font.render(player_right_name + " Score: " + str(player_right.score),
                                          True, pygame.Color('white'))
    screen.blit(text_player_right_score, (screen_width // 2 + 30, 30))
    text_player_left_score = font.render(player_left_name + " Score: " + str(player_left.score),
                                         True, pygame.Color('white'))
    screen.blit(text_player_left_score,
                (screen_width // 2 - 30 - text_player_left_score.get_width(), 30))
    pygame.display.update()
    pygame.time.Clock().tick(FPS)


def endless(ball1, player_right, player_left, speed, versus='ai'):
    """
    This is a function for endless mode window.
    """
    while True:
        game_event(ball1, player_right, player_left, speed, versus)


def arcade(ball1, player_right, player_left, speed, versus='ai'):
    """
    This is a function for arcade mode window.
    """

    def end_message(winner):
        """
        This is a function to display end message & return to main menu.
        """
        text_end = pygame.font.Font(None, screen_height // 4).render(
            winner + ' WIN', True, pygame.Color('white'))
        position_x = (screen_width - text_end.get_width()) // 2
        position_y = (screen_height - text_end.get_height()) // 2
        screen.blit(text_end, (position_x, position_y))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        pygame.time.delay(2000)
        main_menu()

    while True:
        if versus == 'ai':
            if player_right.score >= 11:
                end_message('YOU')
            elif player_left.score >= 11:
                end_message('AI')
        else:
            if player_right.score >= 11:
                end_message('RIGHT PLAYER')
            elif player_left.score >= 11:
                end_message('LEFT PLAYER')
        game_event(ball1, player_right, player_left, speed, versus)


if __name__ == '__main__':
    main_menu()
