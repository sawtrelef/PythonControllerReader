from joystickstuff import Button, TriggerAxis, Stick, Hat
from pygame import draw

class LoadGenericController():
    buttondict = {}
    axisdict = {}
    sticklist = []
    hatdict = {}
    StickLines = True
    ID = False
    actioncount = 0
    timecount = 0
    def __init__(self, joystick = False):
        self.gamepad = joystick
        self.buttondict = {}
        self.axisdict = {}
        self.hatdict = {}
        self.sticklist = []
        if self.gamepad:
            for i in range(self.gamepad.get_numbuttons()):
                self.buttondict[i] = Button(i,40, 100+(i*20),self)
            offset = 150 + (i*20)

            for i in range(self.gamepad.get_numaxes()):
                self.axisdict[i] = (TriggerAxis(40, offset + (i*20), i, self))

            for item in self.axisdict:
                self.axisdict[item].Rotate()

            offset = 115
            length = self.gamepad.get_numhats()
            for i in range(length):
                self.hatdict[i] = Hat(i, 70, offset + i*95, self)
                self.hatdict[i].setdefaults()


    def update(self):
        for item in self.buttondict:
            check = self.buttondict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount +1
        for item in self.axisdict:
            check = self.axisdict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount+1
        for item in self.sticklist:
            check = item.UpdateSelf()
            if check:
                self.actioncount = self.actioncount+1
        for item in self.hatdict:
            #check = item.UpdateSelf(item)
            check = self.hatdict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount+1

        self.timecount = self.timecount+1

    def draw(self, WINDOW):
        for item in self.buttondict:
            self.buttondict[item].draw(WINDOW)
        for item in self.axisdict:
            self.axisdict[item].draw(WINDOW)
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13), (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)
        for item in self.hatdict:
            self.hatdict[item].draw(WINDOW)

    def resetCounter(self):
        self.actioncount = 0
        self.timecount = 0
        for item in self.buttondict:
            item.actions = 0
        for item in self.axisdict:
            item.actions = 0
        for item in self.hatdict:
            item.actions = 0
        for item in self.sticklist:
            item.pressactions = 0
            item.moveactions = 0

    def resetListItems(self):
        for item in self.buttondict:
            self.buttondict[item].controller = self
        for item in self.axisdict:
            self.axisdict[item].controller = self
        for item in self.sticklist:
            item.controller = self
        for item in self.hatdict:
            self.hatdict[item].controller = self

class GenericController():
    buttondict = {}
    axisdict = {}
    sticklist = []
    hatdict = {}
    StickLines = True
    ID = False
    actioncount = 0
    timecount = 0
    gamepad = False
    def __init__(self,joystick = False, ID = -1):
        offset = 0
        self.ID = ID
        self.gamepad = joystick

    def update(self):
        for item in self.buttondict:
            check = self.buttondict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount + 1
        for item in self.axisdict:
            check = self.axisdict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount + 1
        for item in self.sticklist:
            check = item.UpdateSelf()
            if check:
                self.actioncount = self.actioncount + 1
        for item in self.hatdict:
            # check = item.UpdateSelf(item)
            check = self.hatdict[item].UpdateSelf()
            if check:
                self.actioncount = self.actioncount + 1

        self.timecount = self.timecount + 1

    def draw(self, WINDOW):
        for item in self.buttondict:
            self.buttondict[item].draw(WINDOW)
        for item in self.axisdict:
            self.axisdict[item].draw(WINDOW)
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13),
                          (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)
        for item in self.hatdict:
            self.hatdict[item].draw(WINDOW)

    def getcount(self):
        return self.actioncount

    def resetCounter(self):
        self.actioncount = 0
        self.timecount = 0
        for item in self.buttondict:
            self.buttondict[item].actions = 0
        for item in self.axisdict:
            self.axisdict[item].actions = 0
        for item in self.hatdict:
            self.hatdict[item].actions = 0
        for item in self.sticklist:
            item.pressactions = 0
            item.moveactions = 0



    def resetListItems(self):
        for item in self.buttondict:
            self.buttondict[item].controller = self
        for item in self.axisdict:
            self.axisdict[item].controller = self
        for item in self.sticklist:
            item.controller = self
        for item in self.hatdict:
            self.hatdict[item].controller = self