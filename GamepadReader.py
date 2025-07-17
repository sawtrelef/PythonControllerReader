import pygame
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((400,250))
clock = pygame.time.Clock()
font = pygame.font.Font('c:/Windows/Fonts/Arial.ttf', 24)
background = pygame.image.load("Background.png")
stick1 = joysticks[0]
buttons = stick1.get_numbuttons()
axis = stick1.get_numaxes()

class FaceButton():
    off = pygame.image.load("unpressed.png")
    on = pygame.image.load("pressed.png")
    def __init__(self, buttonnum, x, y):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off
    def UpdateSelf(self, ID):
        self.state = joysticks[ID].get_button(self.buttonnum)
        if self.state == 0 :
            self.image = self.off
        else:
            self.image = self.on

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x, self.y))

xbutton = FaceButton(0,302,111)
obutton = FaceButton(1, 322, 91)
sqbutton = FaceButton(2, 282, 91)
tbutton = FaceButton(3, 302, 71)

class DPadButton():
    off = pygame.image.load("arrowunpressed.png")
    on = pygame.image.load("arrowpressed.png")

    def __init__(self, buttonnum, x, y):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off

    def UpdateSelf(self, ID):
        self.state = joysticks[ID].get_button(self.buttonnum)
        if self.state == 0:
            self.image = self.off
        else:
            self.image = self.on

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x, self.y))
upbutton = DPadButton(11,81, 71)
downbutton = DPadButton(12,81, 111)
downbutton.off = pygame.transform.rotate(downbutton.off,180)
downbutton.on = pygame.transform.rotate(downbutton.on,180)
leftbutton = DPadButton(13,61, 91)
leftbutton.off = pygame.transform.rotate(downbutton.off,270)
leftbutton.on = pygame.transform.rotate(downbutton.on,270)
rightbutton = DPadButton(14,101, 91)
rightbutton.off = pygame.transform.rotate(downbutton.off,90)
rightbutton.on = pygame.transform.rotate(downbutton.on,90)

class BumperButton():
    off = pygame.image.load("bumperunpressed.png")
    on = pygame.image.load("bumperpressed.png")

    def __init__(self, buttonnum, x, y):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off

    def UpdateSelf(self, ID):
        self.state = joysticks[ID].get_button(self.buttonnum)
        if self.state == 0:
            self.image = self.off
        else:
            self.image = self.on

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x, self.y))

lbump = BumperButton(9,60, 5)
rbump = BumperButton(10,243, 5)
mbump = BumperButton(15, 153, 71)

class ExtraButton():
    off = pygame.image.load("unpressedoption.png")
    on = pygame.image.load("pressedoption.png")
    def __init__(self, buttonnum, x, y):
            self.x = x
            self.y = y
            self.buttonnum = buttonnum
            self.state = 0
            self.image = self.off

    def UpdateSelf(self, ID):
            self.state = joysticks[ID].get_button(self.buttonnum)
            if self.state == 0:
                self.image = self.off
            else:
                self.image = self.on

    def draw(self, WINDOW):
            WINDOW.blit(self.image, (self.x, self.y))

sharebutton = ExtraButton(4, 131, 71)
pausebutton = ExtraButton(6, 256, 71)
micbutton = ExtraButton(16, 195, 141)
micbutton.off = pygame.transform.rotate(micbutton.off,90)
micbutton.on = pygame.transform.rotate(micbutton.on, 90)
psbutton = ExtraButton(5, 195, 122)
psbutton.on = pygame.image.load("playstationpressed.png")
psbutton.off = pygame.image.load("playstationunpressed.png")

class TriggerAxis():
    bar = pygame.image.load("triggerbar.png")
    paddle = pygame.image.load("paddlebar.png")
    def __init__(self, axis, x, y):
            self.x = x
            self.y = y
            self.ymod = -1
            self.axis = axis
            self.axisstate = 0

    def UpdateSelf(self, ID):
            self.axisstate = joysticks[ID].get_axis(self.axis)
            self.ymod = abs(-1 - self.axisstate)/2

    def draw(self, WINDOW):
        WINDOW.blit(self.bar,(self.x,self.y))
        WINDOW.blit(self.paddle,(self.x-4,(self.y +(100 *self.ymod))))

l2Trigger = TriggerAxis(4, 18, 5)
r2Trigger = TriggerAxis(5, 378, 5)


class Stick():
    stickunpressed = pygame.image.load("stickunpressed.png")
    stickpressed = pygame.image.load("stickpressed.png")

    def __init__(self, vertaxis, horaxis, buttonnum, x, y):
        self.x = x
        self.y = y
        self.vertaxis = vertaxis
        self.vertstate = 0
        self.vertmod = 0
        self.horaxis = horaxis
        self.horstate = 0
        self.hormod = 0
        self.buttonnum = buttonnum
        self.image = self.stickunpressed
    def UpdateSelf(self, ID):
        if joysticks[ID].get_button(self.buttonnum) == 1:
            self.image = self.stickpressed
        else:
            self.image = self.stickunpressed
        self.vertstate = joysticks[ID].get_axis(self.vertaxis)
        self.vertmod = 13*self.vertstate
        self.horstate = joysticks[ID].get_axis(self.horaxis)
        self.hormod = 13*self.horstate

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x+self.hormod, self.y+self.vertmod))

lstick = Stick(1,0,7,147, 185)
rstick = Stick(3,2, 8, 249, 185)


class PlayStation5Controller():
    buttonlist = [xbutton,obutton,sqbutton,tbutton,upbutton,downbutton,leftbutton,rightbutton,lbump,rbump,mbump,sharebutton,pausebutton,micbutton,sharebutton,psbutton]
    axislist = [l2Trigger, r2Trigger, lstick, rstick]
    def __init__(self, ID):
        self.ID = ID
    def update(self):
        for item in self.buttonlist:
            item.UpdateSelf(self.ID)
        for item in self.axislist:
            item.UpdateSelf(self.ID)
    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        for item in self.axislist:
            item.draw(WINDOW)
        
controller = PlayStation5Controller(stick1.get_id())
done = False
while not done:

    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            done = True
    if done:
        break

    controller.update()
    display.blit(background, (0,0))
    controller.draw(display)


    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()