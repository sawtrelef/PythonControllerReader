from pygame import image, transform, draw
from joystickstuff import Button, TriggerAxis, Stick

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

l2Trigger = TriggerAxis(4, 18, 5)
r2Trigger = TriggerAxis(5, 378, 5)

lstick = Stick(1,0,7,147, 185)
rstick = Stick(3,2, 8, 249, 185)

class PlayStation5Controller():
    buttonlist = [xbutton,obutton,sqbutton,tbutton,upbutton,downbutton,leftbutton,rightbutton,lbump,rbump,mbump,sharebutton,pausebutton,micbutton,sharebutton,psbutton]
    axislist = [l2Trigger, r2Trigger]
    sticklist = [lstick, rstick]
    def __init__(self, ID):
        self.ID = ID
        self.timecount = 0
        self.actioncount = 0
        self.StickLines = True

    def update(self):
        for item in self.buttonlist:
            check = item.UpdateSelf( self.ID)
            if check:
                self.actioncount = self.actioncount +1
        for item in self.axislist:
            check = item.UpdateSelf(self.ID)
            if check:
                self.actioncount = self.actioncount+1
        for item in self.sticklist:
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
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13), (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)