"""
Tests pour le module Reservation.
La partie critique : verifier que la detection de conflits marche.

Lancer avec : pytest tests/test_reservation.py -v

Auteurs : ACODODJA Mélaine, BAGNAN Abdel-Naguib
"""

import pytest 
from models.salle import Salle
from models.utilisateur import Utilisateur
from models.reservation import Reservation


class TestReservation:
    """Tests de creation et manipulation de reservations."""

    def setup_method(self):
        Salle._compteur = 0
        Utilisateur._compteur = 0
        Reservation._compteur = 0

        self.salle = Salle("A101", 30)
        self.user = Utilisateur(
            "BAGNAN Abdel-Naguib", "bagnan@univ-parakou.bj"
        )
        self.resa = Reservation(
            self.salle, self.user,
            "25/04/2026", "10:00", "12:00", "Cours Python"
        )

    def test_creation(self):
        assert self.resa.salle.nom == "A101"
        assert self.resa.utilisateur.nom == "BAGNAN Abdel-Naguib"
        assert self.resa.date == "25/04/2026"
        assert self.resa.heure_debut == "10:00"
        assert self.resa.heure_fin == "12:00"
        assert self.resa.statut == "confirmee"

    def test_annulation(self):
        self.resa.annuler()
        assert self.resa.statut == "annulee"

    def test_conversion_minutes(self):
        assert self.resa.get_debut_minutes() == 600 # 10 * 60
        assert self.resa.get_fin_minutes() == 720   # 12 * 60

    def test_vers_dict(self):
        d = self.resa.vers_dict()
        assert d["date"] == "25/04/2026"
        assert d["statut"] == "confirmee"


class TestChevauchement:
    """
    Tests de la detection de chevauchements.
    On teste tous les cas possibles.
    """ 

    def setup_method(self):
        Salle._compteur = 0
        Utilisateur._compteur = 0
        Reservation._compteur = 0

        self.salle = Salle("A101", 30)
        self.salle2 = Salle("B202", 40)
        self.user = Utilisateur(
            "ACODODJA Mélaine", "acododja@univ-parakou.bj"
        )
        # reservation de reference : 10h-12h le 25/04
        self.ref = Reservation(
            self.salle, self.user, "25/04/2026", "10:00", "12:00"
        )
        
    def test_meme_creneau(self):
        """Meme heure exacte = conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "10:00", "12:00")
        assert self.ref.chevauche(r2) == True
 
    def test_chevauchement_debut(self):
        """Commence avant, finit pendant = conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "09:00", "11:00")
        assert self.ref.chevauche(r2) == True
 
    def test_chevauchement_fin(self):
        """Commence pendant, finit apres = conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "11:00", "13:00")
        assert self.ref.chevauche(r2) == True
        
    def test_chevauchement_englobant(self):
        """Un creneau qui englobe l'autre = conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "08:00", "14:00")
        assert self.ref.chevauche(r2) == True
 
    def test_juste_avant_pas_conflit(self):
        """Finit exactement quand l'autre commence = pas de conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "08:00", "10:00")
        assert self.ref.chevauche(r2) == False
 
    def test_juste_apres_pas_conflit(self):
        """Commence exactement quand l'autre finit = pas de conflit."""
        r2 = Reservation(self.salle, self.user, "25/04/2026", "12:00", "14:00")
        assert self.ref.chevauche(r2) == False
 
    def test_salle_differente_pas_conflit(self):
        """Meme heure mais salle differente = pas de conflit."""
        r2 = Reservation(self.salle2, self.user, "25/04/2026", "10:00", "12:00")
        assert self.ref.chevauche(r2) == False
 
    def test_date_differente_pas_conflit(self):
        """Meme salle meme heure mais jour different = pas de conflit."""
        r2 = Reservation(self.salle, self.user, "26/04/2026", "10:00", "12:00")
        assert self.ref.chevauche(r2) == False
 
    def test_annulee_pas_conflit(self):
        """Si une reservation est annulee, pas de conflit."""
        self.ref.annuler()
        r2 = Reservation(self.salle, self.user, "25/04/2026", "10:00", "12:00")
        assert self.ref.chevauche(r2) == False
    