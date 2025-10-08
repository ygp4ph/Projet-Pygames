import pygame
from src.utils.constants import *


class Entity(pygame.sprite.Sprite):
    """Classe parent pour toutes les entités du jeu (joueur, ennemis)"""
    
    def __init__(self, x, y, width, height, health, speed):
        super().__init__()
        
        # Position et dimensions
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Statistiques
        self.health = health
        self.max_health = health
        self.speed = speed
        
        # Physique
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Combat
        self.is_attacking = False
        self.attack_cooldown = 0
        self.facing_right = True
    
    def apply_gravity(self):
        """Applique la gravité à l'entité"""
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
    
    def check_ground_collision(self):
        """Vérifie si l'entité touche le sol (temporaire)"""
        ground_y = 500 - self.rect.height
        if self.rect.y >= ground_y:
            self.rect.y = ground_y
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def move(self, dt):
        """Déplace l'entité en fonction de sa vélocité"""
        self.rect.x += self.velocity_x * dt * 60
        self.rect.y += self.velocity_y * dt * 60
        
        # Limites de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def take_damage(self, damage):
        """Inflige des dégâts à l'entité"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def is_alive(self):
        """Vérifie si l'entité est vivante"""
        return self.health > 0
    
    def draw_health_bar(self, surface):
        """Dessine la barre de vie au-dessus de l'entité"""
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        # Fond de la barre (rouge)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Barre de vie (verte)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_width, bar_height))