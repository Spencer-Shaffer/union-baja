import pygame
import RPi.GPIO as gpio
from wheel import *
from datetime import datetime
import serial

# GPIO Setup -- might not need
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)


# Serial Setup
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyS0'
ser.open()


def transmit(msg):
    msg = msg
    length = len(msg)
    ser.write(f'AT+SEND=0,{length},{msg}\r\n'.encode())


# Display Library Setup
pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()  # Used for FPS control
running = True
# pygame.display.toggle_fullscreen()
font = pygame.freetype.SysFont('Arial', 150)

# Display Library Helper Function


def drawTextCentered(surface, text, text_size, color):
    text_rect = font.get_rect(text, size=200)
    text_rect.center = surface.get_rect().center
    font.render_to(surface, text_rect, text, color, size=200)


# Declare Class Instances
# leftWheel = Wheel(23)
# rightWheel = Wheel(3)
# rearLeftWheel = Wheel(None)  # !!
# rearRightWheel = Wheel(None)  # !!

lastTransmit = datetime.now()

# placeholder vars for testing warning lights
cvTemp = 75
portalTemp = 75
# Warning lights timing
warningTimeClockStart = datetime.now()
warningTempDrawn = False
warningBlinkRate = 0.25


# Main Loop
while running:

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check each wheel to see if it has triggered
#    leftWheel.checkStatus()
#    rightWheel.checkStatus()
#    rearLeftWheel.checkStatus()
#    rearRightWheel.checkStatus()

    # Draw to screen
    screen.fill("lightblue")

    # hypothetical temperature warning code, blink every second
    if cvTemp > 70:
        if datetime.now().second % 2 == 0:
            pygame.draw.circle(screen, (255, 165, 0), (700, 425), 35)
        else:
            pass

    # more customizable code for warning lights, can change blink rate
    if portalTemp >= 70:
        if not warningTempDrawn:
            warningTimeClockStart = datetime.now()

        difference = (datetime.now() - warningTimeClockStart).total_seconds()

        if difference <= warningBlinkRate:
            pygame.draw.circle(screen, (255, 0, 0), (620, 425), 35)
            if not warningTempDrawn:
                warningTimeClock = datetime.now()
                warningTempDrawn = True
        elif difference >= warningBlinkRate*2:
            warningTempDrawn = False

    drawTextCentered(screen, str("10"), 100, (0, 0, 0))
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

    # Transmit Data -- only do it every 5 seconds or so (measure amount of time sense last sent)
    currentTime = datetime.now()
    delta = currentTime - lastTransmit
    if delta.total_seconds() >= 5.0:
        # transmit("Sending message")
        lastTransmit = datetime.now()

pygame.quit()
