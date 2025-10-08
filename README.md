# Dark Souls 2D

Un RPG 2D inspiré de Dark Souls, développé en Python avec Pygame.

## Description

Dark Souls 2D est un jeu d'action-RPG en vue de côté où vous incarnez un guerrier qui doit affronter des ennemis dans un monde sombre et dangereux. Le jeu reprend les mécaniques emblématiques de Dark Souls : combat au corps à corps, système d'endurance, roulade esquive, et collecte d'âmes.

## Fonctionnalités

* ✅ Système de combat avec attaques et esquives
* ✅ Gestion de la vie et de l'endurance
* ✅ IA des ennemis avec patrouille et poursuite
* ✅ Système de score (âmes)
* ✅ Sauvegarde et chargement de partie
* ✅ Interface utilisateur affichant les statistiques

## Prérequis

* Python 3.8 ou supérieur
* pip (gestionnaire de paquets Python)

## Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone [URL_DU_PROJET]
   cd dark_souls_2d
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## Lancer le jeu

Pour démarrer le jeu, exécutez simplement :

```bash
python main.py
```

## Contrôles

### Déplacements

* **Q** ou **Flèche Gauche** : Se déplacer à gauche
* **D** ou **Flèche Droite** : Se déplacer à droite
* **ESPACE** ou **Z** : Sauter

### Actions

* **E** : Attaquer (coûte de l'endurance)
* **SHIFT Gauche** : Roulade/Esquive (coûte de l'endurance, donne l'invincibilité temporaire)

### Menu

* **ESC** : Mettre en pause
* **F5** : Sauvegarder la partie
* **F9** : Charger la sauvegarde

## Structure du projet

```
dark_souls_2d/
├── main.py                 # Point d'entrée du jeu
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
├── assets/                # Ressources (sprites, sons, maps)
├── src/                   # Code source
│   ├── game.py           # Classe Game principale
│   ├── entities/         # Entités (joueur, ennemis)
│   ├── world/            # Gestion du monde
│   ├── ui/               # Interface utilisateur
│   └── utils/            # Utilitaires et constantes
└── saves/                # Fichiers de sauvegarde
```

## Système de jeu

### Combat

* Chaque attaque consomme de l'endurance
* La roulade permet d'esquiver les attaques et rend invincible pendant sa durée
* L'endurance se régénère automatiquement

### Score (Âmes)

* Tuez des ennemis pour gagner des âmes
* Ennemi normal : 100 âmes
* Boss : 1000 âmes (à venir)

### Sauvegarde

* Appuyez sur **F5** pour sauvegarder
* La sauvegarde conserve votre position, vos statistiques et l'état des ennemis
* Appuyez sur **F9** pour charger la dernière sauvegarde

## À venir

* [ ]  Maps avec Tiled
* [ ]  Plus de types d'ennemis
* [ ]  Boss avec patterns d'attaque
* [ ]  Système d'items et d'équipement
* [ ]  Amélioration des animations
* [ ]  Sons et musique
* [ ]  Feux de camp (points de sauvegarde)

## Développement

Ce projet a été développé dans le cadre d'un exercice de programmation orientée objet avec Pygame.

### Technologies utilisées

* **Python 3.x**
* **Pygame 2.5.2** - Bibliothèque de développement de jeux
* **pytmx 3.32** - Lecture de maps Tiled (à venir)

## Auteurs

* Votre équipe de 3 personnes

## Licence

Projet éducatif - Tous droits réservés
