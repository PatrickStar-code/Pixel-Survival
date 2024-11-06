import pygame
import os
import random
from player import Player
from enemy import Enemy
from enemy2 import Enemy2 
from bullet import Bullet  
from upgrade import Upgrade

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Survival")

# Carrega o fundo e a imagem de coração
BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets/images", "background.png"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
HEART_IMAGE = pygame.image.load(os.path.join("assets/images", "heart.png"))
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (40, 40))

# Cria o jogador
player = Player(WIDTH // 2, HEIGHT // 2, speed=2)

# Configurações dos inimigos e balas
enemy_speed = 1.5
enemies = []
bullets = []
enemy_spawn_delay = 2000
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, enemy_spawn_delay)

# Configurações da pontuação e dificuldade
score = 0
difficulty_level = 1
next_difficulty_increase = 100

# Configurações de tempo e tiro
clock = pygame.time.Clock()
shoot_delay = 500  # Intervalo entre tiros em milissegundos
last_shot_time = pygame.time.get_ticks()

# Função para atualizar a dificuldade
def update_difficulty():
    global difficulty_level, enemy_spawn_delay, enemy_speed, next_difficulty_increase
    difficulty_level += 1

    # Aumenta a dificuldade conforme o nível
    enemy_speed += 0.2
    enemy_spawn_delay = max(500, enemy_spawn_delay - 200)
    pygame.time.set_timer(spawn_event, enemy_spawn_delay)

# Função para spawnar inimigos
def spawn_enemy():
    # Define a chance de spawnar `Enemy2` após 200 pontos
    if score >= 200 and random.random() < 0.5:  # 50% de chance para `Enemy2`
        enemy = Enemy2(player, enemy_speed, WIDTH, HEIGHT)
    else:
        enemy = Enemy(player, enemy_speed, WIDTH, HEIGHT)
    enemies.append(enemy)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_event:
            spawn_enemy()

    # Movimentação do jogador e atualização de animação
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.update()

    # Tiro automático do jogador
    current_time = pygame.time.get_ticks()
    if enemies and current_time - last_shot_time > shoot_delay:
        closest_enemy = min(enemies, key=lambda e: (player.rect.centerx - e.rect.centerx)**2 + (player.rect.centery - e.rect.centery)**2)
        bullet = Bullet(player.rect.centerx, player.rect.centery, closest_enemy)
        bullets.append(bullet)
        last_shot_time = current_time

    # Atualiza balas e checa colisão com inimigos
    for bullet in bullets[:]:
        bullet.update()
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= 1
                bullets.remove(bullet)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += 10  # Incrementa a pontuação ao derrotar um inimigo
                break

    # Atualiza os inimigos e verifica colisões com o jogador
    for enemy in enemies[:]:
        enemy.update()
        if player.rect.colliderect(enemy.rect):
            player.health -= 1
            enemies.remove(enemy)
            if player.health <= 0:
                print("Game Over")
                running = False

    # Aumenta a dificuldade ao atingir a pontuação alvo
    if score >= next_difficulty_increase:
        update_difficulty()
        next_difficulty_increase += 100

    # Renderização
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    player.draw(screen)

    # Desenha os inimigos e balas
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Exibe a vida do jogador
    for i in range(player.health):
        screen.blit(HEART_IMAGE, (10 + i * 25, 10))

    # Exibe a pontuação
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 10))

    # Exibe Level
    font = pygame.font.Font(None, 36)
    level_text = font.render(f" {difficulty_level}", True, (255, 255, 255))
    screen.blit(level_text, (WIDTH/2, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
