import pygame
from src.entities.entity import Entity
from src.utils.constants import *


class Enemy(Entity):
    """Classe représentant un ennemi basique"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_SIZE[0], ENEMY_SIZE[1], 
                         ENEMY_HEALTH, ENEMY_SPEED)
        
        # Couleur temporaire de l'ennemi (rouge)
        self.image.fill((200, 0, 0))
        
        # IA
        self.detection_range = 200
        self.attack_range = 50
        self.attack_cooldown_timer = 0
        self.patrol_direction = 1  # 1 = droite, -1 = gauche
        self.patrol_distance = 100
        self.start_x = x
    
    def update(self, dt, player):
        """Met à jour l'ennemi"""
        # Cooldown d'attaque
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt * 1000
        
        # IA simple
        self.simple_ai(player)
        
        # Physique
        self.apply_gravity()
        self.move(dt)
        self.check_ground_collision()
    
    def simple_ai(self, player):
        """IA basique : patrouille et poursuite du joueur"""
        distance_to_player = abs(self.rect.centerx - player.rect.centerx)
        
        # Si le joueur est détecté
        if distance_to_player < self.detection_range:
            # Se déplacer vers le joueur
            if player.rect.centerx < self.rect.centerx:
                self.velocity_x = -self.speed
                self.facing_right = False
            else:
                self.velocity_x = self.speed
                self.facing_right = True
            
            # Attaquer si à portée
            if distance_to_player < self.attack_range and self.attack_cooldown_timer <= 0:
                self.attack(player)
        else:
            # Patrouille simple
            self.patrol()
    
    def patrol(self):
        """Fait patrouiller l'ennemi"""
        self.velocity_x = self.speed * self.patrol_direction
        
        # Changer de direction si trop loin du point de départ
        distance_from_start = abs(self.rect.x - self.start_x)
        if distance_from_start > self.patrol_distance:
            self.patrol_direction *= -1
            self.facing_right = not self.facing_right
    
    def attack(self, player):
        """Attaque le joueur"""
        self.attack_cooldown_timer = ATTACK_COOLDOWN
        
        # Infliger des dégâts au joueur
        if not player.is_rolling:  # Le joueur est invincible pendant la roulade
            player.take_damage(ENEMY_DAMAGE)
            print(f"Joueur touché ! Vie : {player.health}")