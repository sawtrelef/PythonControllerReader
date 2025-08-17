from pygame import joystick, image, transform, draw

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

xbutton = Button(0,302,111)
obutton = Button(1, 322, 91)
sqbutton = Button(2, 282, 91)
tbutton = Button(3, 302, 71)

upbutton = Button(11,81, 71)
upbutton.off = image.load("arrowunpressed.png")
upbutton.on = image.load("arrowpressed.png")
downbutton = Button(12,81, 111)
downbutton.off = image.load("arrowunpressed.png")
downbutton.on = image.load("arrowpressed.png")
downbutton.off = transform.rotate(downbutton.off,180)
downbutton.on = transform.rotate(downbutton.on,180)
leftbutton = Button(13,61, 91)
leftbutton.off = image.load("arrowunpressed.png")
leftbutton.on = image.load("arrowpressed.png")
leftbutton.off = transform.rotate(downbutton.off,270)
leftbutton.on = transform.rotate(downbutton.on,270)
rightbutton = Button(14,101, 91)
rightbutton.off = image.load("arrowunpressed.png")
rightbutton.on = image.load("arrowpressed.png")
rightbutton.off = transform.rotate(downbutton.off,90)
rightbutton.on = transform.rotate(downbutton.on,90)

lbump = Button(9,60, 5)
lbump.off = image.load("bumperunpressed.png")
lbump.on = image.load("bumperpressed.png")
rbump = Button(10,243, 5)
rbump.off = image.load("bumperunpressed.png")
rbump.on = image.load("bumperpressed.png")
mbump = Button(15, 153, 71)
mbump.off = image.load("bumperunpressed.png")
mbump.on = image.load("bumperpressed.png")

sharebutton = Button(4, 131, 71)
sharebutton.off = image.load("unpressedoption.png")
sharebutton.on = image.load("pressedoption.png")
pausebutton = Button(6, 256, 71)
pausebutton.off = image.load("unpressedoption.png")
pausebutton.on = image.load("pressedoption.png")
micbutton = Button(16, 195, 141)
micbutton.off = image.load("unpressedoption.png")
micbutton.on = image.load("pressedoption.png")
micbutton.off = transform.rotate(micbutton.off,90)
micbutton.on = transform.rotate(micbutton.on, 90)
psbutton = Button(5, 195, 122)
psbutton.on = image.load("playstationpressed.png")
psbutton.off = image.load("playstationunpressed.png")

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

l2Trigger = TriggerAxis(4, 18, 5)
r2Trigger = TriggerAxis(5, 378, 5)


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
        draw.line(WINDOW,(0,255,0),(self.x+13, self.y+13),(self.x+self.hormod+13, self.y+self.vertmod+13), 2)

lstick = Stick(1,0,7,147, 185)
rstick = Stick(3,2, 8, 249, 185)

class PlayStation5Controller():
    joystick.init()
    joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]
    buttonlist = [xbutton,obutton,sqbutton,tbutton,upbutton,downbutton,leftbutton,rightbutton,lbump,rbump,mbump,sharebutton,pausebutton,micbutton,sharebutton,psbutton]
    axislist = [l2Trigger, r2Trigger, lstick, rstick]
    def __init__(self, ID):
        self.ID = ID
        self.timecount = 0
        self.actioncount = 0

    def update(self):
        for item in self.buttonlist:
            check = item.UpdateSelf( self.ID)
            if check:
                self.actioncount = self.actioncount +1
        for item in self.axislist:
            check = item.UpdateSelf(self.ID)
            if check:
                self.actioncount = self.actioncount+1
        self.timecount = self.timecount+1

    def getcount(self):
        return int(self.actioncount)

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        for item in self.axislist:
            item.draw(WINDOW)
