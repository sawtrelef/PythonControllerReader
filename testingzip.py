from zipfile import ZipFile
from joystickstuff import Button, Stick, TriggerAxis, Hat
from GenericController import GenericController
from pygame import image, transform

filename = 'TestZip.zip'

with ZipFile(filename) as zf:
    for file in zf.namelist():
        if not file.endswith('.png'): # optional filtering by filetype
            continue
        with zf.open(file) as f:
            print(file)
            #image = pygame.image.load(f, namehint=file)

with ZipFile(filename, 'r') as zf:
    folder = filename[:-4]
    with zf.open(folder+'/layout.txt') as layout:
        print('peepus poopus')
        lines = layout.readlines()
        bookmarks = []
        length = len(lines)
        ## removes the newline character from the end of each line
        for i in range(length):
            lines[i] = lines[i].decode().removesuffix('\r\n')
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
                offimage = str(values[3]).removeprefix('.')
                onimage = str(values[4]).removeprefix('.')
                rotation = int(values[5])
                name = ""
                if 6 < len(values):
                    name = str(values[6])
                addbutton = Button(buttonnum, xpos, ypos, False, name)
                #addbutton.unpressed = offimage
                offimagename = folder+offimage
                onimagename = folder+onimage
                with zf.open(offimagename) as f:
                    off = image.load(f)
                #addbutton.pressed = onimage
                with zf.open(onimagename) as f:
                    on = image.load(f)
                off = transform.rotate(off,rotation)
                on = transform.rotate(on, rotation)
                addbutton.on = on
                addbutton.off = off
                addbutton.rotate = rotation
                #addbutton.load()
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

                paddleimagename = folder+paddleimage.removeprefix('.')
                triggerimagename = folder+triggerimage.removeprefix('.')
                with zf.open(paddleimagename) as f:
                    paddle = image.load(f)
                with zf.open(triggerimagename) as f:
                    bar = image.load(f)
                if flipbool == True:
                    paddle = transform.rotate(paddle,90)
                    bar = transform.rotate(bar,90)
                addtrigger.paddle = paddle
                addtrigger.bar = bar

                #addtrigger.paddleimage = paddleimage
                #addtrigger.barimage = triggerimage
                addtrigger.horizontal = flipbool
                #addtrigger.load()
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
                addstick = Stick(xpos, ypos, vertaxis, horizontalaxis, buttonnumber, stickname, buttonname)

                offimagename = folder + offimage.removeprefix('.')
                onimagename = folder + onimage.removeprefix('.')
                with zf.open(offimagename) as f:
                    off = image.load(f)
                # addbutton.pressed = onimage
                with zf.open(onimagename) as f:
                    on = image.load(f)
                off = transform.rotate(off, rotation)
                on = transform.rotate(on, rotation)
                addstick.stickunpressed = off
                addstick.stickpressed = on

                #addstick.pressed = onimage
                #addstick.unpressed = offimage
                #addstick.load()
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

                offimagename = folder + offimage
                onimagename = folder + onimage
                backgroundimagename = folder + backgroundimagename.removeprefix(".")
                with zf.open(offimagename) as f:
                    off = image.load(f)
                # addbutton.pressed = onimage
                with zf.open(onimagename) as f:
                    on = image.load(f)
                with zf.open(backgroundimagename) as f:
                    bg = image.load(f)
                off = transform.rotate(off, rotation)
                on = transform.rotate(on, rotation)
                bg = transform.rotate(bg, rotation)
                addhat.pressed = on
                addhat.unpressed = off
                addhat.backgroundimage = bg
                #addhat.unpressed = offimage
                #addhat.pressed = onimage
                #addhat.background = backgroundimage
                #addhat.rotate = rotation
                #addhat.load()
                hatdict[hatnum] = addhat

        Controller = GenericController(False)
        Controller.buttondict = buttondict
        Controller.axisdict = axisdict
        Controller.sticklist = sticklist
        Controller.hatdict = hatdict
        Controller.resetListItems()
    #return Controller





print('yo waddup')
print('we done here')