import pygame
from Actions import ModAction, ActionContainer
from PS5Controller import PlayStation5Controller
from os import listdir
from joystickstuff import Button, Stick, TriggerAxis, Hat
from GenericController import LoadGenericController, GenericController
from ClickableOptionButton import ClickableOptionButton

pygame.init()

font = pygame.font.Font('Zou.ttf', 48)

pygame.display.set_caption('Build Your Controller Layout')
workrectimage = pygame.image.load('assets/Background.png')
workrect = workrectimage.get_rect()
width = workrect.bottomright[0]
height = workrect.bottomright[1]
x = 150
y = 350

displaywidth = 600
displayheight = 725

if x + width > displaywidth:
    displaywidth = x + width +20

if y + height + 115 > displayheight:
    displayheight = y + height + 115

display = pygame.display.set_mode((displaywidth,displayheight))
rect = pygame.rect.Rect(0,0,displaywidth,displayheight)

clock = pygame.time.Clock()

done = False
words = "PRESS BUTTON"
name = ""
text = font.render(words, True, (200, 74, 220))

drawlist = []
joysticks = {}
for i in range (pygame.joystick.get_count()):
    joysticks[i] = pygame.joystick.Joystick(i)

ActiveStick = False
currentAction = ActionContainer()

collidables = []

class HoldingCell():
    def __init__(self):
        self.holding = False
        self.dragging = False
        self.buttonlist = []
        self.changelist = []

    def holdItem(self,item):
        self.holding = item
        if item:
            self.dragging = True

    def stopdrag(self):
        self.dragging = False

    def Drag(self, position):
        self.holding.x = position[0]-5
        self.holding.rect.x = position[0]-5
        self.holding.y = position[1]-5
        self.holding.rect.y = position[1]-5

    def update(self):
        for item in self.buttonlist:
            for thing in collidables:
                if item == thing:
                    collidables.remove(item)
        self.buttonlist = []
        if self.holding.__class__ == Button:
            self.changelist = []
            directory = './buttons/'
            filelist = listdir(directory)
            for file in filelist:
                if 'unpressed' in file:
                    self.changelist.append(directory+file)
            self.buttonlist = ButtonModList
        if self.holding.__class__ == Stick:
            self.changelist = []
            directory = './sticks/'
            filelist = listdir(directory)
            for file in filelist:
                if 'unpressed' in file:
                    self.changelist.append(directory+file)
            self.buttonlist = StickModList
        if self.holding.__class__ == TriggerAxis:
            self.changelist = []
            directory = './Axis/'
            filelist = listdir(directory)
            for file in filelist:
                if 'unpressed' in file:
                    self.changelist.append(directory + file)
            self.buttonlist = AxisModList
        if self.holding.__class__ == Hat:
            self.changelist = []
            directory = './hats/'
            filelist = listdir(directory)
            for file in filelist:
                if 'unpressed' in file:
                    self.changelist.append(directory + file)
            self.buttonlist = HatModList
        templist = []
        for item in collidables:
            templist.append(item)
        collidables.clear()
        for item in self.buttonlist:
            collidables.append(item)
        for item in templist:
            collidables.append(item)

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)

widgetCell = HoldingCell()


def save():
    file = open('layout.txt', 'w')
    if ActiveStick:
        buttondict = ActiveStick.buttondict
        length = len(buttondict)
        print("Number of Independent buttons: " + str(length) + '\n')
        file.write("Number of Independent buttons: " + str(length) + '\n')
        for button in buttondict:
            #(buttonnum, x, y, offimage, onimage, rotation)
            number = str(buttondict[button].buttonnum)
            xposition = str(buttondict[button].x-x)
            yposition = str(buttondict[button].y-y)
            onimage = str(buttondict[button].pressed)
            offimage = str(buttondict[button].unpressed)
            rotation = str(buttondict[button].rotate)
            buttontext = "({},{},{},{},{},{})\n".format(number,xposition,yposition, offimage,onimage,rotation)
            print(buttontext)
            file.write(buttontext)
        axisdict = ActiveStick.axisdict
        length = len(axisdict)
        print("Number of Independent Axis: " + str(length) + '\n')
        file.write("Number of Independent Axis: " + str(length) + '\n')
        for axis in axisdict:
            #(axisnumber, xpos, ypos, barimage, paddleimage, flippedbool)
            number = str(axisdict[axis].axis)
            xpos = str(axisdict[axis].x-x)
            ypos = str(axisdict[axis].y-y)
            barim = str(axisdict[axis].barimage)
            paddleim = str(axisdict[axis].paddleimage)
            flip = str(axisdict[axis].horizontal)
            axistext = "({},{},{},{},{},{})\n".format(number,xpos,ypos,barim,paddleim,flip)
            print(axistext)
            file.write(axistext)
        sticklist = ActiveStick.sticklist
        length = len(sticklist)
        print("Number of Sticks: " + str(length) + '\n')
        file.write("Number of Sticks: " + str(length) + '\n')
        for stick in sticklist:
            #(vertaxis,horizontalaxis,buttonnumber, xpos, ypos, pressed, unpressed)
            vertaxis = str(stick.vertaxis)
            horizontal = str(stick.horaxis)
            button = str(stick.buttonnum)
            xpos = str(stick.x-x)
            ypos = str(stick.y-y)
            pressed = str(stick.pressed)
            unpressed = str(stick.unpressed)
            sticktext = "({},{},{},{},{},{},{})\n".format(vertaxis,horizontal,button,xpos,ypos,pressed,unpressed)
            print(sticktext)
            file.write(sticktext)
        hatdict = ActiveStick.hatdict
        length = len(hatdict)
        print("Number of Hats: " + str(length) + '\n')
        file.write("Number of Hats: " + str(length) + '\n')
        for hat in hatdict:
            # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            number = str(hatdict[hat].hatnumber)
            xposition = str(hatdict[hat].x - x)
            yposition = str(hatdict[hat].y - y)
            onimage = str(hatdict[hat].pressed)
            offimage = str(hatdict[hat].unpressed)
            backgroundimage = str(hatdict[hat].background)
            rotation = str(hatdict[hat].rotate)
            hattext = '({},{},{},{},{},{},{},)\n'.format(number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            print(hattext)
            file.write(hattext)

    else:
        print("nothing to save")
        ##buttons
        #triggers
        #sticks
    file.close()

def load(filename = ""):
    if filename == "":
        filename = "layout.txt"
    file = open(filename, 'r')
    collidables = [SaveButton, LoadButton, ReloadButton]

    ## generates a list object that holds each line as a string
    #Current load order is buttons first, then axis, then sticks
    lines = file.readlines()
    bookmarks = []
    length = len(lines)
    ## removes the newline character from the end of each line
    for i in range(length):
        lines[i] = lines[i].removesuffix('\n')
        if lines[i][0] == 'N':
            bookmarks.append(i)

    buttondict = {}
    for i in range(bookmarks[0],bookmarks[1]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            buttonnum = int(values[0])
            xpos = int(values[1])+x
            ypos = int(values[2])+y
            offimage = str(values[3])
            onimage = str(values[4])
            rotation = int(values[5])
            addbutton = Button(buttonnum,xpos,ypos)
            addbutton.unpressed = offimage
            addbutton.pressed = onimage
            addbutton.rotate = rotation
            addbutton.load()
            buttondict[buttonnum] = addbutton

    axisdict = {}
    for i in range(bookmarks[1],bookmarks[2]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            axisnum = int(values[0])
            xpos = int(values[1])+x
            ypos = int(values[2])+y
            triggerimage = str(values[3])
            paddleimage = str(values[4])
            flipbool = values[5]
            if flipbool == 'True':
                flipbool = True
            else:
                flipbool = False
            addtrigger = TriggerAxis(xpos, ypos, axisnum)
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
            xpos = int(values[3])+x
            ypos = int(values[4])+y
            buttonnumber = int(values[2])
            onimage = values[5]
            offimage = values[6]
            #stick creation data format
            #(xpos,ypos,vertaxis, horizontalaxis, buttonnumber)
            addstick = Stick(xpos,ypos,vertaxis,horizontalaxis,buttonnumber)
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
            xpos = int(values[1]) + x
            ypos = int(values[2]) + y
            rotation = int(values[3])
            onimage = str(values[4])
            offimage = str(values[5])
            backgroundimage = str(values[6])

            addhat = Hat(hatnum, xpos, ypos)
            addhat.unpressed = offimage
            addhat.pressed = onimage
            addhat.background = backgroundimage
            addhat.rotate = rotation
            addhat.load()
            hatdict[hatnum]=addhat

    if ActiveStick:
        Controller = GenericController(ActiveStick.gamepad)
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

def makeStick():
    emptystick = Stick(MakeStickButton.rect.x + 145, MakeStickButton.rect.y)
    print(emptystick)
    if emptystick.controller == False:
        if ActiveStick:
            emptystick.controller = ActiveStick
    return emptystick

def reloadController():
    if ActiveStick:
        if ActiveStick.gamepad:
            stick = LoadGenericController(ActiveStick.gamepad)
        else:
            stick = LoadGenericController()
    else:
        stick = LoadGenericController()
    return stick


saveimage = pygame.image.load('assets/savebutton.png')
loadimage = pygame.image.load('assets/loadbutton.png')
makestickimage = pygame.image.load('assets/makestickbutton.png')
reloadimage = pygame.image.load('assets/reloadbutton.png')

SaveButton = ClickableOptionButton((x + width)/2-(saveimage.get_rect().bottomright[0])/2,y + height + 20,saveimage)
LoadButton = ClickableOptionButton(SaveButton.rect.x + 145, SaveButton.rect.y,loadimage)
ReloadButton = ClickableOptionButton(0,0,reloadimage)


MakeStickButton = ClickableOptionButton(SaveButton.rect.x +(LoadButton.rect.x - SaveButton.rect.x)/2,SaveButton.rect.y + 50, makestickimage)
SaveButton.doclicked = save
LoadButton.doclicked = load
MakeStickButton.doclicked = makeStick
ReloadButton.doclicked = reloadController

collidables.append(SaveButton)
collidables.append(LoadButton)
collidables.append(ReloadButton)
collidables.append(MakeStickButton)

def changeButtonImage():
    morph = widgetCell.holding
    if morph.__class__ == Button or morph.__class__ == Stick or morph.__class__ == Hat:
        unpressed = morph.unpressed
        num = widgetCell.changelist.index(unpressed)
        if num + 1 < len(widgetCell.changelist):
            num = num+1
        else:
            num = 0
        unpressed = widgetCell.changelist[num]
        prunedex = unpressed.index("unpressed")
        pressed = unpressed[:prunedex] + unpressed[prunedex+2:]
        morph.unpressed = unpressed
        morph.pressed = pressed
        morph.load()

    stickcollidables()

    ###if morph.__class__ == Stick:
        #unpressed = morph.unpressed
        #num = widgetCell.changelist.index(unpressed)
        #if num + 1 < len(widgetCell.changelist):
            #num = num+1
        #else:
            #num = 0
        #unpressed = widgetCell.changelist[num]
        #prunedex = unpressed.index("unpressed")
        #pressed = unpressed[:prunedex] + unpressed[prunedex+2:]
        #morph.pressed = pressed
        #morph.unpressed = unpressed
        #morph.load()###

def rotateButtonImage():
    morph = widgetCell.holding
    morph.Rotate()
    stickcollidables()

ChangeImage = pygame.image.load('assets/changebutton.png')
changebutton = ClickableOptionButton(x+20, y-50, ChangeImage)
changebutton.doclicked = changeButtonImage
RotateImage = pygame.image.load('assets/rotatebutton.png')
rotatebutton = ClickableOptionButton(x+40+135, y-50, RotateImage)
rotatebutton.doclicked = rotateButtonImage
ButtonModList = []
ButtonModList.append(changebutton)
ButtonModList.append(rotatebutton)

horizontalaxis = pygame.image.load('assets/horizontalaxisbutton.png')

changehorizontalbutton = ClickableOptionButton(changebutton.rect.x, changebutton.rect.y-50,horizontalaxis)
def addButtontoController(Core, buttonnum):
    buttonadd = Button(buttonnum ,Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2), ActiveStick)
    buttonadd.Rotate()
    ActiveStick.buttondict[buttonnum] = buttonadd

def addAxistoController(Core, Axisnum):
    axisadd = TriggerAxis(Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2), Axisnum, ActiveStick)
    axisadd.Rotate()
    ActiveStick.axisdict[Axisnum] = axisadd

def changehorizontalaxis(self):
    numswap = self.trigger.axis
    if self.Core.horaxis >= 0:
        temp = self.Core.horaxis
        self.Core.horaxis = numswap
        addAxistoController(self.Core, temp)
    else:
        self.Core.horaxis = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.axisdict:
            tempdict.append(key)
        for item in tempdict:
           if ActiveStick.axisdict[item] == self.trigger:
               del ActiveStick.axisdict[item]
        del tempdict
    stickcollidables()

def changehorizontalclicked():
    action = ModAction(widgetCell.holding, TriggerAxis(),"CLICK DESIRED HORIZONTAL AXIS")
    ModAction.doaction = changehorizontalaxis
    return action
changehorizontalbutton.doclicked = changehorizontalclicked

vertaxis = pygame.image.load('assets/vertaxisbutton.png')

changevertbutton = ClickableOptionButton(rotatebutton.rect.x, changehorizontalbutton.rect.y, vertaxis)
def changevertaxis(self):
    numswap = self.trigger.axis
    if self.Core.vertaxis >= 0:
        temp = self.Core.vertaxis
        self.Core.vertaxis = numswap
        addAxistoController(self.Core, temp)
    else:
        self.Core.vertaxis = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.axisdict:
            tempdict.append(key)
        for item in tempdict:
           if ActiveStick.axisdict[item] == self.trigger:
               del ActiveStick.axisdict[item]
        del tempdict
    stickcollidables()

def changevertclicked():
    action = ModAction(widgetCell.holding, TriggerAxis(),"CLICK DESIRED VERTICAL AXIS")
    ModAction.doaction = changevertaxis
    return action
changevertbutton.doclicked = changevertclicked

changeButtonImage = pygame.image.load('assets/addbutton.png')
changeStickButton = ClickableOptionButton(changevertbutton.rect.x-12, changehorizontalbutton.rect.y-50,changeButtonImage)
def changestickbutton(self):
    numswap = self.trigger.buttonnum
    if self.Core.buttonnum >= 0:
        temp = self.Core.buttonnum
        self.Core.buttonnum = numswap
        addButtontoController(self.Core, temp)
    else:
        self.Core.buttonnum = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.buttondict:
            tempdict.append(key)
        for item in tempdict:
            if ActiveStick.buttondict[item] == self.trigger:
               del ActiveStick.buttondict[item]
    stickcollidables()

def changebuttonclicked():
    action = ModAction(widgetCell.holding, Button(),"CLICK DESIRED BUTTON")
    ModAction.doaction = changestickbutton
    return action
changeStickButton.doclicked = changebuttonclicked

DropSettingsImage = pygame.image.load('assets/dropsettings.png')
detachAllButton = ClickableOptionButton(changeStickButton.rect.x - DropSettingsImage.get_rect().bottomright[0]-10, changeStickButton.rect.y, DropSettingsImage)
def detachAllclicked():
    if widgetCell.holding:
        itemstoadd = widgetCell.holding.dropItems()
    else:
        itemstoadd = []
    for item in itemstoadd:
        if item.__class__ == list:
            for thing in item:
                ActiveStick.axisdict[thing.axis] = thing
        else:
            ActiveStick.buttondict[item.buttonnum] = item

    stickcollidables()
detachAllButton.doclicked = detachAllclicked


StickModList = []
StickModList.append(changebutton)
StickModList.append(rotatebutton)
StickModList.append(changehorizontalbutton)
StickModList.append(changevertbutton)
StickModList.append(changeStickButton)
StickModList.append(detachAllButton)

AxisModList = []
AxisModList.append(rotatebutton)

HatModList = []
HatModList.append(changebutton)


def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    if mousex >= collisionbox[0] and mousex <= collisionbox[0]+collisionbox[2]:
        if mousey >= collisionbox[1] and mousey <= collisionbox[1]+collisionbox[3]:
            return True
    return False

def stickcollidables():
    for item in ActiveStick.buttondict:
        rectangle = ActiveStick.buttondict[item].off.get_rect()
        ActiveStick.buttondict[item].rect = rectangle
        ActiveStick.buttondict[item].rect.x = ActiveStick.buttondict[item].x
        ActiveStick.buttondict[item].rect.y = ActiveStick.buttondict[item].y
        if ActiveStick.buttondict[item] not in collidables:
            collidables.append(ActiveStick.buttondict[item])
    for item in ActiveStick.axisdict:
        rectangle1 = ActiveStick.axisdict[item].bar.get_rect()
        ActiveStick.axisdict[item].rect = rectangle1
        ActiveStick.axisdict[item].rect.x = ActiveStick.axisdict[item].x
        ActiveStick.axisdict[item].rect.y = ActiveStick.axisdict[item].y
        if ActiveStick.axisdict[item] not in collidables:
            collidables.append(ActiveStick.axisdict[item])
    for item in ActiveStick.sticklist:
        rectangle2 = item.stickunpressed.get_rect()
        item.rect = rectangle2
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)

    for item in ActiveStick.hatdict:
        rectangle3 = ActiveStick.hatdict[item].backgroundimage.get_rect()
        ActiveStick.hatdict[item].rect = rectangle3
        ActiveStick.hatdict[item].rect.x = ActiveStick.hatdict[item].x
        ActiveStick.hatdict[item].rect.y = ActiveStick.hatdict[item].y
        if ActiveStick.hatdict[item] not in collidables:
            collidables.append(ActiveStick.hatdict[item])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if ActiveStick == False:
                ActiveStick = LoadGenericController(joysticks[event.instance_id],event.instance_id)
                name = ActiveStick.gamepad.get_name()
                stickcollidables()
                words = ""
                text = font.render(words, True, (200, 74, 220))
            if ActiveStick.gamepad == False:
                if name == joysticks[event.instance_id].get_name():
                    ActiveStick.gamepad = joysticks[event.instance_id]
                    ActiveStick.resetListItems()
                    stickcollidables()
                    words = ""
                    name = ActiveStick.gamepad.get_name()
                    text = font.render(words, True, (200, 74, 220))
                else:
                    ActiveStick = LoadGenericController(joysticks[event.instance_id], event.instance_id)
                    name = ActiveStick.gamepad.get_name()
                    stickcollidables()
                    words = ""
                    text = font.render(words, True, (200, 74, 220))


        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            ID = joy.get_instance_id()
            joysticks[ID] = joy

        if event.type == pygame.JOYDEVICEREMOVED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = event.instance_id
            #ID = ActiveStick.gamepad.get_instance_id()
            if ActiveStick:
                if ActiveStick.gamepad:
                    if ActiveStick.gamepad.get_instance_id() == joy:
                        ActiveStick.gamepad = False
                        words = "PRESS BUTTON"
                        text = font.render(words, True, (200, 74, 220))
            del joysticks[joy]



        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            touch = False

            for i in range(len(collidables)-1,-1,-1):
                item = collidables[i]
                touch = CollisionCheck(position, item.rect)
                if touch:
                    collided = item
                    if collided.__class__ == ClickableOptionButton:
                        check = collided.doclicked()
                        if check.__class__ == GenericController or check.__class__ == LoadGenericController:
                            ActiveStick = check
                            if check.gamepad:
                                name = check.gamepad.get_name()
                                words = ""
                                text = font.render(words, True, (200, 74, 220))
                            else:
                                name = 'unknown'
                            stickcollidables()
                        if check.__class__ == Stick:
                            if ActiveStick:
                                widgetCell.holdItem(check)
                                widgetCell.stopdrag()
                                widgetCell.update()

                                ActiveStick.sticklist.append(check)
                                stickcollidables()
                        if check.__class__ == ModAction:
                            currentAction.action = check
                    elif currentAction.hasAction():
                        currentAction.setTrigger(collided)
                    elif widgetCell.holding == False or widgetCell.holding != collided:
                        widgetCell.holdItem(collided)
                        widgetCell.stopdrag()
                        widgetCell.update()
                    elif widgetCell.holding == collided:
                        widgetCell.dragging = True


                    break
            if touch == False:
                widgetCell.holdItem(False)
                widgetCell.update()

        if event.type == pygame.MOUSEBUTTONUP:
            widgetCell.stopdrag()


    if done:
        break

    if widgetCell.dragging == True:
        position = pygame.mouse.get_pos()
        widgetCell.Drag(position)


    pygame.draw.rect(display,(255,255,255),rect)
    display.blit(text, (20, 20))
    pygame.draw.rect(display, (0, 0, 0), (x - 1, y - 1, width + 2, height + 2))
    display.blit(workrectimage, (x, y))
    SaveButton.draw(display)
    LoadButton.draw(display)
    MakeStickButton.draw(display)
    ReloadButton.draw(display)
    if widgetCell.holding:
        widgetCell.draw(display)

    if ActiveStick:
        font = pygame.font.Font('Zou.ttf', 48)
        active = font.render(str(name).upper(),True,(40,200,60))
        display.blit(active,(20,60))
        ActiveStick.update()
        ActiveStick.draw(display)


    if currentAction.hasAction() != False:
        actiontext = currentAction.action.text
        font = pygame.font.Font('Zou.ttf', 24)
        active = font.render(actiontext,True,(20,20,230))
        display.blit(active,(175,120))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()