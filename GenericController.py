from joystickstuff import Button, TriggerAxis, Stick
from pygame import joystick, draw

class GenericController():
    buttonlist = []
    axislist = []
    sticklist = []
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
            self.axislist.append(TriggerAxis(i,40, offset + (i*20)))

        for item in self.axislist:
            item.flip()

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

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        for item in self.axislist:
            item.draw(WINDOW)
        for item in self.sticklist:
            item.draw(WINDOW)
            if self.StickLines == True:
                draw.line(WINDOW, (0, 255, 0), (item.x + 13, item.y + 13), (item.x + item.hormod + 13, item.y + item.vertmod + 13), 2)

