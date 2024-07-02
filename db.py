import sqlite3
import json

conn = sqlite3.connect('colloscope1.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Colleurs')
cursor.execute('DROP TABLE IF EXISTS Eleves')
cursor.execute('DROP TABLE IF EXISTS Trinomes')

# Création des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Colleurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    matiere TEXT NOT NULL,
    creneaux TEXT NOT NULL -- Stocke les créneaux sous forme de texte JSON
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Eleves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    indisponibilites TEXT NOT NULL -- Stocke les indisponibilités sous forme de texte JSON
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Trinomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    membres TEXT NOT NULL, -- Stocke les IDs des membres sous forme de texte JSON
    indisponibilites TEXT NOT NULL, -- Stocke les indisponibilités totales du trinôme sous forme de texte JSON
    noms_eleves TEXT NOT NULL -- Stocke les noms des élèves sous forme de texte JSON
)
''')



# Insertion des données exemples pour les colleurs
colleurs = [
    ('Colleur1', 'Mathématiques', json.dumps([
        {"jour": "Mercredi", "heure_debut": "16:00", "heure_fin": "17:00"},
        {"jour": "Mercredi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Colleur2', 'Mathématiques', json.dumps([
        {"jour": "Vendredi", "heure_debut": "08:00", "heure_fin": "09:00"},
        {"jour": "Vendredi", "heure_debut": "09:00", "heure_fin": "10:00"}
    ])),
    ('Colleur3', 'Mathématiques', json.dumps([
        {"jour": "Lundi", "heure_debut": "16:00", "heure_fin": "17:00"},
        {"jour": "Lundi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Colleur3', 'Mathématiques', json.dumps([
        {"jour": "Mercredi", "heure_debut": "14:00", "heure_fin": "15:00"},
        {"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}
    ])),
    ('Colleur4', 'Mathématiques', json.dumps([
        {"jour": "Mercredi", "heure_debut": "17:00", "heure_fin": "18:00"},
        {"jour": "Mercredi", "heure_debut": "18:00", "heure_fin": "19:00"}
    ])),
    ('Colleur5', 'Mathématiques', json.dumps([
        {"jour": "Jeudi", "heure_debut": "16:00", "heure_fin": "17:00"},
        {"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Colleur6', 'Mathématiques', json.dumps([
        {"jour": "Lundi", "heure_debut": "17:00", "heure_fin": "18:00"},
        {"jour": "Lundi", "heure_debut": "18:00", "heure_fin": "19:00"}
    ])),
    ('Colleur7', 'Mathématiques', json.dumps([
        {"jour": "Lundi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Colleur8', 'Mathématiques', json.dumps([
        {"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Colleur9', 'Mathématiques', json.dumps([
        {"jour": "Mardi", "heure_debut": "18:00", "heure_fin": "19:00"}
    ])),
    ('Colleur10', 'Mathématiques', json.dumps([
        {"jour": "Jeudi", "heure_debut": "16:00", "heure_fin": "17:00"}
    ])),
        ('Colleur11', 'Anglais', json.dumps([{"jour": "Jeudi", "heure_debut": "16:00", "heure_fin": "17:00"}, {"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}, {"jour": "Jeudi", "heure_debut": "18:00", "heure_fin": "19:00"}])),
    ('Colleur12', 'Anglais', json.dumps([{"jour": "Jeudi", "heure_debut": "16:00", "heure_fin": "17:00"}, {"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}])),
    ('Colleur13', 'Anglais', json.dumps([{"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}])),
    ('Colleur14', 'Anglais', json.dumps([{"jour": "Mercredi", "heure_debut": "14:00", "heure_fin": "15:00"}, {"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}])),


    ('Colleur15', 'Physique', json.dumps([{"jour": "Mercredi", "heure_debut": "09:00", "heure_fin": "10:00"}, {"jour": "Mercredi", "heure_debut": "14:00", "heure_fin": "15:00"}, {"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}])),
    ('Colleur16', 'Physique', json.dumps([{"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}, {"jour": "Mercredi", "heure_debut": "16:00", "heure_fin": "17:00"}])),
    ('Colleur17', 'Physique', json.dumps([{"jour": "Lundi", "heure_debut": "18:00", "heure_fin": "19:00"}])),
    ('Colleur18', 'Physique', json.dumps([{"jour": "Lundi", "heure_debut": "18:00", "heure_fin": "19:00"}])),
    ('Colleur19', 'Physique', json.dumps([{"jour": "Vendredi", "heure_debut": "10:00", "heure_fin": "11:00"}])),

]

eleves = [
    ('Eleve1', json.dumps([])),
    ('Eleve2', json.dumps([
        {"jour": "Lundi", "heure_debut": "16:00", "heure_fin": "17:00"}
    ])),
    ('Eleve3', json.dumps([
        {"jour": "Mercredi", "heure_debut": "14:00", "heure_fin": "15:00"},
        {"jour": "Mercredi", "heure_debut": "15:00", "heure_fin": "16:00"}
    ])),
    ('Eleve4', json.dumps([
        {"jour": "Jeudi", "heure_debut": "16:00", "heure_fin": "17:00"},
        {"jour": "Jeudi", "heure_debut": "17:00", "heure_fin": "18:00"}
    ])),
    ('Eleve5', json.dumps([])),
    ('Eleve6', json.dumps([])),
    ('Eleve7', json.dumps([])),
    ('Eleve8', json.dumps([])),
    ('Eleve9', json.dumps([])),
    ('Eleve10', json.dumps([])),
    ('Eleve11', json.dumps([])),
    ('Eleve12', json.dumps([])),
    ('Eleve13', json.dumps([])),
    ('Eleve14', json.dumps([])),
    ('Eleve15', json.dumps([])),
    ('Eleve16', json.dumps([])),
    ('Eleve17', json.dumps([])),
    ('Eleve18', json.dumps([])),
    ('Eleve19', json.dumps([])),
    ('Eleve20', json.dumps([])),
    ('Eleve21', json.dumps([])),
    ('Eleve22', json.dumps([])),
    ('Eleve23', json.dumps([])),
    ('Eleve24', json.dumps([])),
    ('Eleve25', json.dumps([])),
    ('Eleve26', json.dumps([])),
    ('Eleve27', json.dumps([])),
    ('Eleve28', json.dumps([])),
    ('Eleve29', json.dumps([])),
    ('Eleve30', json.dumps([])),
    ('Eleve31', json.dumps([])),
    ('Eleve32', json.dumps([])),
    ('Eleve33', json.dumps([])),
    ('Eleve34', json.dumps([])),
    ('Eleve35', json.dumps([])),
    ('Eleve36', json.dumps([])),
    ('Eleve37', json.dumps([])),
    ('Eleve38', json.dumps([])),
    ('Eleve39', json.dumps([])),
    ('Eleve40', json.dumps([])),
    ('Eleve41', json.dumps([])),
    ('Eleve42', json.dumps([])),
    ('Eleve43', json.dumps([])),
    ('Eleve44', json.dumps([])),
    ('Eleve45', json.dumps([])),
    ('Eleve46', json.dumps([])),
    ('Eleve47', json.dumps([])),
    ('Eleve48', json.dumps([])),
]

def calculate_total_unavailabilities(eleve_ids):
    total_unavailabilities = []
    for eleve_id in eleve_ids:
        cursor.execute('SELECT indisponibilites FROM Eleves WHERE id = ?', (eleve_id,))
        indisponibilites_json = cursor.fetchone()[0]
        indisponibilites = json.loads(indisponibilites_json)
        total_unavailabilities.extend(indisponibilites)
    return json.dumps(total_unavailabilities)

trinomes = [
    ('Trinome1', [1, 2, 3]),
    ('Trinome2', [4, 5, 6]),
    ('Trinome3', [7, 8, 9]),
    ('Trinome4', [10, 11, 12]),
    ('Trinome5', [13, 14, 15]),
    ('Trinome6', [16, 17, 18]),
    ('Trinome7', [19, 20, 21]),
    ('Trinome8', [22, 23, 24]),
    ('Trinome9', [25, 26, 27]),
    ('Trinome10', [28, 29, 30]),
    ('Trinome11', [31, 32, 33]),
    ('Trinome12', [34, 35, 36]),
    ('Trinome13', [37, 38, 39]),
    ('Trinome14', [40, 41, 42]),
    ('Trinome15', [43, 44, 45]),
    ('Trinome16', [46, 47, 48]),
]

def get_eleve_names(eleve_ids):
    names = []
    for eleve_id in eleve_ids:
        cursor.execute('SELECT nom FROM Eleves WHERE id = ?', (eleve_id,))
        name = cursor.fetchone()[0]
        names.append(name)
    return json.dumps(names)


for colleur in colleurs:
    cursor.execute('INSERT INTO Colleurs (nom, matiere, creneaux) VALUES (?, ?, ?)', colleur)

for eleve in eleves:
    cursor.execute('INSERT INTO Eleves (nom, indisponibilites) VALUES (?, ?)', eleve)

for trinome in trinomes:
    eleve_ids = trinome[1]
    total_unavailabilities = calculate_total_unavailabilities(eleve_ids)
    noms_eleves = get_eleve_names(eleve_ids)
    cursor.execute('INSERT INTO Trinomes (nom, membres, indisponibilites, noms_eleves) VALUES (?, ?, ?, ?)', (trinome[0], json.dumps(eleve_ids), total_unavailabilities, noms_eleves))


conn.commit()
conn.close()

def afficher_eleves():
    conn = sqlite3.connect('colloscope1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom, noms_eleves FROM Trinomes')
    groupes = cursor.fetchall()
    for groupe in groupes:
        noms_eleves = json.loads(groupe[2])
        noms_eleves_str = ", ".join(noms_eleves)
        print(f"{groupe[1]} : ID : {groupe[0]} - {noms_eleves_str}")
    conn.close()

