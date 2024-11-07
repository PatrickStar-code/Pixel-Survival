import pygame
import os
import random
import json
from player import Player
from enemy import Enemy
from enemy2 import Enemy2
from bullet import Bullet
from boss import Boss

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

    # Verifica se o arquivo existe e carrega as pontuações existentes
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores.append(score_data)
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

# Função para executar o jogo
def run_game():
    # Variáveis do jogo
    player = Player(WIDTH // 2, HEIGHT // 2, speed=2)
    enemies = []
    bullets = []
    score = 0
    difficulty_level = 10
    next_difficulty_increase = 100
    enemy_spawn_delay = 2000
    enemy_speed = 1.5
    boss_spawned = False
    boss_level = 10
    game_over = False
    score_saved = False  # Flag para salvar a pontuação apenas uma vez

    clock = pygame.time.Clock()
    shoot_delay = 500
    last_shot_time = pygame.time.get_ticks()
    pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_delay)

    # Função interna para resetar o jogo
    def reset_game():
        nonlocal player, enemies, bullets, score, difficulty_level, next_difficulty_increase, enemy_speed, enemy_spawn_delay, game_over, boss_spawned, score_saved
        player = Player(WIDTH // 2, HEIGHT // 2, speed=2)
        enemies = []
        bullets = []
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
                # Gerenciamento de spawn do boss e inimigos
                if difficulty_level == boss_level and not boss_spawned:
                    enemies.append(Boss(player, enemy_speed, WIDTH, HEIGHT))
                    boss_level += 10
                    boss_spawned = True
                else:
                # Verifica o nível de dificuldade para spawnar inimigos
                    if difficulty_level >= 3:
                        # A partir do nível 3, 50% de chance de spawnar Enemy ou Enemy2
                        enemy_type = Enemy2 if random.random() < 0.5 else Enemy
                    else:
                        # Antes do nível 3, apenas spawn de Enemy
                        enemy_type = Enemy
                    enemies.append(enemy_type(player, enemy_speed, WIDTH, HEIGHT))


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
                closest_enemy = min(enemies, key=lambda e: (player.rect.centerx - e.rect.centerx)**2 + (player.rect.centery - e.rect.centery)**2)
                bullets.append(Bullet(player.rect.centerx, player.rect.centery, closest_enemy))
                last_shot_time = current_time

            # Atualização das balas e checagem de colisão com inimigos
            for bullet in bullets[:]:
                bullet.update()
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= 1
                        bullets.remove(bullet)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            score += 10
                        break

            # Atualização dos inimigos e verificação de colisões com o jogador
            for enemy in enemies[:]:
                enemy.update()
                if player.rect.colliderect(enemy.rect):
                    player.health -= 1
                    enemies.remove(enemy)

            # Aumenta a dificuldade a cada 100 pontos
            if score >= next_difficulty_increase:
                difficulty_level += 1
                enemy_speed += 0.1
                enemy_spawn_delay = max(500, enemy_spawn_delay - 200)
                pygame.time.set_timer(pygame.USEREVENT + 1, enemy_spawn_delay)
                next_difficulty_increase += 100

        # Renderização dos elementos na tela
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        player.draw(screen)

        for enemy in enemies:
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

        if player.health <= 0:
            game_over = True
            if not score_saved:
                save_score(score)
                score_saved = True

        if game_over:
            # Mensagem de "Game Over" e instruções para reiniciar
            font = pygame.font.Font(None, 80)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Pressione 'R' para reiniciar", True, (255, 255, 255))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
