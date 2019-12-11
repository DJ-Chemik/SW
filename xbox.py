import pygame

# buttons
A = 0
B = 1
X = 2
Y = 3

pygame.init()
clock = pygame.time.Clock()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Detected joystick " + str(joystick.get_name()))

gameExit = False

while not gameExit:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == A:
                print("Wonsz idzie w dol")
            elif event.button == B:
                print("Wonsz idzie w prawo")
            elif event.button == X:
                print("Wonsz idzie w lewo")
            elif event.button == Y:
                print("Wonsz idzie w gore")

pygame.quit()
