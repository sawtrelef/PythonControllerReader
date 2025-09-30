import pygame
from PS5Controller import PlayStation5Controller
from joystickstuff import Button, TriggerAxis, Stick, Hat
from GenericController import GenericController
from ClickableOptionButton import ClickableOptionButton
from FileStuff import FileWindow, FileBox
from os import listdir



pygame.init()
joysticks = {}
for i in range (pygame.joystick.get_count()):
    joysticks[i] = pygame.joystick.Joystick(i)
font = pygame.font.Font('SuperMystery.ttf', 32)
background = pygame.image.load("assets/Background.png")
rect = background.get_rect()
x = int(rect.bottomright[0])
y = int(rect.bottomright[1])
pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((x,y+24))
clock = pygame.time.Clock()
filewindow = FileWindow()


class APMCounter():
    valuelist = []
    timepassed = 0
    actionperlastminute = 0
    averageapm = 0
    highest = 0
    ValueTarget = False
    def __init__(self,target):
        self.ValueTarget = target
        self.text = font.render('APLM: ' + str(self.actionperlastminute), True, (149, 75, 220))
        rect = self.text.get_rect()
        self.width = rect.width
        self.height = rect.height

    def update(self):
        num = self.ValueTarget.getcount()
        self.valuelist.append(num)
        self.timepassed = self.timepassed + 1
        if self.timepassed > 3600:
            self.valuelist.pop(0)
        length = len(self.valuelist)
        num1 = self.valuelist[length-1]
        num2 = self.valuelist[0]
        value = num1 - num2
        self.actionperlastminute = value
        if self.actionperlastminute > self.highest:
            self.highest = self.actionperlastminute
        self.averageapm = int(self.valuelist[length-1]/(self.timepassed/3600))

    def draw(self, WINDOW):
        self.text = font.render('APLM: ' + str(self.actionperlastminute), True, (149, 75, 220))
        WINDOW.blit(self.text, (int(x/2)-int(self.width/2), y-self.height))

    def resetCounter(self):
        self.valuelist = []
        self.timepassed = 0

controller = False

def load(filename = ""):
    if filename == "":
        filename = "./layouts/layout.txt"
    file = open(filename, 'r')

    ## generates a list object that holds each line as a string
    # Current load order is buttons first, then axis, then sticks
    lines = file.readlines()
    bookmarks = []
    length = len(lines)
    ## removes the newline character from the end of each line
    for i in range(length):
        lines[i] = lines[i].removesuffix('\n')
        if lines[i][0] == 'N':
            bookmarks.append(i)

    buttondict = {}
    for i in range(bookmarks[0], bookmarks[1]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            buttonnum = int(values[0])
            xpos = int(values[1])
            ypos = int(values[2])
            offimage = str(values[3])
            onimage = str(values[4])
            rotation = int(values[5])
            name = ""
            if 6 < len(values):
                name = str(values[6])
            addbutton = Button(buttonnum, xpos, ypos, False, name)
            addbutton.unpressed = offimage
            addbutton.pressed = onimage
            addbutton.rotate = rotation
            addbutton.load()
            buttondict[buttonnum] = addbutton

    axisdict = {}
    for i in range(bookmarks[1], bookmarks[2]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            axisnum = int(values[0])
            xpos = int(values[1])
            ypos = int(values[2])
            triggerimage = str(values[3])
            paddleimage = str(values[4])
            flipbool = values[5]
            mode = str(values[6])
            rotate = int(values[7])
            name = ""
            if 8 < len(values):
                name = str(values[8])
            if flipbool == 'True':
                flipbool = True
            else:
                flipbool = False
            addtrigger = TriggerAxis(xpos, ypos, axisnum, False, mode, rotate, name)
            addtrigger.paddleimage = paddleimage
            addtrigger.barimage = triggerimage
            addtrigger.horizontal = flipbool
            addtrigger.load()
            axisdict[axisnum] = addtrigger

    sticklist = []
    for i in range(bookmarks[2], bookmarks[3]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            ##Stick extraction data format
            # (vertaxis,horizontalaxis,buttonnum, xpos, ypos, pressed, unpressed)
            values = lines[i].split(',')
            vertaxis = int(values[0])
            horizontalaxis = int(values[1])
            xpos = int(values[3])
            ypos = int(values[4])
            buttonnumber = int(values[2])
            onimage = values[5]
            offimage = values[6]
            stickname = ""
            buttonname = ""
            if 7 < len(values):
                stickname = values[7]
            if 8 < len(values):
                buttonname = values[8]
            # stick creation data format
            # (xpos,ypos,vertaxis, horizontalaxis, buttonnumber)
            addstick = Stick(xpos, ypos, vertaxis, horizontalaxis, buttonnumber,False,stickname, buttonname)
            addstick.pressed = onimage
            addstick.unpressed = offimage
            addstick.load()
            sticklist.append(addstick)
    hatdict = {}
    for i in range(bookmarks[3], length):
        if lines[i][0] == '(':
            # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            hatnum = int(values[0])
            xpos = int(values[1])
            ypos = int(values[2])
            rotation = int(values[3])
            onimage = str(values[4])
            offimage = str(values[5])
            backgroundimage = str(values[6])
            name = ""
            if 7 < len(values):
                name = str(values[7])

            addhat = Hat(hatnum, xpos, ypos, False, name)
            addhat.unpressed = offimage
            addhat.pressed = onimage
            addhat.background = backgroundimage
            addhat.rotate = rotation
            addhat.load()
            hatdict[hatnum] = addhat

    if controller:
        Controller = GenericController(controller.gamepad)
    else:
        if(len(joysticks)>0):
            Controller = GenericController(joysticks[0])
        else:
            Controller = GenericController(False)
    Controller.buttondict = buttondict
    Controller.axisdict = axisdict
    Controller.sticklist = sticklist
    Controller.hatdict = hatdict
    file.close()
    Controller.resetListItems()
    if Controller:
        return Controller
    return False

def createlogfile():
    filelist = listdir('./logs')
    listlen = len(filelist)
    logname = 'log_'+str(listlen)+".txt"
    file = open('./logs/'+logname, 'w')
    duration = controller.timecount
    actions = controller.actioncount
    minutes = int(duration/3600)
    seconds = int((duration%3600)/60)
    leftover = duration%60
    average = counter.averageapm
    highest = counter.highest
    file.write("Frames Logged(60 fps): " + str(duration)+'\n')
    file.write("Actual time passed: " +str(minutes)+"m"+str(seconds)+"s"+ " and " + str(leftover) +" frames"+'\n')
    file.write("Actions logged: " +str(actions)+'\n')
    file.write("Overall average per minute: " + str(average)+'\n')
    file.write("Highest minute: " + str(highest)+'\n')
    buttondict = controller.buttondict
    axisdict = controller.axisdict
    hatdict = controller.hatdict
    sticklist = controller.sticklist
    file.write ("BTTONS *************\n")
    for item in buttondict:
        var = buttondict[item].actions
        if len(buttondict[item].name) > 0:
            name = buttondict[item].name
        else:
            name = buttondict[item].buttonnum
        #name = buttondict[item].name
        file.write("Button " +str(name)+": " + str(var) + "\n")
    file.write ("AXIS *************\n")
    for item in axisdict:
        var = axisdict[item].actions
        if len(axisdict[item].name) > 0:
            name = axisdict[item].name
        else:
            name = axisdict[item].axis
        # name = axisdict[item].name
        file.write("Axis " +str(name)+": " + str(var) + "\n")
    file.write("HATS *************\n")
    for item in hatdict:
        var = hatdict[item].actions
        if len(hatdict[item].name)>0:
            name = hatdict[item].name
        else:
            name = hatdict[item].hatnumber
        # name = hatdict[item].name
        file.write("Hat " +str(name)+": " + str(var) + "\n")
    file.write ("STICKS *************\n")
    for i in range(len(sticklist)):
        pressed = sticklist[i].pressactions
        moved = sticklist[i].moveactions
        total = pressed+moved
        if len(sticklist[i].stickname) > 0:
            name = sticklist[i].stickname
        else:
            name = i

        if len(sticklist[i].buttonname) > 0:
            buttname = sticklist[i].buttonname
        else:
            buttname = "pressed"
        # name = sticklist[i].name
        file.write("Stick " + str(name) + "- total = " +str(total) + " - "+buttname+" = " +str(pressed) + " - moved = " +str(moved) + "\n")

    file.close()
    Reset()


controller = load("./layouts/layout.txt")
controller.resetListItems()
counter = APMCounter(controller)

def Reset():
        counter.resetCounter()
        controller.resetCounter()
        return 0

def ToggleLines():
    controller.StickLines = not controller.StickLines

def loadclicked(self):
    dummy = load("./layouts/"+self.text)
    drawlist[0] = dummy
    counter.ValueTarget =  dummy
    return dummy

def LoadButtonDoClicked():
    itemlist = filewindow.UpdateSelf("./layouts/",(position[0],position[1]))

    for item in itemlist:
        item.clickdummy = loadclicked

    return itemlist

resetimage = pygame.image.load('./assets/resetbutton.png')
resetrect = resetimage.get_rect()
ResetButton = ClickableOptionButton(1, y,resetimage)
ResetButton.doclicked = Reset

loadimage = pygame.image.load('assets/loadbutton.png')
loadrect = loadimage.get_rect()
LoadButton = ClickableOptionButton(ResetButton.rect.x + loadrect.width+1, ResetButton.rect.y,loadimage)
LoadButton.doclicked = LoadButtonDoClicked

linetoggleimage = pygame.image.load('./assets/linesbutton.png')
linerect = linetoggleimage.get_rect()
LineToggleButton = ClickableOptionButton(x-linerect.width, y,linetoggleimage)
LineToggleButton.doclicked = ToggleLines

logbuttonimage = pygame.image.load('./assets/logbutton.png')
logrect = logbuttonimage.get_rect()
LogButton = ClickableOptionButton(LoadButton.rect.x+LoadButton.rect.width, y, logbuttonimage)
LogButton.doclicked = createlogfile


collidables = []
collidables.append(ResetButton)
collidables.append(LineToggleButton)
collidables.append(LoadButton)
collidables.append(LogButton)
drawlist = [controller, counter,ResetButton, LoadButton, LineToggleButton, LogButton, filewindow]


def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    if mousex >= collisionbox[0] and mousex <= collisionbox[0]+collisionbox[2]:
        if mousey >= collisionbox[1] and mousey <= collisionbox[1]+collisionbox[3]:
            return True
    return False

#controller = PlayStation5Controller(0)

done = False
while not done:

    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                touch = False
                check = False
                filewindow.state = False

                for i in range(len(collidables) - 1, -1, -1):
                    item = collidables[i]
                    touch = CollisionCheck(position, item.rect)
                    if touch:
                        collided = item
                        if collided.__class__ == ClickableOptionButton:
                            check = collided.doclicked()
                            if check.__class__ == dict:
                                for item in check:
                                    collidables.append(item)
                        elif collided.__class__ == FileBox:
                            check = collided.doclicked()
                            print("high")
                            if check.__class__ == GenericController:
                                controller = check
                        break

                if check.__class__ != dict:
                    for item in filewindow.itemdict:
                        for thing in collidables:
                            if thing == item:
                                collidables.remove(item)
                    break

        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            ID = joy.get_instance_id()
            joysticks[ID] = joy
            if controller:
                if controller.gamepad == False:
                    controller.gamepad = joysticks[ID]
                    controller.resetListItems()

        if event.type == pygame.JOYDEVICEREMOVED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = event.instance_id
            #ID = ActiveStick.gamepad.get_instance_id()
            if controller:
                if controller.gamepad:
                    if controller.gamepad.get_instance_id() == joy:
                        controller.gamepad = False
                        words = "PRESS BUTTON"
                        text = font.render(words, True, (200, 74, 220))
            del joysticks[joy]
    if done:

        break

    controller.update()
    counter.update()
    display.blit(background, (0,0))

    for item in drawlist:
        item.draw(display)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()