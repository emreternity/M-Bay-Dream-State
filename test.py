# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
pygame.display.set_caption("M-Bay: Dream State Prototip 1")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
idleDir = 0
velchar = 300
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
char = pygame.image.load('img\char\WillieIdle.png')
rect_char = pygame.Rect(0,0,100,100)
npc = pygame.image.load('img\char\Lisa1.png')
door = pygame.image.load('img\obj\door.png')
door = pygame.transform.scale(door,(120,170))
rect_door = pygame.Rect(0,0,140,190)
rect_door.top = 140
rect_door.left = 790
rect_doorstop = pygame.Rect(0,0,140,95)
rect_doorstop.top = 140
rect_doorstop.left = 790
rect_npc = pygame.Rect(0,0,20,20)
rect_npc.x = 360
rect_npc.y = 210
rect_npcreact = pygame.Rect(0,0,150,150)
rect_npcreact.x = 290
rect_npcreact.y = 200
isGamePaused = False
    
chardown = [pygame.image.load('img\char\WillieIdle.png'),pygame.image.load('img\char\Willie1.png'),pygame.image.load('img\char\Willie2.png')]
charright = [pygame.image.load('img\char\Willie-yan1.png'),pygame.image.load('img\char\Willie-yan2.png'),pygame.image.load('img\char\Willie-yan4.png')]
charleft = [pygame.image.load('img\char\Willie-sol-yan1.png'),pygame.image.load('img\char\Willie-sol-yan2.png'),pygame.image.load('img\char\Willie-sol-yan4.png')]
charup = [pygame.image.load('img\char\willie-arka-sonn.png'),pygame.image.load('img\char\willie-arka-sonn.png'),pygame.image.load('img\char\willie-arka-sonn.png')]

font = pygame.font.Font('freesansbold.ttf',24)

snip = font.render('', True, 'white')
txtnpccounter = 0
txtnpcspeed = 2
txtnpcdone = False
txtnpcactivemsg = 0
txtdoorcounter = 0
txtdoorspeed = 2
txtdoordone = False

# def startLockpickMinigame():

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

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
    rect_char.x = (player_pos.x + 15)
    rect_char.y = (player_pos.y + 15)
    pygame.display.update()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and isGamePaused == False:
                isGamePaused = True
            elif event.key == pygame.K_ESCAPE and isGamePaused == True:
                isGamePaused = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and txtnpcdone and txtnpcactivemsg < len(messages)-1:
                    txtnpcactivemsg += 1
                    done = False
                    message = messages[txtnpcactivemsg]
                    txtnpccounter = 0
                elif event.key == pygame.K_RETURN and txtnpcdone and txtnpcactivemsg == len(messages)-1:
                    txtnpcactivemsg = 0
                    txtnpccounter = 0
                    message = messages[txtnpcactivemsg]
                    done = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    clock = pygame.time.Clock()
    clock.tick(60)
    if isGamePaused == False:
        screen.blit(npc,(300,200))
        screen.blit (door,(800,150))
        draw_rect_alpha(screen,(0, 0, 255, 0),rect_char)
        draw_rect_alpha(screen,(1,1,1, 0),rect_npc)
        draw_rect_alpha(screen,(1,1,1, 0),rect_npcreact)
        draw_rect_alpha(screen,(1,1,1,0),rect_door)
        draw_rect_alpha(screen,(30,30,30,0),rect_doorstop)

        if rect_char.colliderect(rect_npc) or rect_char.colliderect(rect_doorstop):
            velchar = 0
            if left:
                player_pos.x += 5
            elif right:
                player_pos.x -= 5
            elif up:
                player_pos.y += 5
            elif down:
                player_pos.y -= 5
            up = False
            down = False
            right = False
            left = False
            walkCount = 0
            velchar = 300

        if rect_char.colliderect(rect_door):
            pygame.draw.rect(screen,'black',[0 , 520, 1280, 200])
            message = 'Lockpick denemek için Enter tuşuna bas!'
            if txtdoorcounter < txtdoorspeed * len(message):
                txtdoorcounter += 1
            elif txtdoorcounter >= txtdoorspeed * len(message):
                txtdoordone = True
            snip = font.render(message[0:txtdoorcounter//txtdoorspeed], True, 'white')
            screen.blit(snip, (10, 540))
            # if keys[pygame.K_RETURN]:
            #     startLockpickMinigame()
        if rect_char.colliderect(rect_npcreact):
            messages = ['Hey! Ben Lisa. Bu cümlem ise yazı motorunun test mesajı. Enter tuşuna bas!',
                       'İşte, konuşmaya devam ediyorum! ESC tuşuna basmaya ne dersin?',
                       'Adamım, harikasın ya! Tekrar Enter\'a basarsan baştan alırız.']
            message = messages[txtnpcactivemsg]
            pygame.draw.rect(screen,'black',[0 , 520, 1280, 200])
            if txtnpccounter < txtnpcspeed * len(message):
                txtnpccounter += 1
            elif txtnpccounter >= txtnpcspeed * len(message):
                txtnpcdone = True
            snip = font.render(message[0:txtnpccounter//txtnpcspeed], True, 'white')
            screen.blit(snip, (10, 540))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= velchar * dt
            up = True    
            left = False
            right = False
            down = False
            idleDir = 1
        elif keys[pygame.K_s]:
            player_pos.y += velchar * dt
            down = True
            left = False
            right = False
            up = False
            idleDir = 3
        elif keys[pygame.K_a]:
            player_pos.x -= velchar * dt
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
            player_pos.x += velchar * dt
        else:
            up = False
            down = False
            right = False
            left = False
            walkCount = 0
        redrawCharMove()
    else:
        screen.fill("black")
        message = 'Oyun durduruldu. Devam etmek istiyorsan tekrar ESC tuşuna bas.'
        snip = font.render(message, True, 'white')
        screen.blit(snip, (30, 640/2))
        

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()