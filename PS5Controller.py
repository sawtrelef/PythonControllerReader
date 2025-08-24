from pygame import image, transform, draw
from joystickstuff import Button, TriggerAxis, Stick

xbutton = Button(0,302,111)
obutton = Button(1, 322, 91)
sqbutton = Button(2, 282, 91)
tbutton = Button(3, 302, 71)

upbutton = Button(11,81, 71)
upbutton.unpressed = "./buttons/arrowunpressed.png"
upbutton.pressed = "./buttons/arrowpressed.png"
downbutton = Button(12,81, 111)
downbutton.unpressed = "./buttons/arrowunpressed.png"
downbutton.pressed = "./buttons/arrowpressed.png"
downbutton.rotate=180

leftbutton = Button(13,61, 91)
leftbutton.unpressed = "./buttons/arrowunpressed.png"
leftbutton.pressed = "./buttons/arrowpressed.png"
leftbutton.rotate = 90

rightbutton = Button(14,101, 91)
rightbutton.unpressed = "./buttons/arrowunpressed.png"
rightbutton.pressed = "./buttons/arrowpressed.png"
rightbutton.rotate = 270


lbump = Button(9,60, 5)
lbump.unpressed = "./buttons/bumperunpressed.png"
lbump.pressed = "./buttons/bumperpressed.png"
rbump = Button(10,243, 5)
rbump.unpressed = "./buttons/bumperunpressed.png"
rbump.pressed = "./buttons/bumperpressed.png"
mbump = Button(15, 153, 71)
mbump.unpressed = "./buttons/bumperunpressed.png"
mbump.pressed = "./buttons/bumperpressed.png"

sharebutton = Button(4, 121, 71)
sharebutton.unpressed = "./buttons/unpressedoption.png"
sharebutton.pressed = "./buttons/pressedoption.png"
pausebutton = Button(6, 256, 71)
pausebutton.unpressed = "./buttons/unpressedoption.png"
pausebutton.pressed = "./buttons/pressedoption.png"
micbutton = Button(16, 195, 141)
micbutton.unpressed = "./buttons/unpressedoption.png"
micbutton.pressed = "./buttons/pressedoption.png"
micbutton.rotate = 90
psbutton = Button(5, 195, 122)
psbutton.pressed = "./buttons/playstationpressed.png"
psbutton.unpressed = "./buttons/playstationunpressed.png"

l2Trigger = TriggerAxis(4, 18, 5)
r2Trigger = TriggerAxis(5, 378, 5)

lstick = Stick(147, 185,1,0, 7)
rstick = Stick( 249, 185,3,2, 8)

class PlayStation5Controller():
    buttonlist = [xbutton,obutton,sqbutton,tbutton,upbutton,downbutton,leftbutton,rightbutton,lbump,rbump,mbump,sharebutton,pausebutton,micbutton,psbutton]
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