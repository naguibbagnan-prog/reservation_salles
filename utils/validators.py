"""
Fonctions de validation pour le systeme de reservation.
On utilise ici les types de donnees complexes :
- tuples pour les constantes (jours valides)
- dictionnaires pour les plages horaires
- listes pour les capacites et equipements
Ref : Cahier des charges, section 3.4
"""
from datetime import datetime

# --- Constantes ---
# tuple : les jours ou on peut reserver (pas le dimanche)
JOURS_VALIDES = (
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"
)

# dictionnaire : horaires autorises selon le type de salle
HORAIRES_AUTORISES = {
    "cours": {"debut": "07:00", "fin": "19:00"},
    "tp": {"debut": "07:00", "fin": "19:00"},
    "amphi": {"debut": "06:00", "fin": "20:00"},
}

# liste : equipements disponibles a l'universite
EQUIPEMENTS_DISPONIBLES = [
    "projecteur", "tableau", "micro",
    "tables et bancs", "ordinateurs"
]

# --- Fonctions de validation ---
def valider_nom_salle(nom):
    """
    Verifie que le nom est correct (au moins 2 caracteres).
    Retourne True ou False.
    """
    if not nom or len(nom.strip()) < 2:
        return False
    return True

def valider_creneau(heure_debut, heure_fin):
    """
    Verifie qu'un creneau horaire est valide.
    Retourne un tuple (ok, message).
    """
    try:
        debut = datetime.strptime(heure_debut, "%H:%M")
        fin = datetime.strptime(heure_fin, "%H:%M")
    except ValueError:
        return (False, "Format invalide, utilisez HH:MM")
    if debut >= fin:
        return (False, "Le debut doit etre avant la fin")
    # verifier que ca dure au moins 30 min
    diff = (fin - debut).seconds // 60
    if diff < 30:
        return (False, "Le creneau doit durer au moins 30 minutes")
    return (True, "OK")

def valider_date(date_str):
    """
    Verifie le format de la date et qu'elle n'est pas passee.
    Retourne un tuple (ok, resultat).
    """
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return (False, "Format invalide, utilisez JJ/MM/AAAA")
    if date_obj.date() < datetime.now().date():
        return (False, "La date est deja passee")
    # pas de reservation le dimanche
    if date_obj.weekday() == 6:
        return (False, "Pas de reservation le dimanche")
    return (True, date_obj)

def valider_email(email):
    """Verification basique d'un email."""
    return "@" in email and "." in email

def formater_creneau(debut, fin):
    """Met en forme un creneau pour l'affichage."""
    return f"{debut} - {fin}"