import pygame.image
from pygame import joystick, image, transform
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'
joystick.init()
joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]

class Button():
    unpressed = "./buttons/unpressed.png"
    pressed = "./buttons/pressed.png"
    off = image.load(unpressed)
    on = image.load(pressed)
    rotate = 0
    def __init__(self, buttonnum=-1, x=-1, y=-1):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off


    def UpdateSelf(self, ID):
        if len(joysticks) > 0:
            length = joysticks[ID].get_numbuttons()
            if self.buttonnum < length and self.buttonnum >= 0:
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
        self.off = image.load(self.unpressed)
        self.on = image.load(self.pressed)
        self.on = transform.rotate(self.on, self.rotate)
        self.off = transform.rotate(self.off, self.rotate)
    def Rotate(self):
        if self.rotate < 270:
            self.rotate = self.rotate+90
        else:
            self.rotate = 0
        self.load()

class TriggerAxis():
    barimage = "./Axis/triggerbar.png"
    paddleimage = "./Axis/paddlebar.png"
    bar = image.load(barimage)
    paddle = image.load(paddleimage)
    horizontal = False
    def __init__(self, x =-1, y = -1, axis = -1):
            self.x = x
            self.y = y
            self.ymod = -1
            self.axis = axis
            self.axisstate = 0

    def UpdateSelf(self, ID):
        if len(joysticks) > 0:
            length = joysticks[ID].get_numaxes()
            if self.axis < length:
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

    def load(self):
        self.bar = image.load(self.barimage)
        self.paddle = image.load(self.paddleimage)
        if self.horizontal:
            self.bar = transform.rotate(self.bar, 90)
            self.paddle = transform.rotate(self.paddle,90)

    def Rotate(self):
       self.horizontal = not self.horizontal
       self.load()

class Stick():
    pressed = "./sticks/stickpressed.png"
    unpressed = "./sticks/stickunpressed.png"
    stickunpressed = image.load(unpressed)
    stickpressed = image.load(pressed)
    rotate = 0

    def __init__(self, x, y, vertaxis = -1, horaxis = -1, buttonnum = -1):
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
        if(self.buttonnum >= 0):
            if len(joysticks) > 0:
                length = joysticks[ID].get_numbuttons()
                if self.buttonnum < length:
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
            length = joysticks[ID].get_numaxes()
            if self.vertaxis < length and self.vertaxis >= 0:
                self.vertstate = joysticks[ID].get_axis(self.vertaxis)
            else:
                self.vertstate = 0
            self.vertmod = 13*self.vertstate

            if self.horaxis < length and self.horaxis >= 0:
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
        self.stickpressed = transform.rotate(self.stickpressed, self.rotate)
        self.stickunpressed = transform.rotate(self.stickunpressed, self.rotate)

    def Rotate(self):
        if self.rotate < 270:
            self.rotate = self.rotate+90
        else:
            self.rotate = 0
        self.load()

    def changehorizontalaxis(self, newaxisnum):
        self.horaxis = newaxisnum

    def changeverticalaxis(self, newaxisnum):
        self.vertaxis = newaxisnum

    def changebutton(self, newbuttonnum):
        self.buttonnum = newbuttonnum

class Hat():
    background = 'assets/hatbackground.png'
    pressed = 'buttons/arrowpressed.png'
    unpressed = 'buttons/unpressed.png'
    rotate = 0
    rotatemod = 0
    backgroundimage = image.load(background)
    pressedimage = image.load(pressed)
    unpressedimage= image.load(unpressed)
    stateimage = unpressedimage

    def __init__(self, hatnum = -1, x = -1, y = -1):
        self.hatnumber = hatnum
        # x and y will be the top left coordinate for the background
        self.x = x
        self.y = y
        self.backgroundrect = self.backgroundimage.get_rect()
        self.staterect = self.stateimage.get_rect()
        self.state = (0,0)

    def UpdateSelf(self,ID):
        action = False
        if (self.hatnumber >= 0):
            if len(joysticks) > 0:
                length = joysticks[ID].get_numbuttons()
                if self.hatnumber < length and self.hatnumber > -1:
                    if self.state != joysticks[ID].get_hat(self.hatnumber) and self.state != (0,0):
                        action = True
                    self.state = joysticks[ID].get_hat(self.hatnumber)
                else:
                    self.state = (0,0)
        else:
            self.state == (0,0)

        self.updateImage()
        return action

    def updateImage(self):

        self.imagex = self.state[0] * self.staterect[2] + self.backgroundrect[2]/2 - self.staterect[3]/2 + self.x+1
        self.imagey = -self.state[1] * self.staterect[3] - self.staterect[3]/2 + self.backgroundrect[3]/2 + self.y
        self.rotatemod = 0
        if self.state == (0, 0):
            self.stateimage = self.unpressedimage
        else:
            self.stateimage = self.pressedimage
            if self.state[0] != 0:
                self.rotatemod = self.rotatemod - (90*self.state[0])
            if self.state[1] != 0:
                if self.rotatemod !=0:
                    self.rotatemod = self.rotatemod - (45*self.state[1]*-self.state[0])
                elif self.state[1] == -1:
                    self.rotatemod = 180


        self.stateimage = transform.rotate(self.stateimage, self.rotate+self.rotatemod)

    def draw(self,WINDOW):
        WINDOW.blit(self.backgroundimage, (self.x, self.y))
        WINDOW.blit(self.stateimage, (self.imagex, self.imagey))

    def load(self):
        self.backgroundimage = transform.rotate(image.load(self.background), self.rotate)
        self.updateImage()

