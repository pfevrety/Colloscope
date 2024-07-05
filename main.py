import json

from colles import generer_edt_et_html
from db import afficher_eleves

MAX_INTERATIONS = 1000

def saisie_indisponibilites():
    jours_valides = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    indisponibilites = []
    
    while True:
        id_eleve = input("Quel est l'id du groupe de colle ('list_id' pour afficher tous les id)> ")
        if id_eleve == 'list_id':
            afficher_eleves()
            continue
        
        while True:
            jour = input("Quel jour l'élève est indisponible (Ex: 'Lundi' ) > ")
            if jour in jours_valides:
                break
            else:
                print("Vous devez entrer un jour dans cette liste :")
                print(jours_valides)
        
        while True:
            heure_debut_str = input("Heure de début de l'indisponibilité (ex: 08:00) > ")
            if len(heure_debut_str) == 5 and heure_debut_str[2] == ':' and heure_debut_str[:2].isdigit() and heure_debut_str[3:].isdigit():
                heure_debut = heure_debut_str
                break
            else:
                print("Vous devez entrer une heure au format HH:MM.")
        
        while True:
            heure_fin_str = input("Heure de fin de l'indisponibilité (ex: 17:00) > ")
            if len(heure_fin_str) == 5 and heure_fin_str[2] == ':' and heure_fin_str[:2].isdigit() and heure_fin_str[3:].isdigit():
                heure_fin = heure_fin_str
                break
            else:
                print("Vous devez entrer une heure au format HH:MM.")
        
        # Ajout des créneaux d'indisponibilité pour chaque heure
        heures_debut = int(heure_debut.split(':')[0])
        heures_fin = int(heure_fin.split(':')[0])
        
        for h in range(heures_debut, heures_fin):
            heure_debut_creneau = f"{h:02}:00"
            
            indisponibilite = {
                "jour": jour,
                "heure_debut": heure_debut_creneau,
            }
            
            indisponibilites.append(indisponibilite)

        return id_eleve, indisponibilites

if __name__ == "__main__":
    nouvelles_indisponiblites = True
    indisponibilites = {}
    
    while nouvelles_indisponiblites:
        x = input("Des élèves ont-ils des indisponibilités cette semaine (y/n)> ")
        if x == "y":
            id_, indisponibilite = saisie_indisponibilites()
            if id_ in indisponibilite:
                indisponibilites[id_] + indisponibilite
            else:
                indisponibilites[id_] = indisponibilite
        elif x == "n":
            nouvelles_indisponiblites = False
        
    print("Génération du colloscope pour la semaine.")
    generation_reussie = False
    iteration = 0
    max_iterations = 100

    while not generation_reussie and iteration < MAX_INTERATIONS:
        print("-"*40)
        generation_reussie = generer_edt_et_html(indisponibilites)
        iteration += 1
    if not generation_reussie:
        print("Il y a eu un problème. La semaine est surement incasable.")
    else:
        print("-"*40)
        print(f"Colloscope généré avec succès après {iteration} itérations principales. Lien du Colloscope : ./emploi_du_temps.html")

        change_date = input("Voulez vous incrémenter la semaine ? (y/n) ") == "y"
        if change_date:
            with open('infosemaine.json', 'r+') as f:
                data = json.load(f)
                data['numero_semaine'] = data['numero_semaine'] + 1
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                