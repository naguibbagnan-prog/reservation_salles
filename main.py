"""
Systeme de Reservation de Salles
Universite de Parakou - Projet 7
Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
Encadre par : Dr MOUSSE Mikael
"""

def afficher_menu():
    """Affiche le menu principal."""
    print("\n--- MENU PRINCIPAL ---")
    print("1. Gerer les salles")
    print("2. Gerer les reservations")
    print("3. Voir le planning")
    print("4. Quitter")

def menu_salles():
    """Sous-menu pour la gestion des salles."""
    print("\n--- Gestion des Salles ---")
    print("a. Ajouter une salle")
    print("b. Lister les salles")
    print("c. Retour")
    choix = input("Votre choix : ").strip().lower()
    if choix == "a":
        nom = input("Nom de la salle : ")
        capacite = input("Capacite : ")
        print(f"Salle {nom} ({capacite} places) enregistree.")
    elif choix == "b":
        salles_exemple = [
            {"nom": "A101", "capacite": 30, "equipements": ["projecteur", "tableau"]},
            {"nom": "B202", "capacite": 40, "equipements": ["micro", "tableau"]},
        ]
        for s in salles_exemple:
            equip = ", ".join(s["equipements"])
            print(f"  - {s['nom']} | {s['capacite']} places | {equip}")

def menu_reservations():
    """Sous-menu pour les reservations."""
    print("\n--- Gestion des Reservations ---")
    print("a. Nouvelle reservation")
    print("b. Annuler une reservation")
    print("c. Retour")
    choix = input("Votre choix : ").strip().lower()
    if choix == "a":
        salle = input("Nom de la salle : ")
        date = input("Date (JJ/MM/AAAA) : ")
        debut = input("Heure de debut (HH:MM) : ")
        fin = input("Heure de fin (HH:MM) : ")
        creneau = (debut, fin)
        print(f"Reservation : {salle} le {date}, creneau {creneau[0]} - {creneau[1]}")

def main():
    """Fonction principale."""
    print("=" * 50)
    print("  Systeme de Reservation de Salles")
    print("  Universite de Parakou")
    print("  ACODODJA Melaine & BAGNAN Abdel-Naguib")
    print("=" * 50)
    while True:
        afficher_menu()
        choix = input("\nVotre choix (1-4) : ").strip()
        if choix == "1":
            menu_salles()
        elif choix == "2":
            menu_reservations()
        elif choix == "3":
            print("\n[Planning - sera implemente au Bloc 4]")
        elif choix == "4":
            print("\nAu revoir !")
            break
        else:
            print("Choix invalide, reessayez.")

if __name__ == "__main__":
    main()