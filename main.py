import pygame
import random

# Ініціалізація pygame
pygame.init()
pygame.mixer.init()

# Загрузка звуків
try:
    bounce_sound = pygame.mixer.Sound("pong-ish-163058.mp3")
    button_click_sound = pygame.mixer.Sound("otskok-myacha.mp3")
    background_music = "underwater-309016.mp3"
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

except pygame.error as e:
    print(f"Помилка при завантаженні звуків: {e}")
    pygame.quit()
    exit()

# Колір фону
back = (173, 177, 178)

# Розміри вікна
window_width, window_height = 300, 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Функція для малювання кнопок
def draw_button(text, rect, color, hover_color, font):
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(window, button_color, rect, border_radius=8)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

# Функція для відображення меню
def show_menu():
    menu = True
    mode_selected = None
    font = pygame.font.Font(None, 40)
    title = font.render("Пинг-Понг", True, (255, 255, 0))
    button1 = pygame.Rect(window_width // 2 - 75, window_height // 2 - 40, 150, 40)
    button2 = pygame.Rect(window_width // 2 - 75, window_height // 2 + 20, 150, 40)
    
    while menu:
        window.fill((30, 30, 30))
        window.blit(title, (window_width // 2 - 60, window_height // 3 - 60))
        draw_button("Два ігрока", button1, (50, 50, 150), (80, 80, 200), font)
        draw_button("Против бота", button2, (50, 50, 150), (80, 80, 200), font)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_click_sound.play()
                if button1.collidepoint(event.pos):
                    mode_selected = "two_players"
                    menu = False
                if button2.collidepoint(event.pos):
                    mode_selected = "bot"
                    menu = False
    return mode_selected

# Функція паузи гри
def pause_game():
    paused = True
    font = pygame.font.Font(None, 36)
    button_resume = pygame.Rect(window_width // 2 - 75, window_height // 2 - 40, 150, 40)
    button_menu = pygame.Rect(window_width // 2 - 75, window_height // 2 + 20, 150, 40)
    
    while paused:
        window.fill((50, 50, 50))
        draw_button("Продовжити", button_resume, (50, 150, 50), (80, 200, 80), font)
        draw_button("В меню", button_menu, (150, 50, 50), (200, 80, 80), font)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_click_sound.play()
                if button_resume.collidepoint(event.pos):
                    paused = False
                if button_menu.collidepoint(event.pos):
                    return True
    return False

# Функція для перезавантаження гри
def restart_game():
    global player1_x, player2_x, ball_x, ball_y, dx, dy, game_over
    player1_x = (window_width - racket_width) // 2
    player2_x = (window_width - racket_width) // 2
    ball_x = window_width // 2
    ball_y = window_height // 2
    dx = random.choice([-3, 3])
    dy = 3
    game_over = False

# Функція для малювання кнопки паузи
def draw_pause_button():
    font = pygame.font.Font(None, 30)
    pause_button = pygame.Rect(window_width - 50, 10, 40, 30)
    draw_button("II", pause_button, (100, 100, 100), (150, 150, 150), font)
    return pause_button

# Розміри та початкові значення
racket_width = 100
racket_height = 15
racket_speed = 6
player1_x = (window_width - racket_width) // 2
player1_y = 40
player2_x = (window_width - racket_width) // 2
player2_y = window_height - 60

dx = random.choice([-3, 3])
dy = 3
ball_x = window_width // 2
ball_y = window_height // 2

game_active = True
game_over = False  # ініціалізація game_over на початку

# Основний цикл гри
while game_active:
    mode = show_menu()
    restart_game()
    
    while not game_over:
        window.fill(back)
        pause_button = draw_pause_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and pause_button.collidepoint(event.pos):
                if pause_game():
                    game_over = True
        
        # Оновлення позиції м'яча
        ball_x += dx
        ball_y += dy

        # Відскок від стін
        if ball_x <= 0 or ball_x >= window_width - 10:
            dx *= -1

        # Відскок від ракеток
        if (player1_y <= ball_y <= player1_y + racket_height and player1_x <= ball_x <= player1_x + racket_width) or \
           (player2_y - 10 <= ball_y <= player2_y and player2_x <= ball_x <= player2_x + racket_width):
            dy *= -1
            dx = random.choice([-3, 3])
            bounce_sound.play()

        # Перемога гравців
        if ball_y > window_height:
            print("ігрок 1 вийграв!")
            game_over = True
        if ball_y < 0:
            print("ігрок 1 вийграв!")
            game_over = True

        # Малювання елементів гри
        pygame.draw.rect(window, (0, 0, 255), (player1_x, player1_y, racket_width, racket_height))
        pygame.draw.rect(window, (255, 0, 0), (player2_x, player2_y, racket_width, racket_height))
        pygame.draw.circle(window, (0, 255, 0), (ball_x, ball_y), 10)

        pygame.display.update()
        clock.tick(60)

pygame.quit()

