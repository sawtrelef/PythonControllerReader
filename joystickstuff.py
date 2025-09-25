import pygame.image
from pygame import image, transform
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'

class Button():
    unpressed = "./buttons/unpressed.png"
    pressed = "./buttons/pressed.png"
    off = image.load(unpressed)
    on = image.load(pressed)
    rotate = 0
    def __init__(self, buttonnum=-1, x=-1, y=-1, controller=False):
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off
        self.controller = controller


    def UpdateSelf(self):
        if self.controller.gamepad:
            if len(self.controller.buttondict) > 0:
                if self.buttonnum in self.controller.buttondict:
                    safetylength = self.controller.gamepad.get_numbuttons()
                    if self.buttonnum < safetylength:
                        self.state = self.controller.gamepad.get_button(self.buttonnum)
            else:
                self.state = 0
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
    pressed = "./Axis/buttons/pressed.png"
    unpressed= "./Axis/buttons/unpressed.png"
    pressedimage = image.load(pressed)
    unpressedimage = image.load(unpressed)
    button = unpressedimage
    bar = image.load(barimage)
    paddle = image.load(paddleimage)
    horizontal = False
    rotate = 0
    def __init__(self, x =-1, y = -1, axis = -1, controller=False , mode='axis', rotate = 0):
            self.x = x
            self.y = y
            self.ymod = -1
            self.axis = axis
            self.axisstate = 0
            self.controller = controller
            self.activestate = False
            self.mode = mode
            self.modedict = {'axis':self.drawAxisMode, 'button':self.drawButtonMode}
            self.loaddict = {'axis':self.loadAxisMode, 'button':self.loadButtonMode}
            self.draw = self.modedict[mode]
            self.load = self.loaddict[mode]
            self.rotate = rotate

    def UpdateSelf(self):
        if self.controller.gamepad:
            if len(self.controller.axisdict) >= 0:
                if self.axis in self.controller.axisdict:
                    self.axisstate = self.controller.gamepad.get_axis(self.axis)
            else:
                self.axisstate = 0
        else:
            self.axisstate = 0
        self.ymod = abs(-1 - self.axisstate)/2

        if self.activestate == False:
            if self.ymod > .1:
                self.activestate = True
                return True
            return False

        if self.ymod < .1:
            self.activestate = False
        return False


    def draw(self, WINDOW):
        return False

    def drawAxisMode(self, WINDOW):
        if self.horizontal:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x + (100 * self.ymod), self.y - 4))
        else:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x - 4, (self.y + (100 * self.ymod))))

    def drawButtonMode(self, WINDOW):
        if self.activestate == False:
            if self.button != self.unpressedimage:
                self.button = self.unpressedimage
        else:
            if self.button != self.pressedimage:
                self.button = self.pressedimage

        WINDOW.blit(self.button, (self.x,self.y))

    def load(self):
        return

    def loadAxisMode(self):
        self.bar = image.load(self.barimage)
        self.paddle = image.load(self.paddleimage)
        if self.horizontal:
            self.bar = transform.rotate(self.bar, 90)
            self.paddle = transform.rotate(self.paddle, 90)

    def loadButtonMode(self):
        self.unpressedimage = image.load(self.unpressed)
        self.pressedimage = image.load(self.pressed)
        self.pressedimage = transform.rotate(self.pressedimage, self.rotate)
        self.unpressedimage = transform.rotate(self.unpressedimage, self.rotate)

    def Rotate(self):
       self.horizontal = not self.horizontal
       self.load()

    def ModeAdjust(self):
        self.draw = self.modedict[self.mode]
        self.load = self.loaddict[self.mode]

class Stick():
    pressed = "./sticks/stickpressed.png"
    unpressed = "./sticks/stickunpressed.png"
    stickunpressed = image.load(unpressed)
    stickpressed = image.load(pressed)
    rotate = 0

    def __init__(self, x, y, vertaxis = -1, horaxis = -1, buttonnum = -1, controller=False):
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
        self.pressedstate = False
        self.controller = controller
        self.rect = self.image.get_rect()
        self.horactive = False
        self.vertactive = False
    def UpdateSelf(self):
        if(self.buttonnum >= 0):
            if self.controller.gamepad:
                if self.buttonnum < self.controller.gamepad.get_numbuttons():
                        self.pressedstate = self.controller.gamepad.get_button(self.buttonnum)
            else:
                self.pressedstate = 0
        else:
            self.pressedstate == 0
        action = False
        if self.pressedstate == 0:
            self.image = self.stickunpressed
            action =  False
        else:
            if self.image != self.stickpressed:
                self.image = self.stickpressed
                action = True
            else:
                action = False
        if self.controller.gamepad:
            if self.vertaxis >= 0:
                if self.vertaxis < self.controller.gamepad.get_numaxes():
                    self.vertstate = self.controller.gamepad.get_axis(self.vertaxis)
                else:
                    self.vertstate = 0
                self.vertmod = (self.rect.height/2)*self.vertstate
            if self.horaxis >= 0:
                if self.horaxis < self.controller.gamepad.get_numaxes():
                    self.horstate = self.controller.gamepad.get_axis(self.horaxis)
                else:
                    self.horstate = 0
            self.hormod = (self.rect.width/2)*self.horstate

        if self.horactive == False:
            if abs(self.hormod) > 2:
                self.horactive = True
                self.controller.actioncount = self.controller.actioncount + 1


        if abs(self.hormod) < 2:
            self.horactive = False

        if self.vertactive == False:
            if abs(self.vertmod) > 2:
                self.vertactive = True
                self.controller.actioncount = self.controller.actioncount + 1

        if abs(self.vertmod) < 2:
            self.vertactive = False

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

    def dropItems(self):

        droplist = []
        axis = []

        if self.vertaxis >= 0:
            axisadd = TriggerAxis(self.x, self.y - (self.stickunpressed.get_rect().bottomright[1]), self.vertaxis, self.controller)
            axisadd.Rotate()
            axis.append(axisadd)

        if self.horaxis >= 0:
            axisadd = TriggerAxis(self.x, self.y - (self.stickunpressed.get_rect().bottomright[1] * 2), self.horaxis, self.controller)
            axisadd.Rotate()
            axis.append(axisadd)

        droplist.append(axis)
        if self.buttonnum >= 0:
            buttonadd = Button(self.buttonnum, self.x, (self.y - self.stickunpressed.get_rect().bottomright[1] * 3), self.controller)
            droplist.append(buttonadd)

        self.vertaxis = -1
        self.horaxis = -1
        self.buttonnum = -1

        return droplist

class Hat():
    background = './hats/hatbackground.png'
    pressed = './hats/pressed.png'
    unpressed = './hats/unpressed.png'
    rotate = 0
    rotatemod = 0
    backgroundimage = image.load(background)
    pressedimage = image.load(pressed)
    unpressedimage= image.load(unpressed)
    stateimage = unpressedimage

    def __init__(self, hatnum = -1, x = -1, y = -1, controller = False):
        self.hatnumber = hatnum
        # x and y will be the top left coordinate for the background
        self.x = x
        self.y = y
        self.backgroundrect = self.backgroundimage.get_rect()
        self.staterect = self.stateimage.get_rect()
        self.backgroundcenterx = self.backgroundrect[2]/2
        self.centery = self.backgroundrect[3]/2
        self.state = (0,0)
        self.controller = controller

    #if (self.buttonnum >= 0):
       # if self.controller.gamepad:
           # if self.buttonnum < self.controller.gamepad.get_numbuttons():
              #  self.state = self.controller.gamepad.get_button(self.buttonnum)
      #  else:
           # self.state = 0
  #  else:
       # self.state == 0


    def UpdateSelf(self):
        action = False
        if (self.hatnumber >= 0):
            if self.controller:
                if self.controller.gamepad:
                    length = self.controller.gamepad.get_numhats()
                    if self.hatnumber < length and self.hatnumber > -1:
                        if self.state != self.controller.gamepad.get_hat(self.hatnumber) and self.state != (0,0):
                            action = True
                        self.state = self.controller.gamepad.get_hat(self.hatnumber)
                    else:
                        self.state = (0,0)
        else:
            self.state == (0,0)

        self.updateImage()
        return action

    def updateImage(self):

        #self.imagex = (self.state[0] * self.staterect[2]) + self.backgroundrect[2]/2 - self.staterect[3]/2 + self.x+1
        #self.imagey = (-self.state[1] * self.staterect[3]) - self.staterect[3]/2 + self.backgroundrect[3]/2 + self.y
        self.rotatemod = 0
        xstate = self.state[0]
        ystate = self.state[1]
        staterectx = self.staterect[2]
        staterecty = self.staterect[3]
        backgroundrectx = self.backgroundrect[2]
        backgroundrecty = self.backgroundrect[3]
        if self.state == (0, 0):
            self.stateimage = self.unpressedimage
        else:
            self.stateimage = self.pressedimage
            if xstate != 0:
                self.rotatemod = self.rotatemod - (90*xstate)
            if ystate != 0:
                if self.rotatemod !=0:
                    self.rotatemod = self.rotatemod - (45*ystate*-xstate)
                elif ystate == -1:
                    self.rotatemod = 180

        self.staterect = self.stateimage.get_rect()

        if xstate != 0 and ystate != 0:
            self.imagex = xstate*staterectx + backgroundrectx / 2 - staterectx/2 + self.x + 1 - staterectx/4
            self.imagey = (-ystate * staterecty) - staterecty / 2 + backgroundrecty / 2 + self.y - staterecty/4
        else:
            self.imagex = (xstate * staterectx) + backgroundrectx / 2 - staterectx / 2 + self.x + 1
            self.imagey = (-ystate * staterecty) - staterecty / 2 + backgroundrecty / 2 + self.y
        self.stateimage = transform.rotate(self.stateimage, self.rotate+self.rotatemod)

    def draw(self,WINDOW):
        WINDOW.blit(self.backgroundimage, (self.x, self.y))
        WINDOW.blit(self.stateimage, (self.imagex, self.imagey))

    def load(self):
        self.backgroundimage = transform.rotate(image.load(self.background), self.rotate)
        self.pressedimage = image.load(self.pressed)
        self.unpressedimage = image.load(self.unpressed)
        self.updateImage()

