import pygame
import pygame.gfxdraw
import time
from math import pi, cos, sin

"""
Still need to add numbers around the speedometer, and implement it into the main code
The code is pretty rough due to needing to make the drawing arc function from scratch as the one in the library
is super buggy and full of artifacts
"""


# Display Library Setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(128, 227, 255)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()  # Used for FPS control
running = True
# pygame.display.toggle_fullscreen()
font = pygame.freetype.SysFont('Arial', 150)


def drawTextCentered(surface, text, text_size, color):
    text_rect = font.get_rect(text, size=200)
    text_rect.center = surface.get_rect().center
    font.render_to(surface, text_rect, text, color, size=200)


def convert_origin(x, y):
    x += 400
    y += 250
    return (x, y)


def drawArc(surface, x, y, radius, width, start_deg, end_deg, color):
    offset = 50
    pygame.gfxdraw.aacircle(surface, int(x+400), int(y+250), radius, color)
    pygame.gfxdraw.filled_circle(surface, int(x+400), int(y+250), radius, color)
    pygame.gfxdraw.filled_circle(surface, int(x+400), int(y+250), radius-width, BG_COLOR)
    pygame.gfxdraw.aacircle(surface, int(x+400), int(y+250), radius-width, color)
    eX1 = int(x + (radius-width) * cos(end_deg * pi/180))
    eY1 = int(y + (radius-width) * sin(end_deg * pi/180))
    eX2 = int((radius+offset)*cos(end_deg * pi/180))
    eY2 = int((radius+offset)*sin(end_deg * pi/180))
    sX2 = int((radius+offset)*cos(start_deg * pi/180))
    sY2 = int((radius+offset)*sin(start_deg * pi/180))

    innerEnd = (int((radius-width-(offset/2))*cos(end_deg * pi/180)),
                int((radius-width-(offset/2))*sin(end_deg * pi/180)))
    innerStart = (int((radius-width-(offset/2))*cos(start_deg * pi/180)),
                  int((radius-width-(offset/2))*sin(start_deg * pi/180)))

    coords = []
    angles = [2, -47, -92, -132, -182, -227, -272, -317, start_deg, end_deg]
    angles.sort()

    for i in angles:
        if i < end_deg or i > start_deg:
            coords.append(convert_origin(int((radius+offset)*cos(i * pi/180)),
                          int((radius+offset)*sin(i * pi/180))))
        if i == start_deg:
            coords.append(convert_origin(innerStart[0], innerStart[1]))
            coords.append(convert_origin(sX2, sY2))

        if i == end_deg:
            coords.append(convert_origin(eX2, eY2))
            coords.append(convert_origin(eX1, eY1))
            coords.append(convert_origin(innerEnd[0], innerEnd[1]))

    pygame.gfxdraw.filled_polygon(screen, coords, BG_COLOR)


def drawSpeed(surface, radius, width, angle, color):
    thickness = 1.5
    eX = int((radius) * cos((angle-thickness) * pi/180))
    eY = int((radius) * sin((angle-thickness) * pi/180))
    eX1 = int((radius-width) * cos((angle-thickness) * pi/180))
    eY1 = int((radius-width) * sin((angle-thickness) * pi/180))
    sX = int((radius) * cos((angle+thickness) * pi/180))
    sY = int((radius) * sin((angle+thickness) * pi/180))
    sX1 = int((radius-width) * cos((angle+thickness) * pi/180))
    sY1 = int((radius-width) * sin((angle+thickness) * pi/180))
    pygame.gfxdraw.filled_polygon(surface, [convert_origin(eX, eY), convert_origin(
        eX1, eY1),  convert_origin(sX1, sY1), convert_origin(sX, sY)], color)


def speedToAngle(speed):
    return -225 + (speed*4.5)


while running:

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    drawArc(screen, 0, 0, 200, 25, 45, -225, (0, 0, 0))  # bg arc
    # Still need to add numbers around the arc

    drawSpeed(screen, 200, 25, speedToAngle(25), (255, 0, 0))  # example going 25 mph

    drawTextCentered(screen, str("25"), 100, (0, 0, 0))
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
