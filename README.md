# Centre échecs

Application de gestion de tournoi d'échec, autonome et hors-ligne, fonctionnant via une interface en ligne de commande.


## Fonctionnalités

- Enregistrement et sauvegarde des joueurs avec leur identifiant national d'échec ;
- Création et gestion complète de tournoi ;
- Génération automatique des paires de joueurs pour chaque tour, en fonction des scores ;
- Sauvegarde et chargement de l'état d'un tournoi en cours ;
- Génération et export de rapports concernant les joueurs et les tournois au format HTML.

## Prérequis

- Python `3.8+`;
- (Optionnel) Git pour clôner le dépôt ;
- Compatible avec n'importe quel OS (Windows/Linux/macOS).

## Installation

- Cloner ou sauvegarder le dépôt dans le répertoire de travail de votre choix.
- (Optionnel) installer les dépendances pour améliorer le visuel de la console.
Pour ce faire, dans le répertoire de travail:

```bash
pip install -r requirements.txt
```

## Usage

Lancer l'application depuis le répertoire de travail:

```bash
python main.py # Ou py main.py
```
Lors de la génération de rapports des tournois au format HTML, le fichier sera installé dans le répertoire courant sous ./RAPPORTS.html

## Architecture maintenabilité du code

- Architecture MVC pour une séparation claire des responsabilités ;
- Respect des normes PEP-8 ;
- Rapport de conformité PEP-8 disponible via Flake8.

### Générer un nouveau rapport Flake-8

- Nécessite Flake8 `5.0.0+`
Pur ce faire, dans le répertoire de travail:

```bash
flake8
```
Le fichier .html sera installé sous ./flake8_report/index.html

