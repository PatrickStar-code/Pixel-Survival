import pygame
import random
import os
import math

class Enemy2:
    def __init__(self, player, speed, screen_width, screen_height, scale_factor=2.0):
        # Carregar e redimensionar as imagens de animação
        self.images = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets/images/enemy", f"CrabMoving{i + 1}.png")),
                (int(pygame.image.load(os.path.join("assets/images/enemy", f"CrabMoving{i + 1}.png")).get_width() * scale_factor),
                 int(pygame.image.load(os.path.join("assets/images/enemy", f"CrabMoving{i + 1}.png")).get_height() * scale_factor))
            ) for i in range(4)
        ]

        # Escolher uma posição fora da tela
        self.rect = self.spawn_outside_screen(screen_width, screen_height)

        # Definir variáveis de movimento e direção
        self.speed = speed
        self.player = player
        self.animation_frame = 0
        self.animation_speed = 10  # Ajuste para definir a velocidade de animação
        self.current_sprite = self.images[0]
        self.health = 3

    def spawn_outside_screen(self, screen_width, screen_height):
        # Escolhe um ponto aleatório fora das bordas da tela
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, screen_width)
            y = -self.images[0].get_height()
        elif side == 'bottom':
            x = random.randint(0, screen_width)
            y = screen_height
        elif side == 'left':
            x = -self.images[0].get_width()
            y = random.randint(0, screen_height)
        else:  # right
            x = screen_width
            y = random.randint(0, screen_height)
        return pygame.Rect(x, y, self.images[0].get_width(), self.images[0].get_height())

    def move_towards_player(self):
        # Calcula a direção para o jogador
        player_x, player_y = self.player.rect.center
        dx, dy = player_x - self.rect.centerx, player_y - self.rect.centery
        distance = math.hypot(dx, dy)
        
        # Normaliza e multiplica pela velocidade para mover na direção do player
        if distance > 0:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def update(self):
        # Atualiza posição
        self.move_towards_player()
        
        # Atualiza o frame de animação
        self.animation_frame += 1
        if self.animation_frame >= self.animation_speed * len(self.images):
            self.animation_frame = 0
        sprite_index = self.animation_frame // self.animation_speed
        self.current_sprite = self.images[sprite_index]

    def draw(self, screen):
        # Desenha o sprite atual na tela
        screen.blit(self.current_sprite, self.rect.topleft)
