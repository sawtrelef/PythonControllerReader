from pygame import joystick, image
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'
joystick.init()
joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]

class Button():
    off = image.load("unpressed.png")
    on = image.load("pressed.png")
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
            return False
        else:
            if self.image != self.on:
                self.image = self.on
                return True
            return False

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x, self.y))

class TriggerAxis():
    bar = image.load("triggerbar.png")
    paddle = image.load("paddlebar.png")
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

class Stick():
    stickunpressed = image.load("stickunpressed.png")
    stickpressed = image.load("stickpressed.png")

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
        self.state = False
    def UpdateSelf(self, ID):
        self.state = joysticks[ID].get_button(self.buttonnum)
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
        self.vertstate = joysticks[ID].get_axis(self.vertaxis)
        self.vertmod = 13*self.vertstate
        self.horstate = joysticks[ID].get_axis(self.horaxis)
        self.hormod = 13*self.horstate
        return action

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.x+self.hormod, self.y+self.vertmod))