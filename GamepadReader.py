import pygame
from PS5Controller import PlayStation5Controller
from joystickstuff import Button, TriggerAxis, Stick, Hat
from GenericController import GenericController

pygame.init()

font = pygame.font.Font('Zou.ttf', 32)
background = pygame.image.load("assets/Background.png")
rect = background.get_rect()
x = int(rect.bottomright[0])
y = int(rect.bottomright[1])
pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((x,y))
clock = pygame.time.Clock()
#font = pygame.font.Font('c:/Windows/Fonts/Arial.ttf', 24)

controller = False




class APMCounter():
    value = 0
    timepassed = 0
    actionperminute = 0
    def __init__(self,target):
        self.ValueTarget = target

    def update(self):
        self.value = self.ValueTarget.getcount()
        self.timepassed = self.timepassed + 1
        self.actionperminute = int(self.value / (self.timepassed / 3600))

    def draw(self, WINDOW):
        text = font.render('APM : ' + str(self.actionperminute), True, (149, 75, 220))
        WINDOW.blit(text, (int(x/2)-45, y-35))

def load(filename = ""):
    if filename == "":
        filename = "layout.txt"
    file = open(filename, 'r')

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
            xpos = int(values[1])
            ypos = int(values[2])
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
            xpos = int(values[1])
            ypos = int(values[2])
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
            xpos = int(values[3])
            ypos = int(values[4])
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
            xpos = int(values[1])
            ypos = int(values[2])
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

    if controller:
        Controller = GenericController(controller.ID)
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

#controller = PlayStation5Controller(0)
controller = load("layout.txt")
counter = APMCounter(controller)
done = False
while not done:

    eventlist = pygame.event.get()
    for event in eventlist:
        if event.type == pygame.QUIT:
            done = True
    if done:

        break

    controller.update()
    counter.update()
    display.blit(background, (0,0))
    controller.draw(display)
    counter.draw(display)


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()