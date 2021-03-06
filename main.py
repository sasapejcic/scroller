import pygame
from random import randint

pygame.init()

rock_color = (0, 255, 255)

W, H = 800, 600
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Penetrator')

player_range_start = (W * 1) // 8
player_range_end = (W * 5) //8
fps = 27
probability = 50
missile_speed = 5

levelVolume = 100
startMinPassage = 200
startMaxPassage = 500

repeater = W // 10
bgUp = [H // 30] * repeater
bgDown = [H - H // 30] * repeater
enemy = [0] * repeater
enemy_fired = [0] * repeater

def BorderGenerator(a, b):
    x = randint(- H // 20, H // 20)
    if a + x < H // 30:
        bgUp.append(H // 30)
    elif a + x < b - maxPassage:
        bgUp.append(b - maxPassage)
    elif a + x > b - minPassage:
        bgUp.append(b - minPassage)
    else:
        bgUp.append(a + x)

    x = randint(- H // 20, H // 20)
    y = randint(0, 100)
    if b + x > H - H // 30:
        pos = H - H // 30
    elif b + x > a + maxPassage:
        pos = a + maxPassage
    elif b + x < a + minPassage:
        pos = a + minPassage
    else:
        pos = b + x
    bgDown.append(pos)

    y = randint(0, 1000)
    if y > 1000 - probability:
        enemy.append(pos)
    else:
        enemy.append(0)
    enemy_fired.append(0)


def collision():
    col = False
    if abs(playerY-bgUp[playerX//10])<radius or abs(playerY-bgDown[playerX//10]) < radius:
        col =  True
    for i in range(len(enemy)):
        if (enemy[i]-playerY)**2 + (i*10-playerX)**2 < (radius+10)**2:
            col = True
    return col

def redrawWindow():
    win.fill((255, 255, 255))
    temenaUp = []
    temenaDown = []
    for i in range(len(bgUp)):
        temenaUp.append((i*10, bgUp[i]))
        temenaDown.append((i*10, bgDown[i]))
    temenaUp.append((W, bgUp[-1]))
    temenaUp.append((W, 0))
    temenaUp.append((0, 0))
    temenaDown.append((W, bgDown[-1]))
    temenaDown.append((W, H))
    temenaDown.append((0, H))
    pygame.draw.polygon(win, (rock_color), temenaUp)
    pygame.draw.polygon(win, (rock_color), temenaDown)
    pygame.draw.circle(win, pygame.Color("green"), (playerX, playerY), radius)
    for i in range(len(enemy)):
        if enemy[i]!=0:
            pygame.draw.polygon(win,pygame.Color("red"), ((i*10, enemy[i]),(i*10+5, enemy[i]+10),(i*10, enemy[i]-10),(i*10-5, enemy[i]+10)))

    font = pygame.font.SysFont("Arial", 50)
    tekst = font.render(str(counter), True, pygame.Color("blue"))
    win.blit(tekst, (0, 0))
    pygame.display.update()



run = True

counter = 0

playerX = W//4
playerY = H//2
dx = 0
dy = 0
radius = 16
velocity = 10

clock = pygame.time.Clock()

while run:
    counter +=1
    clock.tick(fps)

    minPassage = startMinPassage - (counter//levelVolume-1)*20
    maxPassage = startMaxPassage - (counter//levelVolume-1)*30

    bgUp = bgUp[1:]
    bgDown = bgDown[1:]
    enemy = enemy[1:]
    enemy_fired = enemy_fired[1:]
    BorderGenerator(bgUp[-1], bgDown[-1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                dy = -1*velocity
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dy = velocity
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx = -1*velocity
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx = velocity

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                dy = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dy = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx = 0

    playerX += dx
    if playerX>player_range_end:
        playerX = player_range_end
        dx = 0
    if playerX<player_range_start:
        playerX = player_range_start
        dx = 0
    playerY += dy

    for i in range(len(enemy)):
        if enemy_fired[i]!=0:
            enemy[i] -= missile_speed
        elif (velocity*abs(playerY-enemy[i])>(missile_speed)*abs(i*10-playerX)-radius):
            enemy_fired[i] = 1
        elif playerX+2*radius>i*velocity:
            enemy_fired[i] = 1


    redrawWindow()

    if collision():
        run = False
        print(counter)
