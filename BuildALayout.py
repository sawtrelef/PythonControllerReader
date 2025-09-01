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
text = font.render(words, True, (200, 74, 220))

drawlist = []
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
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
        buttonlist = ActiveStick.buttonlist
        length = len(buttonlist)
        print("Number of Independent buttons: " + str(length) + '\n')
        file.write("Number of Independent buttons: " + str(length) + '\n')
        for button in buttonlist:
            #(buttonnum, x, y, offimage, onimage, rotation)
            number = str(button.buttonnum)
            xposition = str(button.x-x)
            yposition = str(button.y-y)
            onimage = str(button.pressed)
            offimage = str(button.unpressed)
            rotation = str(button.rotate)
            buttontext = "({},{},{},{},{},{})\n".format(number,xposition,yposition, offimage,onimage,rotation)
            print(buttontext)
            file.write(buttontext)
        axislist = ActiveStick.axislist
        length = len(axislist)
        print("Number of Independent Axis: " + str(length) + '\n')
        file.write("Number of Independent Axis: " + str(length) + '\n')
        for axis in axislist:
            #(axisnumber, xpos, ypos, barimage, paddleimage, flippedbool)
            number = str(axis.axis)
            xpos = str(axis.x-x)
            ypos = str(axis.y-y)
            barim = str(axis.barimage)
            paddleim = str(axis.paddleimage)
            flip = str(axis.horizontal)
            axistext = "({},{},{},{},{},{})\n".format(number,xpos,ypos,barim,paddleim,flip)
            print(axistext)
            file.write(axistext)
        sticklist = ActiveStick.sticklist
        length = len(sticklist)
        print("Number of Sticks: " + str(length) + '\n')
        file.write("Number of Sticks: " + str(length) + '\n')
        for stick in ActiveStick.sticklist:
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
        hatlist = ActiveStick.hatlist
        length = len(hatlist)
        print("Number of Hats: " + str(length) + '\n')
        file.write("Number of Hats: " + str(length) + '\n')
        for hat in ActiveStick.hatlist:
            # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            number = str(hat.hatnumber)
            xposition = str(hat.x - x)
            yposition = str(hat.y - y)
            onimage = str(hat.pressed)
            offimage = str(hat.unpressed)
            backgroundimage = str(hat.background)
            rotation = str(hat.rotate)
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
    collidables = [SaveButton, LoadButton]

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

    buttonlist = []
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
            buttonlist.append(addbutton)

    axislist = []
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
            axislist.append(addtrigger)

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
    hatlist = []
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
            hatlist.append(addhat)

    controller = False
    if ActiveStick:
        Controller = GenericController(ActiveStick.ID)
        Controller.buttonlist = buttonlist
        Controller.axislist = axislist
        Controller.sticklist = sticklist
        Controller.hatlist = hatlist
    else:
        Controller = GenericController(0)
        Controller.buttonlist = buttonlist
        Controller.axislist = axislist
        Controller.sticklist = sticklist
        Controller.hatlist = hatlist
    file.close()
    if Controller:
        return Controller
    return False

def makeStick():
    emptystick = Stick(MakeStickButton.rect.x + 145, MakeStickButton.rect.y)
    return emptystick

saveimage = pygame.image.load('assets/savebutton.png')
loadimage = pygame.image.load('assets/loadbutton.png')
makestickimage = pygame.image.load('assets/makestickbutton.png')

SaveButton = ClickableOptionButton((x + width)/2-(saveimage.get_rect().bottomright[0])/2,y + height + 20,saveimage)
LoadButton = ClickableOptionButton(SaveButton.rect.x + 145, SaveButton.rect.y,loadimage)
MakeStickButton = ClickableOptionButton(SaveButton.rect.x +(LoadButton.rect.x - SaveButton.rect.x)/2,SaveButton.rect.y + 50, makestickimage)
SaveButton.doclicked = save
LoadButton.doclicked = load
MakeStickButton.doclicked = makeStick

collidables.append(SaveButton)
collidables.append(LoadButton)
collidables.append(MakeStickButton)

def changeButtonImage():
    morph = widgetCell.holding
    if morph.__class__ == Button or morph.__class__ == Stick:
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
    axisadd = Button(buttonnum ,Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2))
    axisadd.Rotate()
    ActiveStick.buttonlist.append(axisadd)

def addAxistoController(Core, Axisnum):
    axisadd = TriggerAxis(Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2), Axisnum)
    axisadd.Rotate()
    ActiveStick.axislist.append(axisadd)

def changehorizontalaxis(self):
    numswap = self.trigger.axis
    if self.Core.horaxis >= 0:
        temp = self.Core.horaxis
        self.Core.horaxis = numswap
        addAxistoController(self.Core, temp)
    else:
        self.Core.horaxis = numswap
    if ActiveStick:
       for item in ActiveStick.axislist:
           if item == self.trigger:
               ActiveStick.axislist.remove(item)
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
       for item in ActiveStick.axislist:
           if item == self.trigger:
               ActiveStick.axislist.remove(item)
    stickcollidables()

def changevertclicked():
    action = ModAction(widgetCell.holding, TriggerAxis(),"CLICK DESIRED VERTICAL AXIS")
    ModAction.doaction = changevertaxis
    return action
changevertbutton.doclicked = changevertclicked

changeButtonImage = pygame.image.load('assets/addbutton.png')
changeButton = ClickableOptionButton(changevertbutton.rect.x-12, changehorizontalbutton.rect.y-50,changeButtonImage)
def changestickbutton(self):
    numswap = self.trigger.buttonnum
    if self.Core.buttonnum >= 0:
        temp = self.Core.buttonnum
        self.Core.buttonnum = numswap
        addButtontoController(self.Core, temp)
    else:
        self.Core.buttonnum = numswap
    if ActiveStick:
       for item in ActiveStick.buttonlist:
           if item == self.trigger:
               ActiveStick.buttonlist.remove(item)
    stickcollidables()

def changebuttonclicked():
    action = ModAction(widgetCell.holding, Button(),"CLICK DESIRED BUTTON")
    ModAction.doaction = changestickbutton
    return action
changeButton.doclicked = changebuttonclicked

DropSettingsImage = pygame.image.load('assets/dropsettings.png')
detachAllButton = ClickableOptionButton(changeButton.rect.x - DropSettingsImage.get_rect().bottomright[0]-10, changeButton.rect.y, DropSettingsImage)
def detachAllclicked():
    if widgetCell.holding:
        itemstoadd = widgetCell.holding.dropItems()
    else:
        itemstoadd = []
    for item in itemstoadd:
        if item.__class__ == list:
            for thing in item:
                ActiveStick.axislist.append(thing)
        else:
            ActiveStick.buttonlist.append(item)

    stickcollidables()
detachAllButton.doclicked = detachAllclicked


StickModList = []
StickModList.append(changebutton)
StickModList.append(rotatebutton)
StickModList.append(changehorizontalbutton)
StickModList.append(changevertbutton)
StickModList.append(changeButton)
StickModList.append(detachAllButton)

AxisModList = []
AxisModList.append(rotatebutton)

def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    if mousex >= collisionbox[0] and mousex <= collisionbox[0]+collisionbox[2]:
        if mousey >= collisionbox[1] and mousey <= collisionbox[1]+collisionbox[3]:
            return True
    return False

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        return

def stickcollidables():
    for item in ActiveStick.buttonlist:
        rectangle = item.off.get_rect()
        item.rect = rectangle
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)
    for item in ActiveStick.axislist:
        rectangle1 = item.bar.get_rect()
        item.rect = rectangle1
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)
    for item in ActiveStick.sticklist:
        rectangle2 = item.stickunpressed.get_rect()
        item.rect = rectangle2
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)

    for item in ActiveStick.hatlist:
        rectangle3 = item.backgroundimage.get_rect()
        item.rect = rectangle3
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if ActiveStick == False:
                ActiveStick = LoadGenericController(joysticks[event.instance_id],event.instance_id)
                name = joysticks[event.instance_id].get_name()
                stickcollidables()

        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy

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
                        if check.__class__ == GenericController:
                            ActiveStick = check
                            if len(joysticks) > 0:
                                name = joysticks[check.ID].get_name()
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