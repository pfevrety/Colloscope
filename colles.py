import json
import random
import sqlite3
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader


MAX_ITERATIONS = 50

conn = sqlite3.connect('colloscope1.db')
cursor = conn.cursor()


def charger_donnees():
    cursor.execute('SELECT id, nom, matiere, creneaux FROM Colleurs')
    colleurs = cursor.fetchall()

    cursor.execute('SELECT id, nom, indisponibilites, noms_eleves FROM Trinomes')
    trinomes = cursor.fetchall()

    colleurs_dict = {colleur[0]: {'nom': colleur[1], 'matiere': colleur[2], 'creneaux': json.loads(colleur[3])} for colleur in colleurs}
    trinomes_dict = {trinome[0]: {'nom': trinome[1], 'indisponibilites': json.loads(trinome[2]), 'noms_eleves': trinome[3]} for trinome in trinomes}

    return colleurs_dict, trinomes_dict

def charger_donnees_semaine():
    with open("infosemaine.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        semaine = data['numero_semaine']
        cours_de_si = data['cours_de_si']
        cours_de_info = data['td_info']
        td_de_francais_en_cours = data['td_de_francais']
        semaine_paire = semaine % 2 == 0

    return semaine, cours_de_si, cours_de_info, td_de_francais_en_cours, semaine_paire

# Fonction pour vérifier la disponibilité d'un créneau pour un trinôme donné
def is_creneau_disponible(creneau, indisponibilites):
    for indisponibilite in indisponibilites:
        if (creneau['jour'] == indisponibilite['jour'] and
            creneau['heure_debut'] == indisponibilite['heure_debut'] and
            creneau['heure_fin'] == indisponibilite['heure_fin']):
            return False
    return True

# Fonction pour marquer un créneau comme indisponible pour un trinôme donné
def marquer_indisponible(trinome_id, creneau, trinomes_dict):
    trinomes_dict[trinome_id]['indisponibilites'].append({
        'jour': creneau['jour'],
        'heure_debut': creneau['heure_debut'],
        'heure_fin': creneau['heure_fin']
    })

# Fonction pour imprimer l'emploi du temps temporaire (pour debug)
def imprimer_edt_temporaire(emploi_du_temps):
    print("\nEmploi du temps temporaire:")
    for item in emploi_du_temps:
        print(f"Trinôme: {item['trinome']}, Colleur: {item['colleur']}")

# Fonction pour assigner les colles d'une matière spécifique
def assigner_colles(matiere, trinomes_disponibles, creneaux_colleurs, trinomes_dict):

    emploi_du_temps = []
    tous_assignes = True

    trinomes_tries = sorted(trinomes_disponibles, key=lambda t: len(trinomes_dict[t]['indisponibilites']), reverse=True)

    for trinome_id in trinomes_tries:

        trinome_data = trinomes_dict[trinome_id]
        trinome_nom = trinome_data['nom']
        trinome_indisponibilites = trinome_data['indisponibilites']
        
        candidats_colleurs = [
            colleur_id for colleur_id, colleur_data in creneaux_colleurs.items()
            if colleur_data['matiere'] == matiere and
            any(is_creneau_disponible(creneau, trinome_indisponibilites) for creneau in colleur_data['creneaux'])
        ]

        if not candidats_colleurs:
            tous_assignes = False
            continue
        
        assigne = False
        
        random.shuffle(candidats_colleurs)
        for colleur_id in candidats_colleurs:
            creneaux_disponibles = creneaux_colleurs[colleur_id]['creneaux']
            creneaux_correspondants = [creneau for creneau in creneaux_disponibles if is_creneau_disponible(creneau, trinome_indisponibilites)]
            
            if creneaux_correspondants:
                creneau = random.choice(creneaux_correspondants)
                emploi_du_temps.append({
                    'trinome': trinome_nom,
                    'colleur': creneaux_colleurs[colleur_id]['nom'],
                    'matiere': matiere,
                    'creneau': creneau
                })
                creneaux_colleurs[colleur_id]['creneaux'].remove(creneau)
                assigne = True
                
                # Rendre le trinome indisponible sur ce créneau
                marquer_indisponible(trinome_id, creneau, trinomes_dict)
                
                break
        
        if not assigne:
            print(f"Le trinôme {trinome_nom} n'a pas pu être assigné pour la matière {matiere}.")
            tous_assignes = False
            break
    
    return emploi_du_temps, tous_assignes

# Fonctions pour attribuer les TD de français de SI et d'info, si en cours
def attribuer_td_francais(td_de_francais_en_cours, semaine, trinomes_dict):
    if td_de_francais_en_cours:
        trinomes_list_id = list(trinomes_dict.keys())
        if semaine % 4 == 0:
            td_1er_creneau = trinomes_list_id[0:4]
            td_2e_creneau = trinomes_list_id[4:8]
        elif semaine % 4 == 1:
            td_1er_creneau = trinomes_list_id[8:12]
            td_2e_creneau = trinomes_list_id[12:]
        elif semaine % 4 == 2:
            td_1er_creneau = trinomes_list_id[4:8]
            td_2e_creneau = trinomes_list_id[0:4]
        elif semaine % 4 == 3:
            td_1er_creneau = trinomes_list_id[12:]
            td_2e_creneau = trinomes_list_id[9:12]

        for id_ in td_1er_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Mercredi", "heure_debut": "14:00", "heure_fin": "15:00"},
                {"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'Français', 'heure': 'Mercredi 14:00-16:00'})

        for id_ in td_2e_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Mercredi", "heure_debut": "16:00", "heure_fin": "17:00"},
                {"jour": "Mercredi", "heure_debut": "17:00", "heure_fin": "18:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'Français', 'heure': 'Mercredi 16:00-18:00'})

def attribuer_cours_si(cours_de_si, semaine, trinomes_dict):
    if cours_de_si:
        trinomes_list_id = list(trinomes_dict.keys())
        if semaine % 2 == 0:
            groupe_1er_creneau = trinomes_list_id[8:16]
            groupe_2e_creneau = trinomes_list_id[0:8]
        elif semaine % 2 == 1:
            groupe_1er_creneau = trinomes_list_id.copy()
            groupe_2e_creneau = []

        for id_ in groupe_1er_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Lundi", "heure_debut": "14:00", "heure_fin": "15:00"},
                {"jour": "Lundi", "heure_debut": "15:00", "heure_fin": "16:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'SI', 'heure': 'Lundi 14:00-16:00'})

        for id_ in groupe_2e_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Lundi", "heure_debut": "16:00", "heure_fin": "17:00"},
                {"jour": "Lundi", "heure_debut": "17:00", "heure_fin": "18:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'SI', 'heure': 'Lundi 16:00-18:00'})

def attribuer_cours_info(cours_de_info, semaine, trinomes_dict):
    if cours_de_info:
        trinomes_list_id = list(trinomes_dict.keys())
        if semaine % 2 == 0:
            groupe_1er_creneau = trinomes_list_id[0:6]
            groupe_2e_creneau = trinomes_list_id[12:16]
        elif semaine % 2 == 1:
            groupe_1er_creneau = []
            groupe_2e_creneau = trinomes_list_id[6:12]

        for id_ in groupe_1er_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Lundi", "heure_debut": "14:00", "heure_fin": "15:00"},
                {"jour": "Lundi", "heure_debut": "15:00", "heure_fin": "16:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'Info', 'heure': 'Lundi 14:00-16:00'})

        for id_ in groupe_2e_creneau:
            trinomes_dict[int(id_)]['indisponibilites'].extend([
                {"jour": "Lundi", "heure_debut": "16:00", "heure_fin": "17:00"},
                {"jour": "Lundi", "heure_debut": "17:00", "heure_fin": "18:00"}
            ])
            trinomes_dict[int(id_)].setdefault('cours', []).append({'matiere': 'Info', 'heure': 'Lundi 16:00-18:00'})

# Fonction principale pour générer les emplois du temps et générer le fichier HTML
def generer_edt_et_html(indisponibilites):

    colleurs_dict, trinomes_dict = charger_donnees()
    semaine, cours_de_si, cours_de_info, td_de_francais_en_cours, semaine_paire = charger_donnees_semaine()

    for id_ in indisponibilites:
        trinomes_dict[int(id_)]['indisponibilites'].extend(indisponibilites[id_])

    # Attribution des TD de français, SI, Info, si en cours
    attribuer_td_francais(td_de_francais_en_cours, semaine, trinomes_dict)
    attribuer_cours_si(cours_de_si, semaine, trinomes_dict)
    attribuer_cours_info(cours_de_info, semaine, trinomes_dict)

    # Attribution des colles par matière
    # On commence par attribuer toutes les colles de mathématiques
    emploi_du_temps_math, all_assigned_math = assigner_colles('Mathématiques', trinomes_dict.keys(), colleurs_dict, trinomes_dict)

    if not all_assigned_math:
        print("Échec lors de l'attribution des colles de Mathématiques.")
        return False

    print("Colles de Mathématiques attribuées avec succès.")

    # Attribution des colles de Physique ou Anglais selon la semaine
    matiere_groupe1 = 'Physique' if semaine_paire else 'Anglais'
    matiere_groupe2 = 'Anglais' if semaine_paire else 'Physique'

    trinomes_list = list(trinomes_dict.keys())
    half_size = len(trinomes_list) // 2
    groupe1 = trinomes_list[:half_size]
    groupe2 = trinomes_list[half_size:]

    emploi_du_temps_groupe1, all_assigned_groupe1 = assigner_colles(matiere_groupe1, groupe1, colleurs_dict, trinomes_dict)
    emploi_du_temps_groupe2, all_assigned_groupe2 = assigner_colles(matiere_groupe2, groupe2, colleurs_dict, trinomes_dict)

    iteration1, iteration2 = 0, 0

    # On attribue alors les colles de physique
    while not all_assigned_groupe1 and iteration1 < MAX_ITERATIONS:
        iteration1 += 1
        emploi_du_temps_groupe1, all_assigned_groupe1 = assigner_colles(matiere_groupe1, groupe1, colleurs_dict, trinomes_dict)

    print(f"Colles de {matiere_groupe1} attribuées avec succès.")

    # On attribue alors les colles d'anglais
    while not all_assigned_groupe2 and iteration2 < MAX_ITERATIONS:
        iteration2 += 1
        emploi_du_temps_groupe2, all_assigned_groupe2 = assigner_colles(matiere_groupe2, groupe2, colleurs_dict, trinomes_dict)

    print(f"Colles de {matiere_groupe2} attribuées avec succès.")

    # On verifie que tout le monde a bien eu ses colles
    tous_assignes = all_assigned_groupe1 and all_assigned_groupe2
    emploi_du_temps = emploi_du_temps_math + emploi_du_temps_groupe1 + emploi_du_temps_groupe2

    if tous_assignes:
        trinomes_groupes = {trinome['nom']: {'Mathematiques': [], 'Autre': [], 'Cours': trinome.get('cours', []), 'Eleves': " ".join(json.loads(trinome['noms_eleves']))} for trinome in trinomes_dict.values()}

        for colle in emploi_du_temps:
            matiere_key = 'Mathematiques' if colle['matiere'] == 'Mathématiques' else 'Autre'
            trinomes_groupes[colle['trinome']][matiere_key].append(colle)

        aujourdhui = datetime.today()
        prochain_lundi = aujourdhui + timedelta(days=-aujourdhui.weekday(), weeks=1)
        prochain_dimanche = prochain_lundi + timedelta(days=6)
        
        # Affiche la semaine prochaine
        lundi_str = prochain_lundi.strftime('%d/%m/%Y')
        dimanche_str = prochain_dimanche.strftime('%d/%m/%Y')

        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')

        html_output = template.render(trinomes_grouped=trinomes_groupes, semaine=f"Colloscope de la semaine du {lundi_str} au {dimanche_str}")

        with open('emploi_du_temps.html', 'w', encoding='utf-8') as f:
            f.write(html_output)

        print("Fichier HTML généré avec succès.")
        return True
    
    return False
