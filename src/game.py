import pygame
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.world.platform import Platform
from src.ui.hud import HUD
from src.utils.constants import *
from src.utils.save_manager import SaveManager


class Game:
    """Classe principale du jeu avec sélection de personnage"""
    
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.game_state = "character_select"  # character_select, playing, game_over, pause_menu
        self.souls = 0
        
        # Sélection de personnage
        self.selected_character = 0
        self.character_keys = list(CHARACTERS.keys())
        
        # Boutons pour les menus
        self.selected_button = 0
        self.pause_button_count = 2
        
        # Gestionnaire de sauvegarde
        self.save_manager = SaveManager()
        
        # Plateforme
        self.platform = Platform()
        
        # Initialiser à None, sera créé après sélection du personnage
        self.player = None
        self.enemies = []
        self.all_sprites = pygame.sprite.Group()
        self.hud = None
    
    def init_game(self, character_type):
        """Initialise le jeu avec le personnage choisi"""
        # Création du joueur au centre de la plateforme
        spawn_x = PLATFORM_X + PLATFORM_WIDTH // 2
        spawn_y = PLATFORM_Y - 100
        self.player = Player(spawn_x, spawn_y, character_type)
        
        # Ennemis sur la plateforme
        self.enemies = [
            Enemy(PLATFORM_X + 100, PLATFORM_Y - 100),
            Enemy(PLATFORM_X + PLATFORM_WIDTH - 150, PLATFORM_Y - 100)
        ]
        
        # Interface
        self.hud = HUD(self)
        
        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        for enemy in self.enemies:
            self.all_sprites.add(enemy)
        
        self.souls = 0
    
    def handle_event(self, event):
        """Gère les événements"""
        if event.type == pygame.KEYDOWN:
            # Sélection de personnage
            if self.game_state == "character_select":
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    self.selected_character = (self.selected_character - 1) % 3
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.selected_character = (self.selected_character + 1) % 3
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    character_type = self.character_keys[self.selected_character]
                    self.init_game(character_type)
                    self.game_state = "playing"
            
            # Pause
            elif self.game_state == "pause_menu":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % self.pause_button_count
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % self.pause_button_count
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.handle_pause_menu_selection()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "playing"
                    self.selected_button = 0
            
            # Game over
            elif self.game_state == "game_over":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % 2
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_button == 0:  # Rejouer
                        self.game_state = "character_select"
                        self.selected_character = 0
                    elif self.selected_button == 1:  # Quitter
                        self.running = False
            
            # En jeu
            elif self.game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "pause_menu"
                    self.selected_button = 0
    
    def handle_pause_menu_selection(self):
        """Gère le menu pause"""
        if self.selected_button == 0:  # Reprendre
            self.game_state = "playing"
            self.selected_button = 0
        elif self.selected_button == 1:  # Menu principal
            self.game_state = "character_select"
            self.selected_button = 0
            self.selected_character = 0
    
    def update(self, dt):
        """Met à jour le jeu"""
        if self.game_state != "playing":
            return
        
        # Mise à jour du joueur
        self.player.update(dt, self.enemies, self.platform)
        
        # Vérifier si le joueur est mort
        if not self.player.is_alive():
            self.game_state = "game_over"
            self.selected_button = 0
            return
        
        # Mise à jour des ennemis
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player, self.platform)
            
            # Si l'ennemi est mort
            if enemy.is_dead or enemy.health <= 0:
                self.souls += ENEMY_KILL_SOULS
                self.enemies.remove(enemy)
                self.all_sprites.remove(enemy)
        
        # Respawn des ennemis s'il n'y en a plus
        if len(self.enemies) == 0:
            self.spawn_new_enemies()
    
    def spawn_new_enemies(self):
        """Fait apparaître de nouveaux ennemis"""
        self.enemies = [
            Enemy(PLATFORM_X + 100, PLATFORM_Y - 100),
            Enemy(PLATFORM_X + PLATFORM_WIDTH - 150, PLATFORM_Y - 100)
        ]
        for enemy in self.enemies:
            self.all_sprites.add(enemy)
    
    def render(self):
        """Affiche le jeu"""
        if self.game_state == "character_select":
            self.render_character_select()
        elif self.game_state == "playing":
            self.render_game()
        elif self.game_state == "pause_menu":
            self.render_game()
            self.render_pause_menu()
        elif self.game_state == "game_over":
            self.render_game_over()
    
    def render_character_select(self):
        """Affiche l'écran de sélection de personnage"""
        self.screen.fill(BLACK)
        
        # Titre
        title_font = pygame.font.Font(None, 80)
        title = title_font.render("CHOISIS TON HEROS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Afficher les 3 personnages
        char_width = 250
        char_spacing = 50
        start_x = (SCREEN_WIDTH - (char_width * 3 + char_spacing * 2)) // 2
        
        for i, char_key in enumerate(self.character_keys):
            char_data = CHARACTERS[char_key]
            x = start_x + i * (char_width + char_spacing)
            y = 200
            
            # Boîte du personnage
            is_selected = (i == self.selected_character)
            border_color = YELLOW if is_selected else WHITE
            border_width = 5 if is_selected else 2
            
            # Fond du personnage
            pygame.draw.rect(self.screen, DARK_GRAY, (x, y, char_width, 350))
            pygame.draw.rect(self.screen, border_color, (x, y, char_width, 350), border_width)
            
            # Rectangle coloré représentant le personnage
            char_rect_size = 80
            char_rect_x = x + (char_width - char_rect_size) // 2
            char_rect_y = y + 30
            pygame.draw.rect(self.screen, char_data['color'], 
                           (char_rect_x, char_rect_y, char_rect_size, char_rect_size * 2))
            
            # Nom du personnage
            name_font = pygame.font.Font(None, 50)
            name = name_font.render(char_data['name'], True, WHITE)
            name_rect = name.get_rect(center=(x + char_width // 2, y + 220))
            self.screen.blit(name, name_rect)
            
            # Pouvoirs
            power_font = pygame.font.Font(None, 30)
            powers_text = " + ".join([p.capitalize() for p in char_data['powers']])
            powers = power_font.render(powers_text, True, char_data['color'])
            powers_rect = powers.get_rect(center=(x + char_width // 2, y + 270))
            self.screen.blit(powers, powers_rect)
            
            # Stats
            stats_font = pygame.font.Font(None, 24)
            stats = [
                f"Vitesse: x{char_data['speed_multiplier']}",
                f"Force: x{char_data['force_multiplier']}",
                f"Saut: x{char_data['jump_multiplier']}"
            ]
            for j, stat in enumerate(stats):
                stat_text = stats_font.render(stat, True, GRAY)
                stat_rect = stat_text.get_rect(center=(x + char_width // 2, y + 300 + j * 20))
                self.screen.blit(stat_text, stat_rect)
        
        # Instructions
        info_font = pygame.font.Font(None, 35)
        info = info_font.render("Q/D pour choisir | ENTREE pour commencer", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(info, info_rect)
        
        # Info sur les contrôles
        controls_font = pygame.font.Font(None, 28)
        controls = controls_font.render("Touches 1 et 2 pour activer les super pouvoirs", True, GRAY)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(controls, controls_rect)
    
    def render_game(self):
        """Affiche le jeu en cours"""
        # Fond (ciel)
        self.screen.fill((50, 150, 200))
        
        # Plateforme
        self.platform.render(self.screen)
        
        # Sprites
        self.all_sprites.draw(self.screen)
        
        # Barres de vie des ennemis
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)
        
        # HUD
        self.hud.render(self.screen)
        
        # Si en respawn, afficher message
        if self.player.is_respawning:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(100)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            font = pygame.font.Font(None, 80)
            text = font.render("RESPAWN...", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
    
    def render_pause_menu(self):
        """Affiche le menu pause"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        title_font = pygame.font.Font(None, 100)
        title = title_font.render("PAUSE", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons = ["Reprendre", "Menu Principal"]
        
        for i, text in enumerate(buttons):
            color = YELLOW if i == self.selected_button else WHITE
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 80))
            self.screen.blit(button, button_rect)
        
        # Instructions
        info_font = pygame.font.Font(None, 30)
        info = info_font.render("Z/S | ENTREE | ESC", True, GRAY)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(info, info_rect)
    
    def render_game_over(self):
        """Affiche l'écran Game Over"""
        self.screen.fill(BLACK)
        
        # Titre
        title_font = pygame.font.Font(None, 120)
        title = title_font.render("YOU DIED", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Score
        score_font = pygame.font.Font(None, 50)
        score = score_font.render(f"Ames: {self.souls}", True, WHITE)
        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score, score_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons = ["Rejouer", "Quitter"]
        
        for i, text in enumerate(buttons):
            color = YELLOW if i == self.selected_button else WHITE
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 420 + i * 80))
            self.screen.blit(button, button_rect)