import pygame
import math
import random
from pygame import mixer

# =============creating  our first game window ============
# we should intialize the pygame first

pygame.init()

screen = pygame.display.set_mode((800, 600))

#  =================backgroud=========
background = pygame.image.load('background.jpg')

# ===========background sound=========
mixer.music.load('background.wav')
mixer.music.play(-1)# her we give -1 to play music contiue


# ============== title and icon =============
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("744737.png")
pygame.display.set_icon(icon)

# ========== player =========
playerImg = pygame.image.load('744737.png')
playerX = 370
playerY = 480
playerX_change = 0

# ========== ENEMY =========
enemyImg =[]
enemyX = []
enemyY =[]
enemyX_change=[]
enemyY_change =[]
num_of_enemies= 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('1970285.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append( 0.3)
    enemyY_change.append(35 )

# ========== bullet =========
# ready state = u cant see the bullet  on the screen
# fire state = The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# =============score===========
score_value =0
font = pygame.font.Font("freesansbold.ttf",32)
textX= 10
textY = 10

# ============gameover ==========
over_font = pygame.font.Font("freesansbold.ttf",64)


def show_score(x,y):
    score = font.render("Score:"+ str(score_value),True,(255,255,253))
    screen.blit(score, (x, y))

def game_over_text():
    over_text =over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over_text, (200,250) )

def player(x, y):
    screen.blit(playerImg, (x, y))  # bilt  actually means draw


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
      global bullet_state
      bullet_state = "fire"
      screen.blit(bulletImg,(x+16,y+10))

def iscollision (enemyX, enemyY,bulletX,bulletY,):
       distance =math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
       if  distance<27:
           return True
       else:
           return False


# ============game loop =============
running = True
while running:
    # =========backgroud of window=======
    # if u want background contunies until end
    # then write code inside  while loop
    # RGB -> Red,Green,Blue
    screen.fill((0, 0, 0))  # it wont change to red
    # color becuse u have to upate like
    # pygame.display.upadte()

    #  ============= background ==========
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # == movement and keyword connection with player=====
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_SPACE:
                if bullet_state =="ready":
                    bullet_sound= mixer.Sound('laser.wav')   # her it is mixer.sound instead of music beacuse it just a sound we need
                    bullet_sound.play()
                    bulletX= playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # ==============making  player not go out of bounds=======
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # ================making enemy not got out of bounds=======
    for i in range(num_of_enemies):
        # ========= game over ========
        if enemyY[i] >= 450 and enemyX[i] >= playerX:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = - 0.3
            enemyY[i] += enemyY_change[i]

        # ====================collosion =========================
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')  # her it is mixer.sound instead of music beacuse it just a sound we need
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)


    # ====================bulllet movement ==============
    if bulletY <= 0 :
        bulletY = 400
        bullet_state ="ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bulletY_change



    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
