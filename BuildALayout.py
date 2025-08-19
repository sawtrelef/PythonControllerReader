import pygame
from joystickstuff import Button, Stick, TriggerAxis
from GenericController import GenericController


pygame.init()

font = pygame.font.Font('Zou.ttf', 48)

pygame.display.set_caption('Build Your Controller Layout')

display = pygame.display.set_mode((600,700))
rect = pygame.rect.Rect(0,0,600,700)
clock = pygame.time.Clock()

done = False
words = "PRESS BUTTON"
text = font.render(words, True, (200, 74, 220))


drawlist = []

ActiveStick = False
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if ActiveStick == False:
                ActiveStick = GenericController(joysticks[event.instance_id],event.instance_id)
                name = joysticks[event.instance_id].get_name()
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
    if done:
        break
    pygame.draw.rect(display,(255,255,255),rect)
    display.blit(text, (20, 20))
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