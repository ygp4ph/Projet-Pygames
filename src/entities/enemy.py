import pygame
from src.entities.entity import Entity
from src.utils.constants import *


class Enemy(Entity):
    """Classe représentant un ennemi avec knockback"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_SIZE[0], ENEMY_SIZE[1], 
                         ENEMY_HEALTH, ENEMY_SPEED)
        
        # Couleur rouge pour les ennemis
        self.image.fill((200, 0, 0))
        
        # IA
        self.detection_range = 200
        self.attack_range = 50
        self.attack_cooldown_timer = 0
        self.patrol_direction = 1
        self.patrol_distance = 100
        self.start_x = x
        
        # Knockback
        self.is_knocked_back = False
        self.knockback_timer = 0
        self.knockback_velocity_x = 0
        self.is_dead = False
    
    def update(self, dt, player, platform):
        """Met à jour l'ennemi"""
        if self.is_dead:
            return
        
        # Cooldown d'attaque
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt * 1000
        
        # Gestion du knockback
        if self.is_knocked_back:
            self.knockback_timer -= dt * 1000
            if self.knockback_timer <= 0:
                self.is_knocked_back = False
                self.knockback_velocity_x = 0
            else:
                self.velocity_x = self.knockback_velocity_x
        else:
            # IA simple si pas en knockback
            self.simple_ai(player, platform)
        
        # Physique
        self.apply_gravity()
        self.move(dt)
        
        # Vérifier collision avec la plateforme
        self.check_platform_collision(platform)
        
        # Vérifier si l'ennemi est tombé
        if self.rect.top > SCREEN_HEIGHT:
            self.is_dead = True
            self.health = 0
            print("Un ennemi est tombé dans le vide !")
    
    def simple_ai(self, player, platform):
        """IA : reste sur la plateforme et poursuit le joueur"""
        distance_to_player = abs(self.rect.centerx - player.rect.centerx)
        
        # Si le joueur est détecté
        if distance_to_player < self.detection_range:
            # Se déplacer vers le joueur mais rester sur la plateforme
            if player.rect.centerx < self.rect.centerx:
                # Vérifier qu'on ne va pas tomber à gauche
                if self.rect.left > platform.rect.left + 30:
                    self.velocity_x = -self.speed
                    self.facing_right = False
                else:
                    self.velocity_x = 0
            else:
                # Vérifier qu'on ne va pas tomber à droite
                if self.rect.right < platform.rect.right - 30:
                    self.velocity_x = self.speed
                    self.facing_right = True
                else:
                    self.velocity_x = 0
            
            # Attaquer si à portée
            if distance_to_player < self.attack_range and self.attack_cooldown_timer <= 0:
                self.attack(player)
        else:
            # Patrouille sur la plateforme
            self.patrol(platform)
    
    def patrol(self, platform):
        """Patrouille sur la plateforme"""
        self.velocity_x = self.speed * self.patrol_direction
        
        # Changer de direction aux bords de la plateforme
        if self.rect.left <= platform.rect.left + 20:
            self.patrol_direction = 1
            self.facing_right = True
        elif self.rect.right >= platform.rect.right - 20:
            self.patrol_direction = -1
            self.facing_right = False
    
    def attack(self, player):
        """Attaque le joueur"""
        self.attack_cooldown_timer = ATTACK_COOLDOWN
        
        if not player.is_rolling and not player.is_respawning:
            player.take_damage(ENEMY_DAMAGE)
            # Knockback sur le joueur
            knockback_dir = 1 if self.facing_right else -1
            player.apply_knockback(knockback_dir)
            print(f"Joueur touché ! Vie : {player.health}")
    
    def apply_knockback(self, direction, force):
        """Applique un effet de recul à l'ennemi"""
        self.is_knocked_back = True
        self.knockback_timer = KNOCKBACK_DURATION
        self.knockback_velocity_x = direction * force
        print("Ennemi repoussé !")
    
    def check_platform_collision(self, platform):
        """Vérifie la collision avec la plateforme"""
        if self.velocity_y > 0:
            if (self.rect.bottom >= platform.rect.top and 
                self.rect.bottom <= platform.rect.top + 20 and
                self.rect.right > platform.rect.left and 
                self.rect.left < platform.rect.right):
                
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
        else:
            self.on_ground = False