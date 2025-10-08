# Constantes du jeu Dark Souls 2D

# Fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Dark Souls 2D - Battle Arena"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (200, 0, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Plateforme
PLATFORM_WIDTH = 800
PLATFORM_HEIGHT = 40
PLATFORM_X = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
PLATFORM_Y = 400

# Joueur
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = 15
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_STAMINA = 100
PLAYER_STAMINA_REGEN = 1
PLAYER_SIZE = (32, 64)
PLAYER_LIVES = 3

# Personnages et leurs capacités
CHARACTERS = {
    'hermes': {
        'name': 'Hermès',
        'color': YELLOW,
        'powers': ['vitesse', 'saut'],
        'speed_multiplier': 2.5,
        'jump_multiplier': 1.8,
        'force_multiplier': 1.0
    },
    'hercule': {
        'name': 'Hercule',
        'color': RED,
        'powers': ['force', 'saut'],
        'speed_multiplier': 1.0,
        'jump_multiplier': 1.8,
        'force_multiplier': 2.0
    },
    'atlas': {
        'name': 'Atlas',
        'color': ORANGE,
        'powers': ['force', 'vitesse'],
        'speed_multiplier': 2.0,
        'jump_multiplier': 1.0,
        'force_multiplier': 2.0
    }
}

# Super pouvoirs
SUPER_POWER_DURATION = 3000  # 3 secondes
SUPER_POWER_COOLDOWN = 10000  # 10 secondes
SUPER_POWER_STAMINA_COST = 50

# Ennemis
ENEMY_SPEED = 2
ENEMY_HEALTH = 50
ENEMY_DAMAGE = 10
ENEMY_SIZE = (32, 64)

# Physique
GRAVITY = 0.8
MAX_FALL_SPEED = 20

# Combat
ATTACK_DAMAGE = 20
ATTACK_COOLDOWN = 500  # millisecondes
ATTACK_STAMINA_COST = 20
ROLL_STAMINA_COST = 25
ROLL_DISTANCE = 150
ROLL_DURATION = 300  # millisecondes

# Knockback
KNOCKBACK_FORCE = 15  # Force de recul
KNOCKBACK_DURATION = 200  # Durée du recul en ms

# Score
ENEMY_KILL_SOULS = 100
BOSS_KILL_SOULS = 1000

# Fichiers
SAVE_FILE = "saves/save_game.json"