import pygame
import sys
import json
from game import run_game  # Função principal do jogo no game.py

# Inicializa o Pygame e define a tela
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Survival Menu")

# Configurações de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)

# Fonte
font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)

# Função para desenhar o texto centralizado
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Função para desenhar um botão com hover e registrar cliques únicos
def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Muda a cor do botão ao passar o mouse
    color = LIGHT_GRAY if x + width > mouse[0] > x and y + height > mouse[1] > y else GRAY
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, button_font, BLACK, screen, x + width // 2, y + height // 2)

    # Verifica se o botão foi clicado e realiza ação
    if click[0] == 1 and x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.time.delay(200)  # Pequeno atraso para evitar múltiplos cliques
        if action is not None:
            action()

# Função para mostrar a tela de pontuações
def show_scores():
    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    # Ordena as pontuações em ordem decrescente
    scores.sort(key=lambda x: x["score"], reverse=True)

    showing_scores = True
    while showing_scores:
        screen.fill(WHITE)
        draw_text("Pontuações", font, BLACK, screen, WIDTH // 2, 50)

        # Exibe as 10 melhores pontuações
        for i, score in enumerate(scores[:10]):
            score_text = f"{i + 1}. Score: {score['score']}"
            draw_text(score_text, button_font, BLACK, screen, WIDTH // 2, 100 + i * 40)

        # Instrução para retornar ao menu
        draw_text("Pressione ESC para voltar", button_font, BLACK, screen, WIDTH // 2, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                showing_scores = False

        pygame.display.flip()

# Funções para os botões
def start_game():
    run_game()  # Executa o jogo ao clicar em "Iniciar"

def quit_game():
    pygame.quit()
    sys.exit()

# Loop principal do menu
running = True
while running:
    screen.fill(WHITE)

    # Desenha o título do jogo
    draw_text("Pixel Survival", font, BLACK, screen, WIDTH // 2, HEIGHT // 3)

    # Desenha os botões com ações únicas
    draw_button("Iniciar", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, start_game)
    draw_button("Pontuações", WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50, show_scores)
    draw_button("Sair", WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50, quit_game)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
