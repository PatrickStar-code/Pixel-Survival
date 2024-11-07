import pygame
import math

class Projectile:
    def __init__(self, x, y, target, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.target = target
        self.rect = pygame.Rect(self.x, self.y, 10, 10)  # Tamanho básico do projétil (pode ser ajustado)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Cor vermelha para o projétil

        # Definir direção do projétil
        self.dx, self.dy = self.get_direction()

    def get_direction(self):
        # Calcula a direção do projétil com base na posição do jogador no momento do disparo
        dx, dy = self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        # Normaliza a direção
        if distance != 0:
            dx, dy = dx / distance, dy / distance

        return dx, dy

    def update(self):
        # Move o projétil na direção definida no momento do disparo
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, screen):
        # Desenha o projétil na tela
        screen.blit(self.image, self.rect.topleft)
