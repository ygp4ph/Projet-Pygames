import pygame
from src.entities.entity import Entity
from src.utils.constants import *


class Player(Entity):
    """Classe représentant le joueur avec des super-pouvoirs"""
    
    def __init__(self, x, y, character_type='hermes'):
        super().__init__(x, y, PLAYER_SIZE[0], PLAYER_SIZE[1], 
                         PLAYER_MAX_HEALTH, PLAYER_SPEED)
        
        # Type de personnage
        self.character_type = character_type
        self.character_data = CHARACTERS[character_type]
        
        # Couleur du personnage
        self.base_color = self.character_data['color']
        self.image.fill(self.base_color)
        
        # Vies
        self.lives = PLAYER_LIVES
        self.respawn_timer = 0
        self.is_respawning = False
        
        # Endurance
        self.stamina = PLAYER_MAX_STAMINA
        self.max_stamina = PLAYER_MAX_STAMINA
        
        # Roulade
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_direction = 0
        
        # Super pouvoirs
        self.power_active = False
        self.power_timer = 0
        self.power_cooldown = 0
        self.current_power = None
        
        # Knockback
        self.is_knocked_back = False
        self.knockback_timer = 0
        self.knockback_velocity_x = 0
    
    def update(self, dt, enemies, platform):
        """Met à jour le joueur"""
        # Si en respawn, ne rien faire
        if self.is_respawning:
            self.respawn_timer -= dt * 1000
            if self.respawn_timer <= 0:
                self.is_respawning = False
                self.health = self.max_health
            return
        
        # Régénération de l'endurance
        if self.stamina < self.max_stamina and not self.is_rolling and not self.power_active:
            self.stamina += PLAYER_STAMINA_REGEN
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
        
        # Gestion du knockback
        if self.is_knocked_back:
            self.knockback_timer -= dt * 1000
            if self.knockback_timer <= 0:
                self.is_knocked_back = False
                self.knockback_velocity_x = 0
            else:
                self.velocity_x = self.knockback_velocity_x
        
        # Gestion de la roulade
        if self.is_rolling:
            self.roll_timer -= dt * 1000
            if self.roll_timer <= 0:
                self.is_rolling = False
                self.velocity_x = 0
        
        # Gestion des super pouvoirs
        if self.power_active:
            self.power_timer -= dt * 1000
            if self.power_timer <= 0:
                self.deactivate_power()
        
        if self.power_cooldown > 0:
            self.power_cooldown -= dt * 1000
        
        # Si pas en roulade ni en knockback, on peut contrôler le joueur
        if not self.is_rolling and not self.is_knocked_back:
            self.handle_input(dt)
        
        # Physique
        self.apply_gravity()
        self.move(dt)
        
        # Vérifier collision avec la plateforme
        self.check_platform_collision(platform)
        
        # Vérifier si le joueur est tombé
        if self.rect.top > SCREEN_HEIGHT:
            self.die()
        
        # Cooldown d'attaque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt * 1000
        
        # Vérifier les collisions avec les ennemis
        self.check_enemy_collision(enemies)
    
    def handle_input(self, dt):
        """Gère les entrées clavier du joueur"""
        keys = pygame.key.get_pressed()
        
        # Multiplicateur de vitesse selon le pouvoir actif
        speed_mult = 1.0
        if self.power_active and self.current_power == 'vitesse':
            speed_mult = self.character_data['speed_multiplier']
        
        # Déplacement horizontal
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.velocity_x = -self.speed * speed_mult
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed * speed_mult
            self.facing_right = True
        
        # Saut
        jump_mult = 1.0
        if self.power_active and self.current_power == 'saut':
            jump_mult = self.character_data['jump_multiplier']
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.on_ground:
            self.velocity_y = -PLAYER_JUMP_FORCE * jump_mult
        
        # Attaque
        if keys[pygame.K_e] and self.attack_cooldown <= 0:
            if self.stamina >= ATTACK_STAMINA_COST:
                self.attack()
        
        # Roulade
        if keys[pygame.K_LSHIFT] and not self.is_rolling and self.on_ground:
            if self.stamina >= ROLL_STAMINA_COST:
                self.roll()
        
        # Activation des super pouvoirs (touches 1 et 2)
        if keys[pygame.K_1]:
            self.activate_power(self.character_data['powers'][0])
        if keys[pygame.K_2]:
            self.activate_power(self.character_data['powers'][1])
    
    def activate_power(self, power_type):
        """Active un super pouvoir"""
        if self.power_cooldown <= 0 and not self.power_active:
            if self.stamina >= SUPER_POWER_STAMINA_COST:
                self.power_active = True
                self.power_timer = SUPER_POWER_DURATION
                self.current_power = power_type
                self.stamina -= SUPER_POWER_STAMINA_COST
                
                # Effet visuel : changer la couleur
                if power_type == 'vitesse':
                    self.image.fill(YELLOW)
                elif power_type == 'force':
                    self.image.fill(RED)
                elif power_type == 'saut':
                    self.image.fill(BLUE)
                
                print(f"Super pouvoir activé : {power_type}")
    
    def deactivate_power(self):
        """Désactive le super pouvoir"""
        self.power_active = False
        self.power_cooldown = SUPER_POWER_COOLDOWN
        self.current_power = None
        self.image.fill(self.base_color)
        print("Super pouvoir désactivé")
    
    def attack(self):
        """Effectue une attaque"""
        self.is_attacking = True
        self.attack_cooldown = ATTACK_COOLDOWN
        self.stamina -= ATTACK_STAMINA_COST
    
    def roll(self):
        """Effectue une roulade"""
        self.is_rolling = True
        self.roll_timer = ROLL_DURATION
        self.stamina -= ROLL_STAMINA_COST
        
        if self.facing_right:
            self.velocity_x = PLAYER_SPEED * 3
        else:
            self.velocity_x = -PLAYER_SPEED * 3
    
    def apply_knockback(self, direction):
        """Applique un effet de recul"""
        if not self.is_rolling:  # Pas de knockback pendant la roulade
            self.is_knocked_back = True
            self.knockback_timer = KNOCKBACK_DURATION
            self.knockback_velocity_x = direction * KNOCKBACK_FORCE * 0.5
    
    def check_enemy_collision(self, enemies):
        """Vérifie les collisions avec les ennemis"""
        if self.is_attacking:
            for enemy in enemies:
                # Zone d'attaque
                attack_rect = pygame.Rect(
                    self.rect.right if self.facing_right else self.rect.left - 40,
                    self.rect.y,
                    40,
                    self.rect.height
                )
                
                if attack_rect.colliderect(enemy.rect):
                    # Dégâts selon le pouvoir de force
                    damage = ATTACK_DAMAGE
                    if self.power_active and self.current_power == 'force':
                        damage *= self.character_data['force_multiplier']
                    
                    enemy.take_damage(damage)
                    
                    # Appliquer knockback à l'ennemi
                    knockback_dir = 1 if self.facing_right else -1
                    knockback_strength = KNOCKBACK_FORCE
                    if self.power_active and self.current_power == 'force':
                        knockback_strength *= self.character_data['force_multiplier']
                    
                    enemy.apply_knockback(knockback_dir, knockback_strength)
                    print(f"Ennemi touché ! Vie : {enemy.health}")
            
            self.is_attacking = False
    
    def check_platform_collision(self, platform):
        """Vérifie la collision avec la plateforme"""
        if self.velocity_y > 0:  # Tombe vers le bas
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
    
    def die(self):
        """Le joueur perd une vie"""
        self.lives -= 1
        print(f"Vie perdue ! Vies restantes : {self.lives}")
        
        if self.lives > 0:
            # Respawn au centre
            self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
            self.rect.y = 200
            self.velocity_x = 0
            self.velocity_y = 0
            self.is_respawning = True
            self.respawn_timer = 2000  # 2 secondes
        else:
            # Game over
            self.health = 0
    
    def is_alive(self):
        """Vérifie si le joueur est vivant"""
        return self.lives > 0