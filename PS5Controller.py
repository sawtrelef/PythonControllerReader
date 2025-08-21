from pygame import image, transform, draw
from joystickstuff import Button, TriggerAxis, Stick

xbutton = Button(0,302,111)
obutton = Button(1, 322, 91)
sqbutton = Button(2, 282, 91)
tbutton = Button(3, 302, 71)

upbutton = Button(11,81, 71)
upbutton.offimagename = "arrowunpressed.png"
upbutton.onimagename = "arrowpressed.png"
downbutton = Button(12,81, 111)
downbutton.offimagename = "arrowunpressed.png"
downbutton.onimagename = "arrowpressed.png"
downbutton.rotate=180

leftbutton = Button(13,61, 91)
leftbutton.offimagename = "arrowunpressed.png"
leftbutton.onimagename = "arrowpressed.png"
leftbutton.rotate = 90

rightbutton = Button(14,101, 91)
rightbutton.offimagename = "arrowunpressed.png"
rightbutton.onimagename = "arrowpressed.png"
rightbutton.rotate = 270


lbump = Button(9,60, 5)
lbump.offimagename = "bumperunpressed.png"
lbump.onimagename = "bumperpressed.png"
rbump = Button(10,243, 5)
rbump.offimagename = "bumperunpressed.png"
rbump.onimagename = "bumperpressed.png"
mbump = Button(15, 153, 71)
mbump.offimagename = "bumperunpressed.png"
mbump.onimagename = "bumperpressed.png"

sharebutton = Button(4, 131, 71)
sharebutton.offimagename = "unpressedoption.png"
sharebutton.onimagename = "pressedoption.png"
pausebutton = Button(6, 256, 71)
pausebutton.offimagename = "unpressedoption.png"
pausebutton.onimagename = "pressedoption.png"
micbutton = Button(16, 195, 141)
micbutton.offimagename = "unpressedoption.png"
micbutton.onimagename = "pressedoption.png"
micbutton.rotate = 90
psbutton = Button(5, 195, 122)
psbutton.onimagename = "playstationpressed.png"
psbutton.offimagename = "playstationunpressed.png"

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
        for item in self.buttonlist:
            item.load()
        for item in self.axislist:
            item.load()
        for item in self.sticklist:
            item.load()


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