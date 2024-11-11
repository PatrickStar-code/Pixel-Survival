import pygame
import random

class Upgrade:
    def __init__(self, x, y):
        # Verifica se os parâmetros estão corretos
        if x is None or y is None:
            raise ValueError("Posição x e y são obrigatórias para o Upgrade.")
        
        self.x = x
        self.y = y
        self.types = ["speed", "attack_speed", "attack_power", "health"]
        self.type = random.choice(self.types)
        
        # Aqui removemos a imagem e vamos desenhar círculos
        self.radius = 15  # Tamanho do círculo
        self.color = self.get_color_based_on_type(self.type)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

    def get_color_based_on_type(self, upgrade_type):
        """Retorna a cor do upgrade com base no tipo."""
        if upgrade_type == "speed":
            return (0, 0, 255)  # Azul
        elif upgrade_type == "attack_speed":
            return (255, 165, 0)  # Laranja
        elif upgrade_type == "attack_power":
            return (255, 69, 0)  # Vermelho alaranjado
        elif upgrade_type == "health":
            return (0, 255, 0)  # Verde
        return (255, 255, 255)  # Branco como fallback

    def draw(self, screen):
        """Desenha o upgrade na tela."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
