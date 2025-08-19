import pygame
import os
from PS5Controller import PlayStation5Controller


pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

font = pygame.font.Font('Zou.ttf', 32)

pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((400,250))
clock = pygame.time.Clock()
#font = pygame.font.Font('c:/Windows/Fonts/Arial.ttf', 24)
background = pygame.image.load("Background.png")


class APMCounter():
    value = 0
    timepassed = 0
    actionperminute = 0
    def __init__(self,target):
        self.ValueTarget = target

    def update(self):
        self.value = self.ValueTarget.getcount()
        self.timepassed = self.timepassed + 1
        self.actionperminute = int(self.value / (self.timepassed / 1800))

    def draw(self, WINDOW):
        text = font.render('APM : ' + str(self.actionperminute), True, (149, 75, 220))
        WINDOW.blit(text, (155, 215))


controller = PlayStation5Controller(0)
counter = APMCounter(controller)
done = False
while not done:

    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            done = True
    if done:
        break

    controller.update()
    counter.update()
    display.blit(background, (0,0))
    controller.draw(display)
    counter.draw(display)


    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()