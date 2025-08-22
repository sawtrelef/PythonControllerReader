import pygame
from PS5Controller import PlayStation5Controller

pygame.init()

font = pygame.font.Font('Zou.ttf', 32)
background = pygame.image.load("Background.png")
rect = background.get_rect()
x = int(rect.bottomright[0])
y = int(rect.bottomright[1])
pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((x,y))
clock = pygame.time.Clock()
#font = pygame.font.Font('c:/Windows/Fonts/Arial.ttf', 24)



class APMCounter():
    value = 0
    timepassed = 0
    actionperminute = 0
    def __init__(self,target):
        self.ValueTarget = target

    def update(self):
        self.value = self.ValueTarget.getcount()
        self.timepassed = self.timepassed + 1
        self.actionperminute = int(self.value / (self.timepassed / 3600))

    def draw(self, WINDOW):
        text = font.render('APM : ' + str(self.actionperminute), True, (149, 75, 220))
        WINDOW.blit(text, (int(x/2)-45, y-35))


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
    clock.tick(60)

pygame.quit()
quit()