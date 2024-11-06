import pygame
import math

class Bullet:
    def __init__(self, x, y, target, speed=5, damage=1):
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))  # Cor vermelha para a bala
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calcula a direção em relação ao alvo
        dx, dy = target.rect.centerx - x, target.rect.centery - y
        distance = math.hypot(dx, dy)
        self.dx, self.dy = (dx / distance) * speed, (dy / distance) * speed
        
        self.damage = damage  # Dano da bala

    def update(self):
        # Move a bala
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen):
        # Desenha a bala na tela
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, enemy):
        """Verifica se a bala colidiu com um inimigo"""
        if self.rect.colliderect(enemy.rect):
            return True
        return False
