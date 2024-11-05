import pygame
import os

class Player:
    def __init__(self, x, y, speed, scale_factor=2.0):  # Adicione scale_factor como parâmetro
        # Carrega o tileset
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

        # Inicializa a animação
        self.current_sprite = self.sprites['down'][0]
        self.rect = self.current_sprite.get_rect(center=(x, y))
        self.speed = speed
        self.direction = 'down'
        self.animation_frame = 0
        self.animation_speed = 10  # Quão rápido a animação muda
        self.animating = False

    def move(self, keys):
        # Movimenta o jogador com suporte para movimento diagonal
        original_rect = self.rect.copy()  # Salva a posição original para checar colisões
        move_x = 0
        move_y = 0

        if keys[pygame.K_LEFT]:
            move_x = -self.speed
            self.direction = 'left'
            self.animating = True
        elif keys[pygame.K_RIGHT]:
            move_x = self.speed
            self.direction = 'right'
            self.animating = True
        
        if keys[pygame.K_UP]:
            move_y = -self.speed
            self.direction = 'up'
            self.animating = True
        elif keys[pygame.K_DOWN]:
            move_y = self.speed
            self.direction = 'down'
            self.animating = True

        # Atualiza a posição do jogador
        self.rect.x += move_x
        self.rect.y += move_y

        # Limitar o jogador à tela
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 800 - self.rect.width:  # 800 é a largura da tela
            self.rect.x = 800 - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 600 - self.rect.height:  # 600 é a altura da tela
            self.rect.y = 600 - self.rect.height

        # Verifica se não está se movendo e para a animação
        if not (move_x or move_y):
            self.animating = False

    def update(self):
        if self.animating:
            # Atualiza o sprite atual baseado na direção e na animação
            if self.direction in self.sprites:
                self.animation_frame += 1
                if self.animation_frame >= self.animation_speed * len(self.sprites[self.direction]):
                    self.animation_frame = 0
                sprite_index = self.animation_frame // self.animation_speed
                self.current_sprite = self.sprites[self.direction][sprite_index]
        else:
            # Se não está se movendo, mantém o sprite atual na posição final da animação
            self.current_sprite = self.sprites[self.direction][0]  # Ou pode ser o sprite de parada

    def draw(self, screen):
        screen.blit(self.current_sprite, self.rect.topleft)
