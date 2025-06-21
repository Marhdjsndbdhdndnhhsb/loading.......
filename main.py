import pygame
import sys
import random

WIDTH, HEIGHT = 600, 400
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def render_ascii_art(ascii_art, x, y, color=BLACK, line_height=20):
    lines = ascii_art.strip().split('\n')
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, color)
        screen.blit(text_surf, (x, y + i * line_height))


rock = "✊"
scissors = "✌"
paper = "✋"

CHOICES = ["Камінь", "Ножиці", "Папір"]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Камінь-Ножиці-Папір")
clock = pygame.time.Clock()

IMAGE_SIZE = 80
font = pygame.font.SysFont("Segoe UI Symbol", IMAGE_SIZE)

# Важливо: приберіть усі зайві пробіли на початку цих рядків
rock_img = font.render(rock, True, "#F0E68C")
scissors_img = font.render(scissors, True, "#F0E68C")
paper_img = font.render(paper, True, "#F0E68C")

# Важливо: приберіть усі зайві пробіли на початку цих рядків
rock_img = pygame.transform.scale(rock_img, (IMAGE_SIZE, IMAGE_SIZE))
scissors_img = pygame.transform.scale(scissors_img, (IMAGE_SIZE, IMAGE_SIZE))
paper_img = pygame.transform.scale(paper_img, (IMAGE_SIZE, IMAGE_SIZE))

CHOICE_IMAGES = {
    "Камінь": rock_img,
    "Ножиці": scissors_img,
    "Папір": paper_img
}

player_score = 0
computer_score = 0
player_choice = None
computer_choice = None
result_message = ""

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def game_loop():
    global player_score, computer_score, player_choice, computer_choice, result_message

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Перевіряємо клік на кнопках
                # Замість діапазонів 100-200, 250-350, 400-500, краще використовувати фактичні позиції зображень.
                # Але для початку, якщо це працює, залишимо так.
                if 100 <= mouse_x <= 200 and 200 <= mouse_y <= 250:
                    player_choice = "Камінь"
                elif 250 <= mouse_x <= 350 and 200 <= mouse_y <= 250:
                    player_choice = "Ножиці"
                elif 400 <= mouse_x <= 500 and 200 <= mouse_y <= 250:
                    player_choice = "Папір"
                elif 250 <= mouse_x <= 350 and 300 <= mouse_y <= 350: # Кнопка "Ще раз"
                    player_choice = None
                    computer_choice = None
                    result_message = ""
                    # Скидаємо рахунок лише тут, якщо це кнопка "Ще раз"
                    # Якщо ви хочете скидати рахунок за бажанням, потрібно додати окрему кнопку
                    # Або скидати його лише на початку гри
                    # player_score = 0
                    # computer_score = 0

                # Важливо: цей if повинен бути на тому ж рівні відступу, що й попередні if/elif,
                # щоб він спрацьовував після обробки кліків
                if player_choice and result_message == "":
                    computer_choice = random.choice(CHOICES)
                    result_message = determine_winner(player_choice, computer_choice)


        screen.fill(WHITE)
        
        # Відображення кнопок вибору гравця
        screen.blit(rock_img, (110, 200))
        draw_text("Камінь", pygame.font.Font(None, 24), BLACK, 150, 260)

        screen.blit(scissors_img, (260, 200))
        draw_text("Ножиці", pygame.font.Font(None, 24), BLACK, 300, 260)

        screen.blit(paper_img, (410, 200))
        draw_text("Папір", pygame.font.Font(None, 24), BLACK, 450, 260)
        
        # Відображення результатів, якщо вибір зроблено
        if player_choice and computer_choice:
            # Зображення вибору гравця
            player_img = CHOICE_IMAGES.get(player_choice)
            if player_img:
                screen.blit(player_img, (WIDTH // 4 - IMAGE_SIZE // 2, 50))
                draw_text(f"Ви: {player_choice}", pygame.font.Font(None, 24), BLACK, WIDTH // 4, 50 + IMAGE_SIZE + 10)
            
            # Зображення вибору комп'ютера
            computer_img = CHOICE_IMAGES.get(computer_choice)
            if computer_img:
                screen.blit(computer_img, (3 * WIDTH // 4 - IMAGE_SIZE // 2, 50))
                draw_text(f"Комп'ютер: {computer_choice}", pygame.font.Font(None, 24), BLACK, 3 * WIDTH // 4, 50 + IMAGE_SIZE + 10)
            
            # Повідомлення про результат
            draw_text(result_message, pygame.font.Font(None, 36), BLACK, WIDTH // 2, 200)
            
            # Відображення рахунку, коли є результат
            draw_text(f"Рахунок: Ви {player_score} - Комп'ютер {computer_score}",
                      pygame.font.Font(None, 36), BLACK, WIDTH // 2, 20)
        else:
            # Повідомлення про вибір, коли результату ще немає
            draw_text("Зробіть свій вибір!", pygame.font.Font(None, 36), BLACK, WIDTH // 2, 100)
            # Рахунок також відображається, коли вибору ще немає
            draw_text(f"Рахунок: Ви {player_score} - Комп'ютер {computer_score}",
                      pygame.font.Font(None, 36), BLACK, WIDTH // 2, 20)

        # Кнопка "Ще раз"
        pygame.draw.rect(screen, GRAY, (250, 300, 100, 50))
        draw_text("Ще раз", pygame.font.Font(None, 30), BLACK, 300, 325)
        
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

def determine_winner(player, computer):
    global player_score, computer_score
    if player == computer:
        return "Нічия!"
    elif (player == "Камінь" and computer == "Ножиці") or \
         (player == "Ножиці" and computer == "Папір") or \
         (player == "Папір" and computer == "Камінь"):
        player_score += 1
        return "Ви перемогли!"
    else:
        computer_score += 1
        return "Комп'ютер переміг!"

if __name__ == "__main__":
    game_loop()

 
    
  
