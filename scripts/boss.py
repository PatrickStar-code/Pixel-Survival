import pygame
import random
import os
import math

from enemy import Enemy
from projectile import Projectile

class Boss(Enemy):
    def __init__(self, player, speed, screen_width, screen_height, scale_factor=2.0):
        # Carregar o tileset do Boss
        tileset_path = os.path.join("assets/images/enemy", "bossTileSet.png")
        tileset = pygame.image.load(tileset_path)
        
        # Suponha que o tileset tem as animações do Boss dispostas horizontalmente
        frame_width = 74 # Largura de cada frame
        frame_height = 74  # Altura de cada frame
        num_frames = 1 # Número de frames na animação
        
        # Extrair as primeiras imagens do tileset
        self.images = []
        for i in range(num_frames):
            frame = tileset.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.images.append(pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor)))

        # Iniciar o Boss com a posição fora da tela
        self.rect = self.spawn_outside_screen(screen_width, screen_height)

        # Definir variáveis de movimento e direção
        self.speed = speed
        self.player = player
        self.animation_frame = 0
        self.animation_speed = 10  # Velocidade de animação
        self.current_sprite = self.images[0]
        self.health = 10  # O Boss tem mais vida
        self.attack_pattern = 0  # Inicia com um padrão de ataque

        # Padrões de ataque, como por exemplo:
        self.attack_types = ["shoot", "charge", "summon"]

        # Lista para armazenar projéteis disparados pelo Boss
        self.projectiles = []

        # Controladores de delay de disparo
        self.shoot_delay = 60  # Delay entre disparos (em quadros, 60 quadros = 1 segundo)
        self.time_since_last_shot = 0  # Controle do tempo desde o último disparo

    def attack(self):
        # Dependendo do padrão de ataque, o Boss faz algo diferente
        if self.attack_types[self.attack_pattern] == "shoot":
            self.shoot_projectile()  # Lança projéteis
        elif self.attack_types[self.attack_pattern] == "charge":
            self.charge_attack()  # Avança em direção ao jogador
        elif self.attack_types[self.attack_pattern] == "summon":
            self.summon_minions()  # Invoca minions para ajudar

    def shoot_projectile(self):
        # Lógica para disparar projéteis
        if self.time_since_last_shot >= self.shoot_delay:
            projectile = Projectile(self.rect.centerx, self.rect.centery, self.player)
            self.projectiles.append(projectile)
            print("Boss is shooting projectiles!")
            self.time_since_last_shot = 0
        else:
            self.time_since_last_shot += 1  # Aumenta o tempo a cada quadro

    def charge_attack(self):
        # Lógica para o ataque de carga
        print("Boss is charging at the player!")

    def summon_minions(self):
        # Lógica para invocar minions
        print("Boss is summoning minions!")

    def update(self):
        # Atualiza a posição e o ataque
        self.move_towards_player()
        self.attack()  # Chama o ataque conforme o padrão

        # Atualiza os projéteis disparados
        for projectile in self.projectiles[:]:
            projectile.update()

            # Verifica se o projétil colidiu com o jogador
            if projectile.rect.colliderect(self.player.rect):
                self.player.health -= 1
                print(f"Player hit by projectile! Player health: {self.player.health}")
                self.projectiles.remove(projectile)

        # Atualiza o frame de animação
        self.animation_frame += 1
        if self.animation_frame >= self.animation_speed * len(self.images):
            self.animation_frame = 0
        sprite_index = self.animation_frame // self.animation_speed
        self.current_sprite = self.images[sprite_index]

    def draw(self, screen):
        # Desenha o Boss na tela
        screen.blit(self.current_sprite, self.rect.topleft)

        # Desenha os projéteis disparados
        for projectile in self.projectiles:
            projectile.draw(screen)
