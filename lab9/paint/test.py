import pygame
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана и рабочей области (canvas)
width = 1000
height = 480
sidebar_width = 150

screen = pygame.display.set_mode((width, height))
canva = pygame.Surface((width - sidebar_width, height))

# Определение основных цветов
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)
light_grey = (150, 150, 150)

# Константы и переменные
running = True               # Флаг работы цикла программы
mouse_click = False          # Флаг зажатой кнопки мыши
last_mouse_pos = None        # Последняя позиция мыши для рисования линий
painting_mode = 'line'       # Режим рисования (инструмент)
scale = 2                    # Размер кисти (толщина линий)
current_color = black        # Текущий цвет кисти
start_pos = None             # Начальная точка для рисования фигур

# Инициализация шрифтов
font = pygame.font.SysFont("Leelawadee", 20)
font_small = pygame.font.SysFont("Leelawadee", 15)

# Определение кнопок для инструментов
buttons = {
    "line":                   pygame.Rect(10, 20, 130, 20),
    "rectangle":              pygame.Rect(10, 45, 130, 20),
    "circle":                 pygame.Rect(10, 70, 130, 20),
    "eraser":                 pygame.Rect(10, 95, 130, 20),
    "+":                      pygame.Rect(50, 115, 30, 20),
    "-":                      pygame.Rect(10, 115, 30, 20),
    "clear":                  pygame.Rect(10, 165, 130, 20),
    "square":                 pygame.Rect(10, 190, 130, 20),
    "right_triangle":         pygame.Rect(10, 215, 130, 20),
    "equilateral_triangle":   pygame.Rect(10, 240, 130, 20),
    "rhombus":                pygame.Rect(10, 265, 130, 20),
}

# Словарь состояний кнопок (нажата или нет)
button_states = {mode: False for mode in buttons}

# Кнопки для выбора цвета
color_buttons = {
    black: pygame.Rect(10, 390, 30, 30),
    blue: pygame.Rect(50, 390, 30, 30),
    red: pygame.Rect(10, 440, 30, 30),
    yellow: pygame.Rect(50, 440, 30, 30),
}

# Заполнение экрана и холста базовыми цветами
screen.fill(black)
canva.fill(white)

def draw_buttons():
    """Отрисовка кнопок инструментов и выбора цвета."""
    for mode, rect in buttons.items():
        color = (233, 233, 233) if button_states[mode] else (light_grey if painting_mode == mode else grey)
        pygame.draw.rect(screen, color, rect)
        text = font_small.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 20, rect.y))
    
    # Отображение текущего размера кисти
    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (10, 325))
    
    # Отрисовка кнопок выбора цвета и подсветка активного цвета
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)

def handle_events():
    """Обработка событий ввода (мышь, клавиши и т.д.)."""
    global running, mouse_click, last_mouse_pos, painting_mode, scale, current_color, start_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            mx, my = pygame.mouse.get_pos()

            # Обработка нажатий на кнопки инструментов
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

            # Обработка выбора цвета
            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

            # Фиксируем начальную точку, если клик в области холста
            if mx >= sidebar_width:
                start_pos = (mx - sidebar_width, my)

        if event.type == pygame.MOUSEBUTTONUP:
            for mode, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    button_states[mode] = False

            mouse_click = False
            last_mouse_pos = None

            # Рисуем фигуру на холсте по выбранному режиму
            if start_pos is not None:
                mx, my = pygame.mouse.get_pos()
                mx -= sidebar_width

                width_diff = abs(mx - start_pos[0])
                height_diff = abs(my - start_pos[1])

                if painting_mode == "rectangle":
                    pygame.draw.rect(canva, current_color,
                                     (min(start_pos[0], mx), min(start_pos[1], my), width_diff, height_diff), scale)
                elif painting_mode == "circle":
                    radius = max(width_diff, height_diff) // 2
                    center = (min(start_pos[0], mx) + width_diff // 2, min(start_pos[1], my) + height_diff // 2)
                    pygame.draw.circle(canva, current_color, center, radius, scale)
                elif painting_mode == "square":
                    # Используем минимальное различие для равных сторон квадрата
                    size = min(width_diff, height_diff)
                    pygame.draw.rect(canva, current_color,
                                     (min(start_pos[0], mx), min(start_pos[1], my), size, size), scale)
                elif painting_mode == "right_triangle":
                    # Точки: начальная, вертикально вниз и горизонтально вправо
                    points = [start_pos, (start_pos[0], my), (mx, my)]
                    pygame.draw.polygon(canva, current_color, points, scale)
                elif painting_mode == "equilateral_triangle":
                    # Длина стороны определяется максимальным из разностей
                    side = max(width_diff, height_diff)
                    # Высота равностороннего треугольника: h = (sqrt(3)/2) * side
                    height_t = (math.sqrt(3) / 2) * side
                    x1, y1 = start_pos
                    x2, y2 = x1 + side, y1
                    x3, y3 = x1 + side / 2, y1 - height_t
                    pygame.draw.polygon(canva, current_color, [(x1, y1), (x2, y2), (x3, y3)], scale)
                elif painting_mode == "rhombus":
                    # Вычисляем центр выделенной области и строим ромб через вершины
                    center_x = (start_pos[0] + mx) // 2
                    center_y = (start_pos[1] + my) // 2
                    points = [(center_x, start_pos[1]), (mx, center_y),
                              (center_x, my), (start_pos[0], center_y)]
                    pygame.draw.polygon(canva, current_color, points, scale)

            start_pos = None

def update():
    """Обновление состояния рисования (например, отрисовка линий в режиме 'line' и 'eraser')."""
    global last_mouse_pos

    mx, my = pygame.mouse.get_pos()
    mx_adjusted = mx - sidebar_width

    if mouse_click and last_mouse_pos is not None and mx_adjusted >= 0:
        if painting_mode == 'line':
            pygame.draw.line(canva, current_color, last_mouse_pos, (mx_adjusted, my), scale)
        elif painting_mode == 'eraser':
            pygame.draw.line(canva, white, last_mouse_pos, (mx_adjusted, my), scale)

    if mouse_click and mx_adjusted >= 0:
        last_mouse_pos = (mx_adjusted, my)

def render():
    """Отрисовка экрана: холст, панель инструментов и предварительный просмотр фигур."""
    screen.fill(black)
    pygame.draw.rect(screen, grey, (0, 0, sidebar_width, height))
    screen.blit(canva, (sidebar_width, 0))
    draw_buttons()

    # Предварительный просмотр фигур до отпускания мыши
    if mouse_click and start_pos:
        mx, my = pygame.mouse.get_pos()
        mx_adjusted = mx - sidebar_width

        width_l = abs(mx_adjusted - start_pos[0])
        height_l = abs(my - start_pos[1])

        if painting_mode == "rectangle":
            pygame.draw.rect(screen, current_color,
                             (sidebar_width + min(start_pos[0], mx_adjusted),
                              min(start_pos[1], my), width_l, height_l), scale)
        elif painting_mode == "circle":
            radius = max(width_l, height_l) // 2
            center = (sidebar_width + min(start_pos[0], mx_adjusted) + width_l // 2,
                      min(start_pos[1], my) + height_l // 2)
            pygame.draw.circle(screen, current_color, center, radius, scale)
        elif painting_mode == "square":
            size = min(width_l, height_l)
            pygame.draw.rect(screen, current_color,
                             (sidebar_width + min(start_pos[0], mx_adjusted),
                              min(start_pos[1], my), size, size), scale)
        elif painting_mode == "right_triangle":
            points = [(sidebar_width + start_pos[0], start_pos[1]),
                      (sidebar_width + start_pos[0], my),
                      (sidebar_width + mx_adjusted, my)]
            pygame.draw.polygon(screen, current_color, points, scale)
        elif painting_mode == "equilateral_triangle":
            side = max(width_l, height_l)
            height_t = (math.sqrt(3) / 2) * side
            x1, y1 = start_pos
            x2, y2 = x1 + side, y1
            x3, y3 = x1 + side / 2, y1 - height_t
            pygame.draw.polygon(screen, current_color,
                                [(sidebar_width + x1, y1), (sidebar_width + x2, y2), (sidebar_width + x3, y3)], scale)
        elif painting_mode == "rhombus":
            center_x = (sidebar_width + start_pos[0] + mx_adjusted) // 2
            center_y = (start_pos[1] + my) // 2
            points = [(center_x, start_pos[1]), (sidebar_width + mx_adjusted, center_y),
                      (center_x, my), (sidebar_width + start_pos[0], center_y)]
            pygame.draw.polygon(screen, current_color, points, scale)

# Основной цикл программы
while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
