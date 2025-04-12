import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана и рабочей области (canvas)
width = 1000
height = 680
toolbar_height = 100  # Теперь панель инструментов сверху

screen = pygame.display.set_mode((width, height))
canva = pygame.Surface((width, height - toolbar_height))

# Определение основных цветов
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)
light_grey = (150, 150, 150)

# Константы и переменные
running = True
mouse_click = False
last_mouse_pos = None
painting_mode = 'line'
scale = 2
current_color = black
start_pos = None

# Шрифты
font = pygame.font.SysFont("Leelawadee", 20)
font_small = pygame.font.SysFont("Leelawadee", 15)

# Создание кнопок инструментов в один ряд
buttons = {
    "line":                   pygame.Rect(10, 10, 90, 20),
    "rectangle":              pygame.Rect(110, 10, 90, 20),
    "circle":                 pygame.Rect(210, 10, 90, 20),
    "square":                 pygame.Rect(310, 10, 90, 20),
    "right_triangle":         pygame.Rect(410, 10, 90, 20),
    "equilateral_triangle":   pygame.Rect(510, 10, 90, 20),
    "rhombus":                pygame.Rect(610, 10, 90, 20),
    "eraser":                 pygame.Rect(710, 10, 90, 20),
    "+":                      pygame.Rect(230, 50, 30, 20),
    "-":                      pygame.Rect(270, 50, 30, 20),
    "clear":                  pygame.Rect(810, 10, 90, 20),
}

# Состояния кнопок
button_states = {mode: False for mode in buttons}

# Цветовые кнопки
color_buttons = {
    black: pygame.Rect(10, 50, 30, 30),
    blue: pygame.Rect(50, 50, 30, 30),
    red: pygame.Rect(90, 50, 30, 30),
    yellow: pygame.Rect(130, 50, 30, 30),
}

# Заливка экрана и холста
screen.fill(black)
canva.fill(white)

def draw_buttons():
    """Отрисовка кнопок инструментов и цветов."""
    for mode, rect in buttons.items():
        color = (233, 233, 233) if button_states[mode] else (light_grey if painting_mode == mode else grey)
        pygame.draw.rect(screen, color, rect)
        text = font_small.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 5, rect.y))

    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (170, 50))

    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)

def handle_events():
    """Обработка событий."""
    global running, mouse_click, last_mouse_pos, painting_mode, scale, current_color, start_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            mx, my = pygame.mouse.get_pos()

            # Нажатие на кнопки
            for mode, rect in buttons.items():
                if rect.collidepoint(mx, my):
                    if mode == "+" and scale < 30:
                        scale += 1
                    elif mode == "-" and scale > 1:
                        scale -= 1
                    elif mode == "clear":
                        canva.fill(white)
                    else:
                        painting_mode = mode
                    button_states[mode] = True

            # Выбор цвета
            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

            # Начало рисования, если мышь ниже панели
            if my >= toolbar_height:
                start_pos = (mx, my - toolbar_height)

        if event.type == pygame.MOUSEBUTTONUP:
            for mode, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    button_states[mode] = False

            mouse_click = False
            last_mouse_pos = None

            # Отрисовка фигуры
            if start_pos is not None:
                mx, my = pygame.mouse.get_pos()
                my -= toolbar_height

                dx = abs(mx - start_pos[0])
                dy = abs(my - start_pos[1])

                if painting_mode == "rectangle":
                    pygame.draw.rect(canva, current_color,
                                     (min(start_pos[0], mx), min(start_pos[1], my), dx, dy), scale)
                elif painting_mode == "circle":
                    radius = max(dx, dy) // 2
                    center = (min(start_pos[0], mx) + dx // 2, min(start_pos[1], my) + dy // 2)
                    pygame.draw.circle(canva, current_color, center, radius, scale)
                elif painting_mode == "square":
                    size = min(dx, dy)
                    pygame.draw.rect(canva, current_color,
                                     (min(start_pos[0], mx), min(start_pos[1], my), size, size), scale)
                elif painting_mode == "right_triangle":
                    points = [start_pos, (start_pos[0], my), (mx, my)]
                    pygame.draw.polygon(canva, current_color, points, scale)
                elif painting_mode == "equilateral_triangle":
                    side = max(dx, dy)
                    h = (math.sqrt(3) / 2) * side
                    x1, y1 = start_pos
                    x2, y2 = x1 + side, y1
                    x3, y3 = x1 + side / 2, y1 - h
                    pygame.draw.polygon(canva, current_color, [(x1, y1), (x2, y2), (x3, y3)], scale)
                elif painting_mode == "rhombus":
                    cx = (start_pos[0] + mx) // 2
                    cy = (start_pos[1] + my) // 2
                    points = [(cx, start_pos[1]), (mx, cy), (cx, my), (start_pos[0], cy)]
                    pygame.draw.polygon(canva, current_color, points, scale)

            start_pos = None

def update():
    """Обновление рисования линий."""
    global last_mouse_pos
    mx, my = pygame.mouse.get_pos()
    my_adj = my - toolbar_height

    if mouse_click and last_mouse_pos is not None and my_adj >= 0:
        if painting_mode == 'line':
            pygame.draw.line(canva, current_color, last_mouse_pos, (mx, my_adj), scale)
        elif painting_mode == 'eraser':
            pygame.draw.line(canva, white, last_mouse_pos, (mx, my_adj), scale)

    if mouse_click and my_adj >= 0:
        last_mouse_pos = (mx, my_adj)

def render():
    """Отрисовка экрана."""
    screen.fill(black)
    pygame.draw.rect(screen, grey, (0, 0, width, toolbar_height))
    screen.blit(canva, (0, toolbar_height))
    draw_buttons()

    # Предпросмотр фигур
    if mouse_click and start_pos:
        mx, my = pygame.mouse.get_pos()
        my_adj = my - toolbar_height

        dx = abs(mx - start_pos[0])
        dy = abs(my_adj - start_pos[1])

        if painting_mode == "rectangle":
            pygame.draw.rect(screen, current_color,
                             (min(start_pos[0], mx), toolbar_height + min(start_pos[1], my_adj), dx, dy), scale)
        elif painting_mode == "circle":
            radius = max(dx, dy) // 2
            center = (min(start_pos[0], mx) + dx // 2, toolbar_height + min(start_pos[1], my_adj) + dy // 2)
            pygame.draw.circle(screen, current_color, center, radius, scale)
        elif painting_mode == "square":
            size = min(dx, dy)
            pygame.draw.rect(screen, current_color,
                             (min(start_pos[0], mx), toolbar_height + min(start_pos[1], my_adj), size, size), scale)
        elif painting_mode == "right_triangle":
            points = [(start_pos[0], toolbar_height + start_pos[1]),
                      (start_pos[0], my), (mx, my)]
            pygame.draw.polygon(screen, current_color, points, scale)
        elif painting_mode == "equilateral_triangle":
            side = max(dx, dy)
            h = (math.sqrt(3) / 2) * side
            x1, y1 = start_pos
            x2, y2 = x1 + side, y1
            x3, y3 = x1 + side / 2, y1 - h
            pygame.draw.polygon(screen, current_color,
                                [(x1, y1 + toolbar_height), (x2, y2 + toolbar_height), (x3, y3 + toolbar_height)], scale)
        elif painting_mode == "rhombus":
            cx = (start_pos[0] + mx) // 2
            cy = (start_pos[1] + my_adj) // 2
            points = [(cx, toolbar_height + start_pos[1]), (mx, toolbar_height + cy),
                      (cx, toolbar_height + my_adj), (start_pos[0], toolbar_height + cy)]
            pygame.draw.polygon(screen, current_color, points, scale)

# Главный цикл
while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
