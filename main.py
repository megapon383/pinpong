import pygame
import random
import os

pygame.init()
back = (173, 177, 178)
window_width, window_height = 300, 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

def show_menu():
    menu = True
    mode_selected = None
    while menu:
        window.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text1 = font.render("натисните 1 для гри вдвоєму", True, (255, 255, 255))
        text2 = font.render("натисните 2 для гри с ботом", True, (255, 255, 255))
        window.blit(text1, (window_width // 2 - 150, window_height // 2 - 40))
        window.blit(text2, (window_width // 2 - 150, window_height // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode_selected = "two_players"
                    menu = False
                if event.key == pygame.K_2:
                    mode_selected = "bot"
                    menu = False
    return mode_selected

def restart_game():
    global player1_y, player2_y, ball_x, ball_y, dx, dy, game_over
    player1_y = (window_height - racket_height) // 2
    player2_y = (window_height - racket_height) // 2
    ball_x = window_width // 2
    ball_y = window_height // 2
    dx = 0
    dy = 3
    game_over = False

racket_width = 100
racket_height = 15
racket_speed = 6
player1_x = (window_width - racket_width) // 2
player1_y = 20
player2_x = (window_width - racket_width) // 2
player2_y = window_height - 40

dx = 0
dy = 3
ball_x = window_width // 2
ball_y = window_height // 2

p1_left = p1_right = False
p2_left = p2_right = False
game_over = False

def load_image(filename, width, height):
    if not os.path.exists(filename):
        print(f"Ошибка: файл {filename} не найден. Используется заглушка.")
        surf = pygame.Surface((width, height))
        surf.fill((255, 0, 0))  # Красный квадрат вместо изображения
        return surf
    return pygame.transform.scale(pygame.image.load(filename), (width, height))

ball_img = load_image("ball6.png", 20, 20)
racket_img = load_image("plat7.jpg", racket_width, racket_height)

game_active = True

while game_active:
    mode = show_menu()
    restart_game()
    
    while not game_over:
        window.fill(back)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p2_left = True
                if event.key == pygame.K_RIGHT:
                    p2_right = True
                if event.key == pygame.K_a:
                    p1_left = True
                if event.key == pygame.K_d:
                    p1_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    p2_left = False
                if event.key == pygame.K_RIGHT:
                    p2_right = False
                if event.key == pygame.K_a:
                    p1_left = False
                if event.key == pygame.K_d:
                    p1_right = False

        if p1_left and player1_x > 0:
            player1_x -= racket_speed
        if p1_right and player1_x < window_width - racket_width:
            player1_x += racket_speed
        if mode == "two_players":
            if p2_left and player2_x > 0:
                player2_x -= racket_speed
            if p2_right and player2_x < window_width - racket_width:
                player2_x += racket_speed
        else:
            if ball_x < player2_x + racket_width // 2:
                player2_x -= racket_speed
            if ball_x > player2_x + racket_width // 2:
                player2_x += racket_speed

        ball_x += dx
        ball_y += dy

        if ball_x <= 0 or ball_x >= window_width - 20:
            dx *= -1

        if (player1_y <= ball_y <= player1_y + racket_height and player1_x <= ball_x <= player1_x + racket_width) or \
           (player2_y - 20 <= ball_y <= player2_y and player2_x <= ball_x <= player2_x + racket_width):
            dy *= -1
            dx = random.choice([-3, 3])

        if ball_y > window_height:
            print("Игрок 1 победил!")
            game_over = True
        if ball_y < 0:
            print("Игрок 2 победил!")
            game_over = True

        window.blit(racket_img, (player1_x, player1_y))
        window.blit(racket_img, (player2_x, player2_y))
        window.blit(ball_img, (ball_x, ball_y))

        pygame.display.update()
        clock.tick(60)

pygame.quit()
