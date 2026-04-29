"""
Module Reservation.
C'est la classe centrale du projet. Elle lie un utilisateur a une salle sur creneau horaire.
La methode chevauche() est l'algorithme de detection de conflits : deux reservations se chavauchent si elles sont dans la meme salle, a la meme date, et que leurs horaires se superposent.
Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""

from datetime import datetime

class Reservation:
    """Represente une reservation de salle."""

    _compteur = 0

    def __init__(self, salle, utilisateur, date, heure_debut, heure_fin, motif =""):
        Reservation._compteur += 1
        self._id = Reservation._compteur
        self._salle = salle
        self._utilisateur = utilisateur
        self._date = date
        self._heure_debut = heure_debut
        self._heure_fin = heure_fin
        self._motif = motif
        self._statut = "confirmee"
        self._ressources = []
        self._cree_le = datetime.now().strftime("%d/%m/%Y %H:%M")

    @property
    def id(self):
        return self._id

    @property
    def salle(self):
        return self._salle

    @property
    def utilisateur(self):
        return self._utilisateur

    @property
    def date(self):
        return self._date

    @property
    def heure_debut(self):
        return self._heure_debut

    @property
    def heure_fin(self):
        return self._heure_fin

    @property
    def statut(self):
        return self._statut
    
    @property
    def motif(self):
        return self._motif

    @property
    def ressources(self):
        return self._ressources.copy()

    def ajouter_ressource(self, ressource):
        self._ressources.append(ressource)

    def annuler(self):
        """Annuler cette reservation."""
        self._statut = "annulee"
        for r in self._ressources:
            r.liberer()
    def _en_minutes(self, heure_str):
        """Convertit "hh:MM" en nombre de minutes depuis minuit."""
        h, m = heure_str.split(":")
        return int(h) * 60 + int(m)

    def get_debut_minutes(self):
        return self._en_minutes(self._heure_debut)

    def get_fin_minutes(self):
        return self._en_minutes(self._heure_fin)

    def chevauche(self, autre):
        """
        Verifie si cette reservation chevauche une autre.
        """
        # pas de conflit si l'une des salles est None
        if self._salle is None or autre.salle is None:
            return False
        # pas de conflit si salle differente
        if self._salle.id != autre.salle.id:
            return False
        # pas de conflit si date differente
        if self._date != autre.date:
            return False
        # pas de conflit si l'une est annulee
        if self._statut == "annulee" or autre.statut == "annulee":
            return False
        d1 = self.get_debut_minutes()
        f1 = self.get_fin_minutes()
        d2 = autre.get_debut_minutes()
        f2 = autre.get_fin_minutes()
        return d1 < f2 and d2 < f1

    def __str__(self):
        return (
            f"Reservation  : #{self._id}\n"
            f"Salle        : {self._salle.nom}\n"
            f"Date         : {self._date}\n"
            f"Creneau      : {self._heure_debut} - {self._heure_fin}\n"
            f"Utilisateur  : {self._utilisateur.nom}\n"
            f"Motif        : {self._motif}\n"
            f"Statut       : {self._statut}\n"
            f"Cree le      : {self._cree_le}"
        )

    def vers_dict(self):
        return {
            "id": self._id,
            "salle_id": self._salle.id,
            "utilisateur_id": self._utilisateur.id,
            "date": self._date,
            "heure_debut": self._heure_debut,
            "heure_fin": self._heure_fin,
            "motif": self._motif,
            "statut": self._statut,
            "cree_le": self._cree_le
        }