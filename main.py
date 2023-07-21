import pygame
import random
import math
from pygame import mixer

# İnitialize the pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('Background.mp3')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('SpaceShip.png')
playerX = 400
playerY = 500
playerX_change = 0
playerY_change = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append( pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(30)

# Bullet
# Not - ready statement = you can't see the bullet
# Fire statement = you can see the bullet (moving)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y + 10))

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32 )
textX = 10
textY = 10

# Game over Text
over_font = pygame.font.Font("freesansbold.ttf", 64 )

def show_score ( x,y):
    score = font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(textX,textX))

def game_over_text():
    over_text = over_font.render("GAME OVER !", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY , 2)))
    if distance < 27:
        return True
    else :
        return False


def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i) :
    screen.blit(enemyImg[i], (x, y))

# Set a variable to control the main loop
running = True

# Main loop
while running:
    # Check for events
    for event in pygame.event.get():
        # If the user closes the window, set running to False to exit the main loop
        if event.type == pygame.QUIT:
            running = False


        # KEYDOWN = KEY PRESSING , KEYUP = KEY RELEASING
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.1

            if event.key ==pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB - RED, GREEN, BLUE
    screen.fill((0,0,0))
    screen.blit((background),(0,0))
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bulletY <= 0 :
        bulletY = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] >= 475 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.mp3')
            explosion_Sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()   # ALWAYS SHOULD BE UPDATED !!!!!

# Quit Pygame
pygame.quit()
