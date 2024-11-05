import pygame
import os
from player import Player

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("´Pixel Survival")

# Carrega o fundo
BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets/images", "background.png"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Cria o jogador
player = Player(WIDTH // 2, HEIGHT // 2, speed=2)

# Loop principal do jogo
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.update()  # Atualiza a animação do jogador

    # Renderização
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # Desenha o fundo
    player.draw(screen)  # Desenha o jogador

    pygame.display.flip()  # Atualiza a tela

# Finaliza o Pygame
pygame.quit()
