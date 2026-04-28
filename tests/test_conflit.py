"""
Tests pour le service de reservation et la detection de conflits.
Lancer avec : pytest tests/test_conflit.py -v

Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""

import pytest
from models.salle import Salle
from models.utilisateur import Utilisateur
from models.reservation import Reservation
from services.reservation_service import ReservationService


class TestReservationService:
    """Tests du service de reservation."""

    def setup_method(self):
        Salle._compteur = 0
        Utilisateur._compteur = 0
        Reservation._compteur = 0

        self.service = ReservationService()
        self.salle = Salle("A101", 30)
        self.user = Utilisateur(
            "ACODODJA Melaine", "acododja@univ-parakou.bj"
        )

        self.service.ajouter_salle(self.salle)
        self.service.ajouter_utilisateur(self.user)

        # ajouter 2 reservations sans conflit
        self.service.creer_reservation(
            self.salle, self.user, "25/04/2026", "08:00", "10:00", "Cours matin"
        )
        self.service.creer_reservation(
            self.salle, self.user, "25/04/2026", "14:00", "16:00", "TD apres-midi"
        )

    def test_reservation_sans_conflit(self):
        """Creer une reservation qui ne chevauche rien."""
        ok, resultat = self.service.creer_reservation(
            self.salle, self.user, "25/04/2026", "10:00", "12:00"
        )
        assert ok == True
        assert resultat.heure_debut == "10:00"

    def test_reservation_avec_conflit(self):
        """Essayer de reserver un creneau deja pris."""
        ok, msg = self.service.creer_reservation(
            self.salle, self.user, "25/04/2026", "09:00", "11:00"
        )
        assert ok == False
        assert "Conflit" in msg

    def test_annulation(self):
        """Annuler une reservation."""
        resas = self.service.lister_reservations()
        resa_id = resas[0].id
        resultat = self.service.annuler_reservation(resa_id)
        assert resultat == True

    def test_creneaux_libres(self):
        """Verifier les creneaux disponibles."""
        creneaux = self.service.trouver_creneaux_libres(
            self.salle, "25/04/2026", 60
        )
        assert len(creneaux) > 0
        # entre les deux reservations il y a 10h-14h de libre
        assert ("10:00", "14:00") in creneaux

    def test_rapport(self):
        """Verifier le rapport de conflits."""
        rapport = self.service.rapport_conflits()
        assert rapport["total"] == 2
        assert rapport["nb_conflits"] == 0

    def test_lister_par_salle(self):
        """Filtrer les reservations par salle."""
        resas = self.service.lister_reservations(salle_id=self.salle.id)
        assert len(resas) == 2

    def test_lister_par_date(self):
        """Filtrer les reservations par date."""
        resas = self.service.lister_reservations(date="25/04/2026")
        assert len(resas) == 2

        resas2 = self.service.lister_reservations(date="30/04/2026")
        assert len(resas2) == 0