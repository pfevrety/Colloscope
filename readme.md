# Colloscope Generator

Programme permettant de générer un coloscope pour la MPSI 2 du lycée Charlemagne (1er semestre).

## Description
Ce programme génère automatiquement un colloscope avec les fonctionnalités suivantes :
- Gestion des indisponibilités régulières (ex. : cours de LV2).
- Gestion des indisponibilités exceptionnelles (ex. : rendez-vous médical d'un élève le jeudi après-midi).
- Gestion des groupes de SI.
- Roulement des groupes de TD de Français.
- Gestion des groupes de TP d'informatique.

## Prérequis
Pour utiliser le programme, vous devez installer la librairie Jinja2 et vous assurer que SQLite3 est disponible (inclus dans la bibliothèque standard de Python).

Installation de Jinja2 :
```bash
pip install Jinja2
```

# Instructions d'utilisation
## Initialisation de la base de données
Pour initialiser la base de données, exécutez la commande suivante :
```bash
python db.py
```
Cette base de données contiendra les colleurs et leurs horaires, les élèves et leurs indisponibilités régulières, ainsi que les trinômes de colles.

# Lancement du programme
## Pour lancer le programme, utilisez la commande suivante :

```bash
python main.py
```

Le programme vous demandera si vous souhaitez ajouter des indisponibilités exceptionnelles pour un élève. Pour ce faire, indiquez l'ID du trinôme de colle de l'élève (si vous ne connaissez pas cet ID, tapez ``list_id``) et suivez les instructions.

Le programme effectuera plusieurs itérations pour générer un colloscope respectant toutes les contraintes. Le résultat sera sauvegardé sous la forme d'un fichier HTML nommé emploi_du_temps.html, que vous pourrez ouvrir avec n'importe quel navigateur.

Le programme est conçu pour fonctionner correctement durant tout le premier semestre. Le support pour le second semestre sera ajouté ultérieurement.

## Remarque
Pour passer d'une semaine à l'autre et effectuer les roulements, incrémentez manuellement de 1 la valeur de numero_semaine dans le fichier ``infosemaine.json``.


# Contributing
Les contributions sont les bienvenues. Veuillez soumettre un pull request ou ouvrir une issue pour discuter des changements majeurs.

