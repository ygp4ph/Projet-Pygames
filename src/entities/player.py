import pygame
from src.entities.entity import Entity
from src.utils.constants import *


class Player(Entity):
    """Classe représentant le joueur"""
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE[0], PLAYER_SIZE[1], 
                         PLAYER_MAX_HEALTH, PLAYER_SPEED)
        
        # Couleur temporaire du joueur (bleu)
        self.image.fill((0, 100, 200))
        
        # Endurance
        self.stamina = PLAYER_MAX_STAMINA
        self.max_stamina = PLAYER_MAX_STAMINA
        
        # Roulade
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_direction = 0
    
    def update(self, dt, enemies):
        """Met à jour le joueur"""
        # Régénération de l'endurance
        if self.stamina < self.max_stamina and not self.is_rolling:
            self.stamina += PLAYER_STAMINA_REGEN
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
        
        # Gestion de la roulade
        if self.is_rolling:
            self.roll_timer -= dt * 1000
            if self.roll_timer <= 0:
                self.is_rolling = False
                self.velocity_x = 0
        
        # Si pas en roulade, on peut contrôler le joueur
        if not self.is_rolling:
            self.handle_input(dt)
        
        # Physique
        self.apply_gravity()
        self.move(dt)
        self.check_ground_collision()
        
        # Cooldown d'attaque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt * 1000
        
        # Vérifier les collisions avec les ennemis
        self.check_enemy_collision(enemies)
    
    def handle_input(self, dt):
        """Gère les entrées clavier du joueur"""
        keys = pygame.key.get_pressed()
        
        # Déplacement horizontal
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.velocity_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_right = True
        
        # Saut
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.on_ground:
            self.velocity_y = -PLAYER_JUMP_FORCE
        
        # Attaque
        if keys[pygame.K_e] and self.attack_cooldown <= 0:
            if self.stamina >= ATTACK_STAMINA_COST:
                self.attack()
        
        # Roulade
        if keys[pygame.K_LSHIFT] and not self.is_rolling and self.on_ground:
            if self.stamina >= ROLL_STAMINA_COST:
                self.roll()
    
    def attack(self):
        """Effectue une attaque"""
        self.is_attacking = True
        self.attack_cooldown = ATTACK_COOLDOWN
        self.stamina -= ATTACK_STAMINA_COST
        print("Attaque !")
    
    def roll(self):
        """Effectue une roulade"""
        self.is_rolling = True
        self.roll_timer = ROLL_DURATION
        self.stamina -= ROLL_STAMINA_COST
        
        # Direction de la roulade
        if self.facing_right:
            self.velocity_x = PLAYER_SPEED * 3
        else:
            self.velocity_x = -PLAYER_SPEED * 3
    
    def check_enemy_collision(self, enemies):
        """Vérifie les collisions avec les ennemis"""
        if self.is_attacking:
            for enemy in enemies:
                # Zone d'attaque simple (rectangle devant le joueur)
                attack_rect = pygame.Rect(
                    self.rect.right if self.facing_right else self.rect.left - 40,
                    self.rect.y,
                    40,
                    self.rect.height
                )
                
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(ATTACK_DAMAGE)
                    print(f"Ennemi touché ! Vie restante : {enemy.health}")
            
            self.is_attacking = False