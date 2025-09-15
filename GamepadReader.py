import pygame
from PS5Controller import PlayStation5Controller
from joystickstuff import Button, TriggerAxis, Stick, Hat
from GenericController import GenericController
from ClickableOptionButton import ClickableOptionButton

pygame.init()
joysticks = {}
for i in range (pygame.joystick.get_count()):
    joysticks[i] = pygame.joystick.Joystick(i)
font = pygame.font.Font('Zou.ttf', 32)
background = pygame.image.load("assets/Background.png")
rect = background.get_rect()
x = int(rect.bottomright[0])
y = int(rect.bottomright[1])
pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((x,y+24))
clock = pygame.time.Clock()

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

    def resetCounter(self):
        self.actionperminute = 0
        self.timepassed = 0

controller = False

def load(filename = ""):
    if filename == "":
        filename = "layout.txt"
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
            addbutton = Button(buttonnum, xpos, ypos)
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
            if flipbool == 'True':
                flipbool = True
            else:
                flipbool = False
            addtrigger = TriggerAxis(xpos, ypos, axisnum, False, mode, rotate)
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
            # stick creation data format
            # (xpos,ypos,vertaxis, horizontalaxis, buttonnumber)
            addstick = Stick(xpos, ypos, vertaxis, horizontalaxis, buttonnumber)
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

            addhat = Hat(hatnum, xpos, ypos)
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

controller = load("layout.txt")
controller.resetListItems()
counter = APMCounter(controller)

def Reset():
        counter.resetCounter()
        controller.resetCounter()
        return 0

def ToggleLines():
    controller.StickLines = not controller.StickLines

resetimage = pygame.image.load('./assets/resetbutton.png')
resetrect = resetimage.get_rect()
ResetButton = ClickableOptionButton(1, y-resetrect.bottomright[1]-1+24,resetimage)
ResetButton.doclicked = Reset

linetoggleimage = pygame.image.load('./assets/linesbutton.png')
linerect = linetoggleimage.get_rect()
LineToggleButton = ClickableOptionButton(x-linerect.bottomright[0], y - linerect.bottomright[1]-1+24,linetoggleimage)
LineToggleButton.doclicked = ToggleLines

collidables = []
collidables.append(ResetButton)
collidables.append(LineToggleButton)
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

                for i in range(len(collidables) - 1, -1, -1):
                    item = collidables[i]
                    touch = CollisionCheck(position, item.rect)
                    if touch:
                        collided = item
                        if collided.__class__ == ClickableOptionButton:
                            check = collided.doclicked()

        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            ID = joy.get_instance_id()
            joysticks[ID] = joy
            if controller:
                if controller.gamepad == False:
                    controller.gamepad = joysticks[ID]

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
    controller.draw(display)
    counter.draw(display)
    ResetButton.draw(display)
    LineToggleButton.draw(display)


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()