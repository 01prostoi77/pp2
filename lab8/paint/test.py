import pygame

pygame.init()

# Screen and canvas sizes
width = 1000
height = 680
sidebar_height = 100  # Интерфейс теперь сверху

screen = pygame.display.set_mode((width, height))
canva = pygame.Surface((width, height - sidebar_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)
light_grey = (150, 150, 150)

# Constants
running = True
mouse_click = False
last_mouse_pos = None
painting_mode = 'line'
scale = 2  # Brush size
current_color = black  # Default brush color
start_pos = None

# Font
font = pygame.font.SysFont("Leelawadee", 20)
font_small = pygame.font.SysFont("Leelawadee", 15)
# Tool buttons
buttons = {
    "line":         pygame.Rect(20, 10, 80, 20),
    "rectangle":    pygame.Rect(110, 10, 80, 20),
    "circle":       pygame.Rect(200, 10, 80, 20),
    "eraser":       pygame.Rect(290, 10, 80, 20),
    "+":            pygame.Rect(380, 10, 30, 20),
    "-":            pygame.Rect(420, 10, 30, 20),
    "clear":        pygame.Rect(460, 10, 80, 20),
}

button_states = {mode: False for mode in buttons}  # The status of button(click or not)
# Color selection buttons
color_buttons = {
    black: pygame.Rect(820, 10, 30, 30),
    blue: pygame.Rect(860, 10, 30, 30),
    red: pygame.Rect(900, 10, 30, 30),
    yellow: pygame.Rect(940, 10, 30, 30),
}

screen.fill(black)
canva.fill(white)

def draw_buttons():
    for mode, rect in buttons.items():
        color = (233, 233, 233) if button_states[mode] else (light_grey if painting_mode == mode else grey)
        pygame.draw.rect(screen, color, rect)
        text = font_small.render(mode.capitalize(), True, white)
        screen.blit(text, (rect.x + 5, rect.y))

    scale_text = font.render(f"Size: {scale}", True, white)
    screen.blit(scale_text, (560, 10))

    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, white, rect, 3)  # Highlight active color

def handle_events():
    global running, mouse_click, last_mouse_pos, painting_mode, scale, current_color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            mx, my = pygame.mouse.get_pos()

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
                if rect.collidepoint(event.pos):
                    button_states[mode] = True  # Button is clicked

            for color, rect in color_buttons.items():
                if rect.collidepoint(mx, my):
                    current_color = color

            if my >= sidebar_height:
                global start_pos
                start_pos = (mx, my - sidebar_height)  # Handle the start position

        if event.type == pygame.MOUSEBUTTONUP:
            for mode, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    button_states[mode] = False  # Button is released

            mouse_click = False
            last_mouse_pos = None
            if start_pos is not None:
                mx, my = pygame.mouse.get_pos()
                my -= sidebar_height

                width = abs(mx - start_pos[0])
                height = abs(my - start_pos[1])

                if painting_mode == "rectangle":
                    pygame.draw.rect(canva, current_color,
                                     (min(start_pos[0], mx), min(start_pos[1], my), width, height), scale)

                elif painting_mode == "circle":
                    radius = max(width, height) // 2
                    center = (min(start_pos[0], mx) + width // 2, min(start_pos[1], my) + height // 2)
                    pygame.draw.circle(canva, current_color, center, radius, scale)

            start_pos = None

def update():
    global last_mouse_pos

    mx, my = pygame.mouse.get_pos()
    my -= sidebar_height

    if mouse_click and last_mouse_pos is not None and my >= 0:
        if painting_mode == 'line':
            pygame.draw.line(canva, current_color, last_mouse_pos, (mx, my), scale)
        elif painting_mode == 'eraser':
            pygame.draw.line(canva, white, last_mouse_pos, (mx, my), scale)

    if mouse_click and my >= 0:
        last_mouse_pos = (mx, my)

def render():
    screen.fill(black)
    pygame.draw.rect(screen, grey, (0, 0, width, sidebar_height))  # Draw top bar
    screen.blit(canva, (0, sidebar_height))  # Display the canvas
    draw_buttons()

    if mouse_click and start_pos:
        mx, my = pygame.mouse.get_pos()
        my -= sidebar_height

        width_l = abs(mx - start_pos[0])
        height_l = abs(my - start_pos[1])

        if painting_mode == "rectangle":
            pygame.draw.rect(screen, current_color,
                             (min(start_pos[0], mx),
                              sidebar_height + min(start_pos[1], my), width_l, height_l), scale)

        elif painting_mode == "circle":
            radius = max(width_l, height_l) // 2
            center = (min(start_pos[0], mx) + width_l // 2,
                      sidebar_height + min(start_pos[1], my) + height_l // 2)
            pygame.draw.circle(screen, current_color, center, radius, scale)

while running:
    handle_events()
    update()
    render()
    pygame.display.flip()

pygame.quit()
