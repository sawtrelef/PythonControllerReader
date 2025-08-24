import pygame
from os import listdir
from joystickstuff import Button, Stick, TriggerAxis
from GenericController import LoadGenericController, GenericController



pygame.init()

font = pygame.font.Font('Zou.ttf', 48)

pygame.display.set_caption('Build Your Controller Layout')
workrectimage = pygame.image.load('Background.png')
workrect = workrectimage.get_rect()
width = workrect.bottomright[0]
height = workrect.bottomright[1]
display = pygame.display.set_mode((600,700))
rect = pygame.rect.Rect(0,0,600,700)

x = 150
y = 350
clock = pygame.time.Clock()

done = False
words = "PRESS BUTTON"
text = font.render(words, True, (200, 74, 220))


drawlist = []

ActiveStick = False
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

collidables = []

class button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, WINDOW, rect=False, transform=False):
        WINDOW.blit(self.image, self.rect)

    # MAKE MORE GENERIC, WILL NEVER NEED A CLICKABLE BUTTON FOR DRAWING CARD, THIS WAS WRITTEN FOR TESTING PURPOSES ONLY
    def doclicked(self):
        return False

    def setImage(self, image):
        self.image = image

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
            onimage = str(button.onimagename)
            offimage = str(button.offimagename)
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
            xpos = str(axis.x-150)
            ypos = str(axis.y-350)
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
            xpos = str(stick.x-150)
            ypos = str(stick.y-350)
            pressed = str(stick.pressed)
            unpressed = str(stick.unpressed)
            sticktext = "({},{},{},{},{},{},{})\n".format(vertaxis,horizontal,button,xpos,ypos,pressed,unpressed)
            print(sticktext)
            file.write(sticktext)
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
            xpos = int(values[1])+150
            ypos = int(values[2])+350
            offimage = str(values[3])
            onimage = str(values[4])
            rotation = int(values[5])
            addbutton = Button(buttonnum,xpos,ypos)
            addbutton.offimagename = offimage
            addbutton.onimagename = onimage
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
            xpos = int(values[1])+150
            ypos = int(values[2])+350
            triggerimage = str(values[3])
            paddleimage = str(values[4])
            flipbool = bool(values[5])
            addtrigger = TriggerAxis(axisnum, xpos, ypos)
            addtrigger.paddleimage = paddleimage
            addtrigger.barimage = triggerimage
            addtrigger.load()
            if flipbool:
                addtrigger.horizontal = flipbool
                addtrigger.flip()
            addtrigger.horizontal = flipbool
            axislist.append(addtrigger)

    sticklist = []
    for i in range(bookmarks[2], length):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            # (vertaxis,horizontalaxis,xpos, ypos, buttonnum, pressed, unpressed)
            values = lines[i].split(',')
            vertaxis = int(values[0])
            horizontalaxis = int(values[1])
            xpos = int(values[2])+150
            ypos = int(values[3])+350
            buttonnumber = int(values[4])
            onimage = values[5]
            offimage = values[6]
            addstick = Stick(xpos,ypos,vertaxis,horizontalaxis,buttonnumber)
            addstick.pressed = onimage
            addstick.unpressed = offimage
            addstick.load()
            sticklist.append(addstick)

    Controller = False
    if ActiveStick:
        Controller = GenericController(ActiveStick.ID)
        Controller.buttonlist = buttonlist
        Controller.axislist = axislist
        Controller.sticklist = sticklist
    else:
        Controller = GenericController(0)
        Controller.buttonlist = buttonlist
        Controller.axislist = axislist
        Controller.sticklist = sticklist
    file.close()
    if Controller:
        return Controller
    return False

saveimage = pygame.image.load('savebutton.png')
loadimage = pygame.image.load('loadbutton.png')
makestickimage = pygame.image.load('makestickbutton.png')
MakeStickButton = button(290,655, makestickimage)
SaveButton = button(370,610,saveimage)
LoadButton = button(210, 610,loadimage)
SaveButton.doclicked = save
LoadButton.doclicked = load

collidables.append(SaveButton)
collidables.append(LoadButton)
collidables.append(MakeStickButton)


def changeButtonImage():
    morph = widgetCell.holding
    if morph.__class__ == Button:
        unpressed = morph.offimagename
        num = widgetCell.changelist.index(unpressed)
        if num + 1 < len(widgetCell.changelist):
            num = num+1
        else:
            num = 0
        unpressed = widgetCell.changelist[num]
        prunedex = unpressed.index("unpressed")
        pressed = unpressed[:prunedex] + unpressed[prunedex+2:]
        morph.offimagename = unpressed
        morph.onimagename = pressed
        morph.load()

    if morph.__class__ == Stick:
        unpressed = morph.offimagename
        num = widgetCell.changelist.index(unpressed)
        if num + 1 < len(widgetCell.changelist):
            num = num+1
        else:
            num = 0
        unpressed = widgetCell.changelist[num]
        prunedex = unpressed.index("unpressed")
        pressed = unpressed[:prunedex] + unpressed[prunedex+2:]
        morph.pressed = unpressed
        morph.unpressed = pressed
        morph.load()

def rotateButtonImage():

    morph = widgetCell.holding
    morph.rotate = morph.rotate+90
    morph.load()



ChangeImage = pygame.image.load('changebutton.png')
changebutton = button(x+20, y-50, ChangeImage)
changebutton.doclicked = changeButtonImage
RotateImage = pygame.image.load('rotatebutton.png')
rotatebutton = button(x+40+135, y-50, RotateImage)
rotatebutton.doclicked = rotateButtonImage
ButtonModList = []
ButtonModList.append(changebutton)
ButtonModList.append(rotatebutton)

def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    if mousex >= collisionbox[0] and mousex <= collisionbox[0]+collisionbox[2]:
        if mousey >= collisionbox[1] and mousey <= collisionbox[1]+collisionbox[3]:
            return True
    return False

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
        self.holding.x = position[0]
        self.holding.rect.x = position[0]
        self.holding.y = position[1]
        self.holding.rect.y = position[1]

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

        for item in self.buttonlist:
            collidables.append(item)


    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)
        return

widgetCell = HoldingCell()

def stickcollidables():
    for item in ActiveStick.buttonlist:
        rectangle = item.off.get_rect()
        item.rect = rectangle
        item.rect.x = item.x
        item.rect.y = item.y
        collidables.append(item)
    for item in ActiveStick.axislist:
        rectangle1 = item.bar.get_rect()
        item.rect = rectangle1
        item.rect.x = item.x
        item.rect.y = item.y
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
            for item in collidables:
                touch = CollisionCheck(position, item.rect)
                if touch:
                    collided = item
                    if collided.__class__ == button:
                        check = collided.doclicked()
                        if check.__class__ == GenericController:
                            ActiveStick = check
                            if len(joysticks) > 0:
                                name = joysticks[check.ID].get_name()
                            else:
                                name = 'unknown'
                            stickcollidables()
                    else:
                        selectedbutton = collided
                        print(str(selectedbutton))
                        widgetCell.holdItem(selectedbutton)
                        widgetCell.update()
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
    display.blit(workrectimage, (x, y))
    SaveButton.draw(display)
    LoadButton.draw(display)
    MakeStickButton.draw(display)
    if ActiveStick:
        font = pygame.font.Font('Zou.ttf', 48)
        active = font.render(str(name).upper(),True,(40,200,60))
        display.blit(active,(20,60))
        ActiveStick.update()
        ActiveStick.draw(display)

    if widgetCell.holding:
        widgetCell.draw(display)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()