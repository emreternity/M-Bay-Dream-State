# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
pygame.mixer.init()
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
rect_door = pygame.Rect(0,0,130,100)
rect_door.top = 0
rect_door.left = 610
rect_doorstop = pygame.Rect(0,0,200,75)
rect_doorstop.top = 0
rect_doorstop.left = 570
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
charup = [pygame.image.load('img\char\williearka1.png'),pygame.image.load('img\char\williearka2.png'),pygame.image.load('img\char\williearka3.png')]
charwalkongrass = [pygame.mixer.Sound('sfx\player\walk1.mp3'),pygame.mixer.Sound('sfx\player\walk2.mp3'),pygame.mixer.Sound('sfx\player\walk3.mp3'),pygame.mixer.Sound('sfx\player\walk4.mp3'),pygame.mixer.Sound('sfx\player\walk5.mp3'),pygame.mixer.Sound('sfx\player\walk6.mp3'),pygame.mixer.Sound('sfx\player\walk7.mp3')]
font = pygame.font.Font('freesansbold.ttf',24)
escmenusfx = pygame.mixer.Sound('sfx\enpc\dialogueblip.mp3')
lisatalksfx = [pygame.mixer.Sound('sfx\enpc\lisatalk1.mp3'),pygame.mixer.Sound('sfx\enpc\lisatalk2.mp3')]
act0song = pygame.mixer.Sound('sfx\embience\eact0routine.mp3')

bg = pygame.image.load('img\proto1\proto1.png').convert()

snip = font.render('', True, 'white')
txtnpccounter = 0
txtnpcspeed = 2
txtnpcdone = False
txtnpcactivemsg = 0
txtdoorcounter = 0
txtdoorspeed = 2
txtdoordone = False
walksfxCounter = 10
blipcounter = 0
songcounter = 0

pygame.mixer.music.load('sfx\embience\proto1ambience.mp3')
pygame.mixer.music.play(-1)

# def startLockpickMinigame():

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def redrawCharMove():
    global walkCount
    global walksfxCounter
    if walkCount + 1 >= 9:
        walkCount = 0
    if left:
        if walksfxCounter == 10:
            walksfxCounter = 0
            pygame.mixer.Sound.play(charwalkongrass[random.randint(0,6)])
        else:
            walksfxCounter += 1
        screen.blit(charleft[walkCount//3], player_pos)
        walkCount += 1
    elif right:
        if walksfxCounter == 10:
            walksfxCounter = 0
            pygame.mixer.Sound.play(charwalkongrass[random.randint(0,6)])
        else:
            walksfxCounter += 1   
        screen.blit(charright[walkCount//3], player_pos)
        walkCount += 1
    elif up:
        if walksfxCounter == 10:
            walksfxCounter = 0
            pygame.mixer.Sound.play(charwalkongrass[random.randint(0,6)])
        else:
            walksfxCounter += 1
        screen.blit(charup[walkCount//3], player_pos)
        walkCount += 1
    elif down:
        if walksfxCounter == 10:
            walksfxCounter = 0
            pygame.mixer.Sound.play(charwalkongrass[random.randint(0,6)])
        else:
            walksfxCounter += 1
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
                pygame.mixer.Sound.play(escmenusfx)
            elif event.key == pygame.K_ESCAPE and isGamePaused == True:
                isGamePaused = False
                pygame.mixer.Sound.play(escmenusfx)
            if event.key == pygame.K_RETURN and txtnpcdone and txtnpcactivemsg < len(messages)-1 and rect_char.colliderect(rect_npcreact):
                txtnpcactivemsg += 1
                done = False
                message = messages[txtnpcactivemsg]
                txtnpccounter = 0
                pygame.mixer.Sound.play(lisatalksfx[random.randint(0,1)])
            elif event.key == pygame.K_RETURN and txtnpcdone and txtnpcactivemsg == len(messages)-1 and rect_char.colliderect(rect_npcreact):
                txtnpcactivemsg = 0
                txtnpccounter = 0
                message = messages[txtnpcactivemsg]
                done = False
                pygame.mixer.Sound.play(lisatalksfx[random.randint(0,1)])

    # fill the screen with a color to wipe away anything from last frame

    screen.fill("white")
    screen.blit(bg,[0,0])

    clock = pygame.time.Clock()
    clock.tick(60)
    if isGamePaused == False:
        screen.blit(npc,(300,200))
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
            if keys[pygame.K_TAB] and songcounter == 0:
                songcounter += 1
                pygame.mixer.Sound.play(act0song)
                
                
        if rect_char.colliderect(rect_npcreact):
            if blipcounter == 0:
                pygame.mixer.Sound.play(lisatalksfx[random.randint(0,1)])
                blipcounter += 1
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