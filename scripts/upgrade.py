import random
import pygame

class Upgrade:
    def __init__(self, upgrade_type, x, y):
        self.upgrade_type = upgrade_type  # Tipo do upgrade (movimento, ataque, dano, multishot)
        self.rect = pygame.Rect(x, y, 30, 30)  # Área de colisão para pegar o upgrade
        self.image = pygame.Surface((30, 30))  # Imagem do upgrade (simplificada como um quadrado)
        self.image.fill((0, 255, 0))  # Cor verde para visualização

    def apply_upgrade(self, player):
        """Aplica o upgrade ao jogador"""
        if self.upgrade_type == "move_speed":
            player.move_speed = min(player.move_speed + 0.5, 5)  # Limite de velocidade
        elif self.upgrade_type == "shoot_speed":
            player.shoot_delay = max(player.shoot_delay - 50, 100)  # Limite mínimo de delay
        elif self.upgrade_type == "damage":
            player.damage = min(player.damage + 1, 10)  # Limite de dano
        elif self.upgrade_type == "multishot":
            player.multishot = True

    def draw(self, screen):
        """Desenha o upgrade na tela"""
        screen.blit(self.image, self.rect.topleft)
