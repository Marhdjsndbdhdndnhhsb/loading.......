"""
Модуль, що реалізує гру "Камінь-Ножиці-Папір" з графічним інтерфейсом за допомогою бібліотеки Pygame.
Графічний інтерфейс дозволяє гравцеві взаємодіяти з грою за допомогою миші.
"""

# --- Імпорт необхідних бібліотек ---
import pygame  # Бібліотека для розробки ігор та мультимедійних застосунків.
import sys     # Модуль для взаємодії з системними параметрами, наприклад, для виходу з програми.
import random  # Модуль для генерації випадкових чисел (використовується для вибору комп'ютера).

# --- Глобальні константи для налаштування вікна гри ---
WIDTH, HEIGHT = 600, 400  # Розміри вікна у пікселях (ширина, висота).
FPS = 30                 # Кількість кадрів на секунду. Визначає швидкість оновлення екрану.

# --- Визначення кольорів у форматі RGB ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- Налаштування ігрових елементів та вікна ---

# Unicode-символи для представлення вибору.
rock = "✊"
scissors = "✌"
paper = "✋"

# Список усіх можливих варіантів вибору.
CHOICES = ["Камінь", "Ножиці", "Папір"]

# Ініціалізація Pygame.
pygame.init()

# Створення об'єкта вікна (дисплея).
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Встановлення заголовка вікна.
pygame.display.set_caption("Камінь-Ножиці-Папір")
# Створення об'єкта для відстеження часу (контроль FPS).
clock = pygame.time.Clock()

# Розмір графічних символів у пікселях.
IMAGE_SIZE = 80
# Створення об'єкта шрифту, який підтримує Unicode-символи.
font = pygame.font.SysFont("Segoe UI Symbol", IMAGE_SIZE)

# Рендеринг (малювання) Unicode-символів на поверхні Pygame.
# True - для згладжування (antialiasing), "#F0E68C" - колір символів.
rock_img = font.render(rock, True, "#F0E68C")
scissors_img = font.render(scissors, True, "#F0E68C")
paper_img = font.render(paper, True, "#F0E68C")

# Масштабування рендерених символів до потрібного розміру.
rock_img = pygame.transform.scale(rock_img, (IMAGE_SIZE, IMAGE_SIZE))
scissors_img = pygame.transform.scale(scissors_img, (IMAGE_SIZE, IMAGE_SIZE))
paper_img = pygame.transform.scale(paper_img, (IMAGE_SIZE, IMAGE_SIZE))

# Словник для зручного доступу до зображень за назвою вибору.
CHOICE_IMAGES = {
    "Камінь": rock_img,
    "Ножиці": scissors_img,
    "Папір": paper_img
}

# --- Змінні для збереження стану гри ---
player_score = 0
computer_score = 0
player_choice = None
computer_choice = None
result_message = ""

# --- Функції гри ---

def draw_text(text, font, color, x, y):
    """
    Відображає заданий текст на екрані Pygame, вирівнюючи його по центру.

    Args:
        text (str): Текст, який потрібно відобразити.
        font (pygame.font.Font): Об'єкт шрифту Pygame для рендерингу тексту.
        color (tuple): Колір тексту у форматі RGB.
        x (int): X-координата центру тексту.
        y (int): Y-координата центру тексту.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def determine_winner(player, computer):
    """
    Визначає переможця в раунді гри "Камінь-Ножиці-Папір".

    Оновлює глобальні змінні `player_score` та `computer_score`.

    Args:
        player (str): Вибір гравця ("Камінь", "Ножиці" або "Папір").
        computer (str): Випадковий вибір комп'ютера.

    Returns:
        str: Повідомлення про результат гри: "Нічия!", "Ви перемогли!" або "Комп'ютер переміг!".
    """
    global player_score, computer_score
    if player == computer:
        # Умова нічиєї.
        return "Нічия!"
    elif (player == "Камінь" and computer == "Ножиці") or \
         (player == "Ножиці" and computer == "Папір") or \
         (player == "Папір" and computer == "Камінь"):
        # Умови перемоги гравця.
        player_score += 1
        return "Ви перемогли!"
    else:
        # Усі інші комбінації призводять до перемоги комп'ютера.
        computer_score += 1
        return "Комп'ютер переміг!"


def game_loop():
    """
    Основний цикл гри.

    Обробляє події (ввід користувача), оновлює логіку гри та малює всі елементи
    на екрані в кожному кадрі.
    """
    # Доступ до глобальних змінних для їх зміни.
    global player_score, computer_score, player_choice, computer_choice, result_message

    running = True
    while running:
        # --- Обробка подій ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Закриття вікна.
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Обробка кліків миші.
                mouse_x, mouse_y = event.pos

                # Перевірка, чи клік був на одній з кнопок вибору.
                if 100 <= mouse_x <= 200 and 200 <= mouse_y <= 250:
                    player_choice = "Камінь"
                elif 250 <= mouse_x <= 350 and 200 <= mouse_y <= 250:
                    player_choice = "Ножиці"
                elif 400 <= mouse_x <= 500 and 200 <= mouse_y <= 250:
                    player_choice = "Папір"
                elif 250 <= mouse_x <= 350 and 300 <= mouse_y <= 350:
                    # Логіка для кнопки "Ще раз".
                    player_choice = None
                    computer_choice = None
                    result_message = ""
                
                # Запуск логіки раунду, якщо гравець зробив вибір і раніше не було результату.
                if player_choice and result_message == "":
                    computer_choice = random.choice(CHOICES)
                    result_message = determine_winner(player_choice, computer_choice)

        # --- Оновлення графіки на екрані ---
        screen.fill(WHITE)
        
        # Відображення кнопок вибору гравця.
        screen.blit(rock_img, (110, 200))
        draw_text("Камінь", pygame.font.Font(None, 24), BLACK, 150, 260)
        screen.blit(scissors_img, (260, 200))
        draw_text("Ножиці", pygame.font.Font(None, 24), BLACK, 300, 260)
        screen.blit(paper_img, (410, 200))
        draw_text("Папір", pygame.font.Font(None, 24), BLACK, 450, 260)
        
        # Відображення вибору гравця, комп'ютера та результату.
        if player_choice and computer_choice:
            player_img = CHOICE_IMAGES.get(player_choice)
            if player_img:
                screen.blit(player_img, (WIDTH // 4 - IMAGE_SIZE // 2, 50))
                draw_text(f"Ви: {player_choice}", pygame.font.Font(None, 24), BLACK, WIDTH // 4, 50 + IMAGE_SIZE + 10)
            computer_img = CHOICE_IMAGES.get(computer_choice)
            if computer_img:
                screen.blit(computer_img, (3 * WIDTH // 4 - IMAGE_SIZE // 2, 50))
                draw_text(f"Комп'ютер: {computer_choice}", pygame.font.Font(None, 24), BLACK, 3 * WIDTH // 4,
                          50 + IMAGE_SIZE + 10)
            draw_text(result_message, pygame.font.Font(None, 36), BLACK, WIDTH // 2, 200)

        # Відображення поточного рахунку.
        draw_text(f"Рахунок: Ви {player_score} - Комп'ютер {computer_score}",
                  pygame.font.Font(None, 36), BLACK, WIDTH // 2, 20)

        # Малювання кнопки "Ще раз".
        pygame.draw.rect(screen, GRAY, (250, 300, 100, 50))
        draw_text("Ще раз", pygame.font.Font(None, 30), BLACK, 300, 325)
        
        # Оновлення екрану.
        pygame.display.flip()
        # Обмеження частоти кадрів.
        clock.tick(FPS)

    # --- Завершення програми ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Цей блок запускає головний ігровий цикл, коли скрипт виконується як основна програма.
    game_loop()

   
