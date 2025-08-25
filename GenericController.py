from joystickstuff import Button, TriggerAxis, Stick, Hat
from pygame import joystick, draw

class LoadGenericController():
    buttonlist = []
    axislist = []
    sticklist = []
    hatlist = []
    StickLines = True
    ID = False
    actioncount = 0
    timecount = 0
    def __init__(self, joystick, ID = 0):
        offset = 0
        self.ID = ID
        for i in range(joystick.get_numbuttons()):
            self.buttonlist.append(Button(i,40, 100+(i*20)))
        offset = 150 + (i*20)

        for i in range(joystick.get_numaxes()):
            self.axislist.append(TriggerAxis(40, offset + (i*20), i))

        for item in self.axislist:
            item.Rotate()

        offset = 115
        for i in range(joystick.get_numhats()):
            self.hatlist.append(Hat(i, 70, offset + i*95))
        dummyhat = Hat(-1, 70, 115)
        dummyhat.state = (-1,-1)
        def stinkupdate(self):
            self.updateImage()
            return False
        dummyhat.UpdateSelf = stinkupdate
        self.hatlist.append(dummyhat)

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
        for item in self.hatlist:
            check = item.UpdateSelf(item)
            #check = item.UpdateSelf(self.ID)
            if check:
                self.actioncount = self.actioncount+1

        self.timecount = self.timecount+1

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        for item in self.axislist:
            item.draw(WINDOW)
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13), (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)
        for item in self.hatlist:
            item.draw(WINDOW)

class GenericController():
    buttonlist = []
    axislist = []
    sticklist = []
    hatlist = []
    StickLines = True
    ID = False
    actioncount = 0
    timecount = 0
    def __init__(self, ID = 0):
        offset = 0
        self.ID = ID

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
        for item in self.hatlist:
            check = item.UpdateSelf(self.ID)
            if check:
                self.actioncount = self.actioncount+1

        self.timecount = self.timecount+1

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        for item in self.axislist:
            item.draw(WINDOW)
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13), (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)
        for item in self.hatlist:
            item.draw(WINDOW)

    def getcount(self):
        return self.actioncount