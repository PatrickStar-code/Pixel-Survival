import pygame
import random
import os
import math

from enemy import Enemy  # Minions que o Boss invocará
from projectile import Projectile

class Boss(Enemy):
    def __init__(self, dificulty ,player, speed, screen_width, screen_height, scale_factor=2.0):
        # Carregar o tileset do Boss
        tileset_path = os.path.join("assets/images/enemy", "bossTileSet.png")
        tileset = pygame.image.load(tileset_path)
        
        # Configuração do sprite do Boss
        frame_width = 74
        frame_height = 74
        num_frames = 1  
        
        # Extrair a imagem do boss
        self.images = []
        for i in range(num_frames):
            frame = tileset.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.images.append(pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor)))

        # Tamanho da tela (tela onde o Boss deve aparecer)
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Definindo o tamanho inicial do Boss, mas sem o rect definido ainda
        self.rect = pygame.Rect(0, 0, self.images[0].get_width(), self.images[0].get_height())

        # Agora chamamos spawn_outside_screen para definir a posição inicial
        self.rect = self.spawn_outside_screen()

        # Atributos de movimento e direção
        self.dificulty = dificulty
        self.speed = speed
        self.player = player
        self.animation_frame = 0
        self.animation_speed = 10
        self.current_sprite = self.images[0]
        self.health = 50 * dificulty  

        print(self.health)

        # Padrões de ataque
        self.attack_pattern = 0
        self.attack_types = ["shoot", "summon"]
        
        # Lista para projéteis e minions
        self.projectiles = []
        self.minions = []  # Para armazenar minions invocados

        # Controladores de delay
        self.shoot_delay = 60
        self.time_since_last_shot = 0
        self.summon_delay = 10000  # Intervalo para invocar minions (5 segundos)
        self.time_since_last_summon = 0

        # Controle de tempo de troca de ataque
        self.attack_switch_delay = 300  # Intervalo entre trocas de ataques (em frames)
        self.attack_switch_counter = 0

    def spawn_outside_screen(self):
        """ Coloca o Boss fora da tela, mas perto da borda para que apareça rapidamente. """
        edge = random.choice(["left", "right", "top", "bottom"])

        if edge == "left":
            return pygame.Rect(-self.rect.width, random.randint(0, self.screen_height), self.rect.width, self.rect.height)
        elif edge == "right":
            return pygame.Rect(self.screen_width + self.rect.width, random.randint(0, self.screen_height), self.rect.width, self.rect.height)
        elif edge == "top":
            return pygame.Rect(random.randint(0, self.screen_width), -self.rect.height, self.rect.width, self.rect.height)
        elif edge == "bottom":
            return pygame.Rect(random.randint(0, self.screen_width), self.screen_height + self.rect.height, self.rect.width, self.rect.height)

    def attack(self):
        if self.attack_types[self.attack_pattern] == "shoot":
            self.shoot_projectile()
        elif self.attack_types[self.attack_pattern] == "summon":
            self.summon_minions()

    def shoot_projectile(self):
        # Dispara projéteis em direção ao jogador
        if self.time_since_last_shot >= self.shoot_delay:
            projectile = Projectile(self.rect.centerx, self.rect.centery, self.player)
            self.projectiles.append(projectile)
            self.time_since_last_shot = 0
        else:
            self.time_since_last_shot += 1

    def summon_minions(self):
        # Invoca 5 minions próximos ao Boss
        if self.time_since_last_summon >= self.summon_delay:
            for _ in range(5):
                minion_x = self.rect.centerx + random.randint(-50, 50)
                minion_y = self.rect.centery + random.randint(-50, 50)
                minion = Enemy(self.player, self.speed, self.rect.width, self.rect.height)
                minion.rect.center = (minion_x, minion_y)
                self.minions.append(minion)
            self.time_since_last_summon = 0
            print("Boss is summoning minions!")
        else:
            self.time_since_last_summon += 1

    def update(self):
        # Atualiza o comportamento do Boss: segue o jogador
        self.move_towards_player()
        
        # Atualiza o contador de troca de ataque
        self.attack_switch_counter += 1
        if self.attack_switch_counter >= self.attack_switch_delay:
            # Altera o padrão de ataque após o intervalo
            self.attack_pattern = (self.attack_pattern + 1) % len(self.attack_types)
            self.attack_switch_counter = 0  # Reseta o contador

        # Executa o ataque atual
        self.attack()

        # Atualiza os projéteis disparados
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.rect.colliderect(self.player.rect):
                self.player.health -= 1
                self.projectiles.remove(projectile)

        # Atualiza minions invocados
        for minion in self.minions[:]:
            minion.update()
            if minion.rect.colliderect(self.player.rect):
                self.player.health -= 1
                self.minions.remove(minion)

        # Atualiza a animação
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

        # Desenha os minions invocados
        for minion in self.minions:
            minion.draw(screen)

    def move_towards_player(self):
        """ Movimenta o Boss em direção ao jogador. Essa é a movimentação padrão do Boss. """
        # O Boss sempre tenta se mover em direção ao jogador
        direction_x = self.player.rect.centerx - self.rect.centerx
        direction_y = self.player.rect.centery - self.rect.centery
        angle = math.atan2(direction_y, direction_x)

        # Movimentação contínua em direção ao jogador
        self.rect.x += int(math.cos(angle) * self.speed)
        self.rect.y += int(math.sin(angle) * self.speed)
