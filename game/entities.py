import pygame
import random
from .utils import draw_text, draw_health_bar

class Character:
    def __init__(self, name, max_hp, attack, defense, x, y, color):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.x = x
        self.y = y
        self.color = color
    
    def attack_target(self, target):
        damage = max(1, self.attack - target.defense + random.randint(-5, 5))
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage
    
    def is_alive(self):
        return self.hp > 0
    
    def draw(self, screen):
        # Représentation temporaire (carré coloré)
        pygame.draw.rect(screen, self.color, (self.x, self.y, 80, 80), 0)
        pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y, 80, 80), 2)
        
        # Nom
        draw_text(screen, self.name, self.x, self.y - 25, (255, 255, 255), 24)
        
        # Barre de vie
        draw_health_bar(screen, self.x, self.y + 85, 80, 10, self.hp / self.max_hp)
        
        # Points de vie
        draw_text(screen, f"{self.hp}/{self.max_hp}", self.x, self.y + 100, (255, 255, 255), 20)

class Player(Character):
    def __init__(self, name, max_hp, attack, defense, x, y, color):
        super().__init__(name, max_hp, attack, defense, x, y, color)
        self.is_player = True
    
    def special_attack(self, target):
        damage = int(self.attack * 1.5) - target.defense
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage

class Enemy(Character):
    def __init__(self, name, max_hp, attack, defense, x, y, color):
        super().__init__(name, max_hp, attack, defense, x, y, color)
        self.is_player = False