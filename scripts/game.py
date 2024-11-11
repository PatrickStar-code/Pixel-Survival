import pygame
import os
import random
import json
from player import Player
from enemy import Enemy
from enemy2 import Enemy2
from bullet import Bullet
from boss import Boss
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

# Função para salvar a pontuação em um arquivo JSON
def save_score(score):
    score_data = {"score": score}

    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append(score_data)
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

# Função para gerar uma posição fora da tela
def generate_spawn_position():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        return random.randint(0, WIDTH), -50  # Acima da tela
    elif side == 'bottom':
        return random.randint(0, WIDTH), HEIGHT + 50  # Abaixo da tela
    elif side == 'left':
        return -50, random.randint(0, HEIGHT)  # À esquerda da tela
    elif side == 'right':
        return WIDTH + 50, random.randint(0, HEIGHT)  # À direita da tela

# Função para spawnar múltiplos inimigos fora da tela
def spawn_multiple_enemies(enemies, player, difficulty_level, enemy_speed, max_enemies=4):
    num_enemies = random.randint(1, max_enemies)  # Define entre 1 e 4 inimigos
    for _ in range(num_enemies):
        enemy_type = Enemy2 if difficulty_level >= 3 and random.random() < 0.5 else Enemy
        spawn_x, spawn_y = generate_spawn_position()
        if(enemy_type == Enemy2):
            new_enemy = enemy_type(difficulty_level/2, player, enemy_speed, WIDTH, HEIGHT)
        else:
            new_enemy = enemy_type(difficulty_level,player, enemy_speed, WIDTH, HEIGHT)
        new_enemy.rect.x = spawn_x
        new_enemy.rect.y = spawn_y
        enemies.append(new_enemy)

# Função para executar o jogo
def run_game():
    # Variáveis do jogo
    player = Player(WIDTH // 2, HEIGHT // 2, speed=2)
    enemies = []
    bullets = []
    upgrades = []  
    score = 0
    difficulty_level = 1
    next_difficulty_increase = 100
    enemy_spawn_delay = 5000
    enemy_speed = 1
    boss_spawned = False
    boss_level = 10
    game_over = False
    score_saved = False  

    clock = pygame.time.Clock()
    shoot_delay = player.attack_speed
    last_shot_time = pygame.time.get_ticks()
    pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_delay)

    # Função interna para resetar o jogo
    def reset_game():
        nonlocal player, enemies, bullets, upgrades, score, difficulty_level, next_difficulty_increase, enemy_speed, enemy_spawn_delay, game_over, boss_spawned, score_saved
        player = Player(WIDTH // 2, HEIGHT // 2, speed=2)
        enemies = []
        bullets = []
        upgrades = []
        score = 0
        difficulty_level = 1
        next_difficulty_increase = 100
        enemy_spawn_delay = 2000
        enemy_speed = 1.5
        game_over = False
        boss_spawned = False
        score_saved = False
        pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_delay)

    # Loop principal do jogo
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Sai do jogo e retorna ao menu
            elif event.type == pygame.USEREVENT + 1 and not game_over:
                # Gerenciamento de spawn de inimigos com limite de 3
                if len(enemies) < 3:
                    if difficulty_level == boss_level and not boss_spawned:
                        boss = Boss(difficulty_level / 10, player, enemy_speed, WIDTH, HEIGHT)
                        enemies.append(boss)
                        boss_level += 10
                        boss_spawned = True
                    else:
                        spawn_multiple_enemies(enemies, player, difficulty_level, enemy_speed)  # Spawn múltiplos inimigos

            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()  # Reinicia o jogo ao pressionar 'R'

        if not game_over:
            # Atualizações do jogador e inimigos
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update()

            # Tiro automático do jogador
            current_time = pygame.time.get_ticks()
            if enemies and current_time - last_shot_time > shoot_delay:
                closest_enemy = min(enemies, key=lambda e: (player.rect.centerx - e.rect.centerx) ** 2 + (player.rect.centery - e.rect.centery) ** 2)
                bullets.append(Bullet(player.rect.centerx, player.rect.centery, closest_enemy))
                last_shot_time = current_time

            # Atualização das balas e checagem de colisão com inimigos
            for bullet in bullets[:]:
                bullet.update()
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= player.attack_power
                        bullets.remove(bullet)
                        if enemy.health <= 0:
                            if isinstance(enemy, Boss):
                                # Remove o Boss e limpa os minions invocados por ele
                                if enemy in enemies:
                                    enemies.remove(enemy)
                                for minion in enemy.minions:
                                    if minion in enemies:
                                        enemies.remove(minion)
                                boss_spawned = False
                                score += 40
                            else:
                                if enemy in enemies:
                                    enemies.remove(enemy)
                                score += 10

                            if random.random() < 0.4:
                                upgrades.append(Upgrade(enemy.rect.x, enemy.rect.y))  
                        break

            for enemy in enemies[:]:
                enemy.update()
                if player.rect.colliderect(enemy.rect):
                    if isinstance(enemy, Boss):
                        player.health -= 1  
                    elif isinstance(enemy, Enemy):  
                        player.health -= 1  
                        enemies.remove(enemy)
                    elif isinstance(enemy, Enemy2):
                        player.health -= 1  
                        enemies.remove(enemy)

            if score >= next_difficulty_increase:
                difficulty_level += 1
                enemy_speed += 0.1
                enemy_spawn_delay = max(500, enemy_spawn_delay - 200)
                pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_delay)
                next_difficulty_increase += 100

            for upgrade in upgrades[:]:
                if player.rect.colliderect(upgrade.rect):
                    player.apply_upgrade(upgrade.type)
                    upgrades.remove(upgrade)

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        player.draw(screen)

        for enemy in enemies:
            if isinstance(enemy, Boss):
                enemy.update()
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        for i in range(player.health):
            screen.blit(HEART_IMAGE, (10 + i * 25, 10))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 150, 10))
        level_text = font.render(f"Level: {difficulty_level}", True, (255, 255, 255))
        screen.blit(level_text, (WIDTH / 2, 10))

        status_text = font.render(f"Speed: {player.speed:.2f} | Attack Cool Down: {player.attack_speed} | Attack Power: {player.attack_power:.2f}", True, (255, 255, 255))
        screen.blit(status_text, (10, HEIGHT - 40))

        if player.health <= 0:
            game_over = True
            if not score_saved:
                save_score(score)
                score_saved = True

        if game_over:
            font = pygame.font.Font(None, 80)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Pressione 'R' para reiniciar", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

        for upgrade in upgrades:
            upgrade.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
