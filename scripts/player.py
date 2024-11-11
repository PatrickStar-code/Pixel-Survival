import pygame
import os
import random

class Player:
    def __init__(self, x, y, speed, scale_factor=2.0):  
        # Parâmetros iniciais do jogador
        self.tileset = pygame.image.load(os.path.join("assets/images", "player_tileset.png"))
        self.tileset_width = self.tileset.get_width() // 4  # 4 colunas
        self.tileset_height = self.tileset.get_height() // 4  # 4 linhas

        # Cria listas para cada direção com escalonamento
        self.sprites = {
            'down': [pygame.transform.scale(self.tileset.subsurface(pygame.Rect(i * self.tileset_width, 0, self.tileset_width, self.tileset_height)), (int(self.tileset_width * scale_factor), int(self.tileset_height * scale_factor))) for i in range(4)],
            'up': [pygame.transform.scale(self.tileset.subsurface(pygame.Rect(i * self.tileset_width, self.tileset_height, self.tileset_width, self.tileset_height)), (int(self.tileset_width * scale_factor), int(self.tileset_height * scale_factor))) for i in range(4)],
            'left': [pygame.transform.scale(self.tileset.subsurface(pygame.Rect(i * self.tileset_width, 2 * self.tileset_height, self.tileset_width, self.tileset_height)), (int(self.tileset_width * scale_factor), int(self.tileset_height * scale_factor))) for i in range(4)],
            'right': [pygame.transform.scale(self.tileset.subsurface(pygame.Rect(i * self.tileset_width, 3 * self.tileset_height, self.tileset_width, self.tileset_height)), (int(self.tileset_width * scale_factor), int(self.tileset_height * scale_factor))) for i in range(4)],
        }

        # Atributos do jogador
        self.current_sprite = self.sprites['down'][0]
        self.rect = self.current_sprite.get_rect(center=(x, y))
        self.speed = speed
        self.attack_speed = 1000  # Tempo entre tiros em ms
        self.attack_power = 1  # Dano inicial do jogador
        self.direction = 'down'
        self.health = 4
        self.animation_frame = 0
        self.animation_speed = 10  # Velocidade da animação
        self.animating = False

    def move(self, keys):
        # Movimenta o jogador
        move_x = 0
        move_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -self.speed
            self.direction = 'left'
            self.animating = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = self.speed
            self.direction = 'right'
            self.animating = True
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -self.speed
            self.direction = 'up'
            self.animating = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = self.speed
            self.direction = 'down'
            self.animating = True

        # Atualiza a posição do jogador
        self.rect.x += move_x
        self.rect.y += move_y

        # Limitar o jogador à tela
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))  # Largura da tela assumida como 800
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))  # Altura da tela assumida como 600

        # Verifica se não está se movendo e para a animação
        if not (move_x or move_y):
            self.animating = False

    def apply_upgrade(self, upgrade_type):
        """Aplica um upgrade ao jogador"""
        if upgrade_type == "speed":
            self.speed += 0.1  # Aumenta a velocidade
        elif upgrade_type == "attack_speed":
            self.attack_speed = max(200, self.attack_speed - 5)  # Reduz o tempo entre tiros
        elif upgrade_type == "attack_power":
            self.attack_power += 0.5  # Aumenta o dano do ataque
        elif upgrade_type == "health":
            self.health += 1  # Aumenta a vida

    def update(self):
        # Animação
        if self.animating:
            if self.direction in self.sprites:
                self.animation_frame += 1
                if self.animation_frame >= self.animation_speed * len(self.sprites[self.direction]):
                    self.animation_frame = 0
                sprite_index = self.animation_frame // self.animation_speed
                self.current_sprite = self.sprites[self.direction][sprite_index]
        else:
            self.current_sprite = self.sprites[self.direction][0]  # Parado

    def draw(self, screen):
        # Renderiza o jogador
        screen.blit(self.current_sprite, self.rect.topleft)
