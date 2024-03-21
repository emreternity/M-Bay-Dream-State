# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
idleDir = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def redrawCharMove():
    global walkCount
    if walkCount + 1 >= 9:
        walkCount = 0
    if left:
        screen.blit(charleft[walkCount//3], player_pos)
        walkCount += 1
    elif right:
        screen.blit(charright[walkCount//3], player_pos)
        walkCount += 1
    elif up:
        screen.blit(charup[walkCount//3], player_pos)
        walkCount += 1
    elif down:
        screen.blit(chardown[walkCount//3], player_pos)
        walkCount += 1
    else:
        if idleDir == 1:
            screen.blit(charup[0],player_pos)
        elif idleDir == 2:
            screen.blit(charright[0],player_pos)
        elif idleDir == 3:
            screen.blit(chardown[0],player_pos)
        elif idleDir == 4:
            screen.blit(charleft[0],player_pos)
        else:
            screen.blit(char,player_pos)
    pygame.display.update()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    clock = pygame.time.Clock()
    clock.tick(60)

    char = pygame.image.load('img\char\WillieIdle.png')
    
    chardown = [pygame.image.load('img\char\WillieIdle.png'),pygame.image.load('img\char\Willie1.png'),pygame.image.load('img\char\Willie2.png')]
    charright = [pygame.image.load('img\char\Willie-yan1.png'),pygame.image.load('img\char\Willie-yan2.png'),pygame.image.load('img\char\Willie-yan4.png')]
    charleft = [pygame.image.load('img\char\Willie-sol-yan1.png'),pygame.image.load('img\char\Willie-sol-yan2.png'),pygame.image.load('img\char\Willie-sol-yan4.png')]
    charup = [pygame.image.load('img\char\willie-arka-sonn.png'),pygame.image.load('img\char\willie-arka-sonn.png'),pygame.image.load('img\char\willie-arka-sonn.png')]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
        up = True    
        left = False
        right = False
        down = False
        idleDir = 1
    elif keys[pygame.K_s]:
        player_pos.y += 300 * dt
        down = True
        left = False
        right = False
        up = False
        idleDir = 3
    elif keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        left = True
        down = False
        right = False
        up = False
        idleDir = 4
    elif keys[pygame.K_d]:
        right = True
        up = False
        left = False
        down = False
        idleDir = 2
        player_pos.x += 300 * dt
    else:
        up = False
        down = False
        right = False
        left = False
        walkCount = 0
    redrawCharMove()
        

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()