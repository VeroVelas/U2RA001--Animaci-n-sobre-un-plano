import os
import math
import random
import pygame
import sys

# Inicializa Pygame
pygame.init()

# Crea la pantalla
screen = pygame.display.set_mode((800, 600))

# Carga la imagen de fondo
background = pygame.image.load('background.png')

# Título e Icono
pygame.display.set_caption("Historia Animada")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Jugador
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Sprites
sprites = [
    {'img': pygame.image.load('laser.png'), 'x': 300, 'y': 100, 'x_change': 1, 'y_change': 40},
    {'img': pygame.image.load('meteorBrown_big1.png'), 'x': 500, 'y': 150, 'x_change': 1.5, 'y_change': 40},
    {'img': pygame.image.load('enemy.png'), 'x': 200, 'y': 200, 'x_change': 1.2, 'y_change': 40},
    {'img': pygame.image.load('enemy2_1.png'), 'x': 100, 'y': 250, 'x_change': 1.8, 'y_change': 40},
    {'img': pygame.image.load('player.png'), 'x': 600, 'y': 100, 'x_change': 1.5, 'y_change': 40},
]

# Objetos adicionales
objects = [
    {'img': pygame.image.load('ufo.png'), 'x': random.randint(0, 500), 'y': random.randint(50, 180)},
    {'img': pygame.image.load('meteor.png'), 'x': random.randint(0, 606), 'y': random.randint(50, 150)},
    {'img': pygame.image.load('meteorBrown_big2.png'), 'x': random.randint(0, 736), 'y': random.randint(50, 150)},
    {'img': pygame.image.load('missile.png'), 'x': random.randint(0, 736), 'y': random.randint(50, 150)},
]

# Bala
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Explosiones
explosion_imgs = [
    pygame.image.load('sonicExplosion06.png'),
    pygame.image.load('sonicExplosion04.png'),
    pygame.image.load('regularExplosion01.png')
]

# Puntuación
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Mostrar puntuación
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Texto de Game Over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Dibujar jugador
def player(x, y):
    screen.blit(playerImg, (x, y))

# Dibujar sprite
def sprite(x, y, img):
    screen.blit(img, (x, y))

# Dibujar objeto adicional
def draw_object(x, y, img):
    screen.blit(img, (x, y))

# Disparar bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Colisión
def isCollision(spriteX, spriteY, bulletX, bulletY):
    distance = math.sqrt(math.pow(spriteX - bulletX, 2) + (math.pow(spriteY - bulletY, 2)))
    return distance < 27

# Mostrar explosión
def show_explosion(x, y, explosion_index):
    screen.blit(explosion_imgs[explosion_index], (x, y))

# Bucle del juego
start_time = pygame.time.get_ticks()
running = True
explosion_index = 0
explosion_time = 0
explosion_duration = 500  # Duración de cada imagen de explosión en milisegundos
while running:
    # Dibuja el fondo
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Si se presiona una tecla, verificar si es derecha o izquierda
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Obtener la coordenada actual del jugador
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimiento de los sprites
    for sprite_data in sprites:
        sprite_data['x'] += sprite_data['x_change']
        if sprite_data['x'] <= 0 or sprite_data['x'] >= 736:
            sprite_data['x_change'] = -sprite_data['x_change']
            sprite_data['y'] += sprite_data['y_change']

        # Colisión
        collision = isCollision(sprite_data['x'], sprite_data['y'], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            sprite_data['x'] = random.randint(0, 736)
            sprite_data['y'] = random.randint(50, 150)
            explosion_time = pygame.time.get_ticks()

        sprite(sprite_data['x'], sprite_data['y'], sprite_data['img'])

    # Mostrar objetos adicionales
    for obj in objects:
        draw_object(obj['x'], obj['y'], obj['img'])

    # Mostrar explosión
    if pygame.time.get_ticks() - explosion_time < explosion_duration:
        show_explosion(bulletX, bulletY, explosion_index)
        explosion_index = (explosion_index + 1) % len(explosion_imgs)

    # Movimiento de la bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

    # Verifica si han pasado 30 segundos
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # Tiempo en segundos
    if elapsed_time >= 30:
        print("Se han completado 30 segundos. Terminando la animación.")
        running = False

pygame.quit()
sys.exit()
