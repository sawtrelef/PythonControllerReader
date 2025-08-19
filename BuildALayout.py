import pygame
from joystickstuff import Button, Stick, TriggerAxis
from GenericController import GenericController


pygame.init()

font = pygame.font.Font('Zou.ttf', 48)

pygame.display.set_caption('Build Your Controller Layout')

display = pygame.display.set_mode((600,700))
rect = pygame.rect.Rect(0,0,600,700)
workrect = pygame.rect.Rect(150,350, 400,250)
clock = pygame.time.Clock()

done = False
words = "PRESS BUTTON"
text = font.render(words, True, (200, 74, 220))


drawlist = []

ActiveStick = False
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

collidables = []

def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    if mousex >= collisionbox[0] and mousex <= collisionbox[0]+collisionbox[2]:
        if mousey >= collisionbox[1] and mousey <= collisionbox[1]+collisionbox[3]:
            return True
    return False

selected = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if ActiveStick == False:
                ActiveStick = GenericController(joysticks[event.instance_id],event.instance_id)
                name = joysticks[event.instance_id].get_name()
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

        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            for item in collidables:
                if CollisionCheck(position, item.rect):
                    selected = item
                    print(str(selected))
                else:
                    print("You missed me: " + str(item))
                    print(str(item.rect))
                    print(str(position))

        if event.type == pygame.MOUSEBUTTONUP:
            selected = False
            position = pygame.mouse.get_pos()
            print("Mouse x: " + str(position[0]) + " Mouse y: " + str(position[1]))
            print("I dropped it")


    if done:
        break

    if selected:
        position = pygame.mouse.get_pos()
        selected.x = position[0]
        selected.rect.x = position[0]
        selected.y = position[1]
        selected.rect.y = position[1]

    pygame.draw.rect(display,(255,255,255),rect)
    display.blit(text, (20, 20))
    pygame.draw.rect(display,(0,0,0), workrect)

    if ActiveStick:
        font = pygame.font.Font('Zou.ttf', 48)
        active = font.render(str(name).upper(),True,(40,200,60))
        display.blit(active,(20,60))
        ActiveStick.update()
        ActiveStick.draw(display)






    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()