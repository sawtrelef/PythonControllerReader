from pygame import joystick, image, transform
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'
joystick.init()
joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]

class Button():
    offimagename = "./buttons/unpressed.png"
    onimagename = "./buttons/pressed.png"
    off = image.load(offimagename)
    on = image.load(onimagename)
    rotate = 0
    def __init__(self, buttonnum, x, y):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off


    def UpdateSelf(self, ID):
        if len(joysticks) > 0:
            self.state = joysticks[ID].get_button(self.buttonnum)
        else:
            self.state = 0
        if self.state == 0:
            self.image = self.off
            return False
        else:
            if self.image != self.on:
                self.image = self.on
                return True
            return False

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x, self.y))
    def load(self):
        self.off = image.load(self.offimagename)
        self.on = image.load(self.onimagename)
        self.on = transform.rotate(self.on, self.rotate)
        self.off = transform.rotate(self.off, self.rotate)
        self.rect = self.off.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class TriggerAxis():
    barimage = "./Axis/triggerbar.png"
    paddleimage = "./Axis/paddlebar.png"
    bar = image.load(barimage)
    paddle = image.load(paddleimage)
    horizontal = False
    def __init__(self, axis, x, y):
            self.x = x
            self.y = y
            self.ymod = -1
            self.axis = axis
            self.axisstate = 0

    def UpdateSelf(self, ID):
        if len(joysticks) > 0:
            self.axisstate = joysticks[ID].get_axis(self.axis)
        else:
            self.axisstate = 0
        self.ymod = abs(-1 - self.axisstate)/2

    def draw(self, WINDOW):
        if self.horizontal:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x + (100 * self.ymod), self.y - 4))
        else:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x - 4, (self.y + (100 * self.ymod))))


    def flip(self):
        self.bar = transform.rotate(self.bar,90)
        self.paddle = transform.rotate(self.paddle, 90)


    def load(self):
        self.bar = image.load(self.barimage)
        self.paddle = image.load(self.paddleimage)


class Stick():
    pressed = "./sticks/stickpressed.png"
    unpressed = "./sticks/stickunpressed.png"
    stickunpressed = image.load(unpressed)
    stickpressed = image.load(pressed)

    def __init__(self, vertaxis, horaxis, x, y, buttonnum = -1):
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
        self.state = False
    def UpdateSelf(self, ID):
        if(self.buttonnum > 0):
            if len(joysticks) > 0:
                self.state = joysticks[ID].get_button(self.buttonnum)
            else:
                self.state = 0
        else:
            self.state == 0
        action = False
        if self.state == 0:
            self.image = self.stickunpressed
            action =  False
        else:
            if self.image != self.stickpressed:
                self.image = self.stickpressed
                action = True
            else:
                action = False
        if len(joysticks) > 0:
            self.vertstate = joysticks[ID].get_axis(self.vertaxis)
        else:
            self.vertstate = 0
        self.vertmod = 13*self.vertstate
        if len(joysticks) > 0:
            self.horstate = joysticks[ID].get_axis(self.horaxis)
        else:
            self.horstate = 0
        self.hormod = 13*self.horstate
        return action

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x+self.hormod, self.y+self.vertmod))

    def load(self):
        self.stickpressed = image.load(self.pressed)
        self.stickunpressed = image.load(self.unpressed)