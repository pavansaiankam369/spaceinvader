# Space Invader Game

This project is a simple implementation of the classic Space Invader game using Python and the Pygame library. The player controls a spaceship and must defend Earth from alien invaders by shooting bullets.

## Table of Contents
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Features](#features)
- [Files](#files)
- [Code Overview](#code-overview)
- [Dependencies](#dependencies)
- [License](#license)

## Installation
1. Clone the repository or download the source code.
2. Install the required libraries using pip:
   ```sh
   pip install pygame
   ```

3. Ensure you have the following assets in the same directory as your script:
   - `background.jpg`: Background image for the game.
   - `744737.png`: Image for the player spaceship and game icon.
   - `1970285.png`: Image for the enemy spaceship.
   - `bullet.png`: Image for the bullet.
   - `background.wav`: Background music for the game.
   - `laser.wav`: Sound effect for shooting bullets.
   - `explosion.wav`: Sound effect for enemy explosions.

4. Run the game script:
   ```sh
   python space_invader.py
   ```

## How to Play
- Use the left and right arrow keys to move the spaceship horizontally.
- Press the space bar to shoot bullets.
- Destroy enemy spaceships to gain points.
- Avoid letting the enemies reach the bottom of the screen, as this will end the game.

## Features
- Background music and sound effects for an immersive experience.
- Multiple enemies with random starting positions and movement patterns.
- Score tracking and display.
- Game over screen when enemies reach the bottom.

## Files
- `space_invader.py`: Main game script.
- `background.jpg`: Background image for the game.
- `744737.png`: Image for the player spaceship and game icon.
- `1970285.png`: Image for the enemy spaceship.
- `bullet.png`: Image for the bullet.
- `background.wav`: Background music for the game.
- `laser.wav`: Sound effect for shooting bullets.
- `explosion.wav`: Sound effect for enemy explosions.

## Code Overview

```python
import pygame
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))

# Load background image
background = pygame.image.load('background.jpg')

# Load and play background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Set window title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("744737.png")
pygame.display.set_icon(icon)

# Load player image and set initial position
playerImg = pygame.image.load('744737.png')
playerX = 370
playerY = 480
playerX_change = 0

# Load enemy images and set initial positions
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('1970285.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(35)

# Load bullet image and set initial state
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 253))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Game Loop
running = True
while running:
    # Fill screen with background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Update player position
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Update enemy positions
    for i in range(num_of_enemies):
        if enemyY[i] >= 450 and enemyX[i] >= playerX:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i])

    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
```

## Dependencies
- Python 3.x
- Pygame

## License
This project is licensed under the MIT License.
