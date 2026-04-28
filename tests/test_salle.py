"""
Tests pour le module Salle.
Lancer avec : pytest tests/test_salle.py -v

Auteurs : ACODODJA Mélaine, BAGNAN Abdel-Naguib
"""

import pytest
from models.salle import Salle, SalleCours, SalleTP, Amphitheatre


class TestSalle:
    """Tests de base pour la classe Salle."""

    def setup_method(self):
        """Reinitialise le compteur avant chaque test."""
        Salle._compteur = 0
        self.salle = Salle("A101", 30, ["projecteur", "tableau"])

    def test_creation(self):
        assert self.salle.nom == "A101"
        assert self.salle.capacite == 30
        assert "projecteur" in self.salle.equipements

    def test_id_incremente(self):
        salle2 = Salle("B202", 40)
        assert salle2.id == self.salle.id + 1

    def test_modifier_nom(self):
        self.salle.nom = "C303"
        assert self.salle.nom == "C303"

    def test_nom_vide_erreur(self):
        with pytest.raises(ValueError):
            self.salle.nom = ""

    def test_capcite_negative_erreur(self):
        with pytest.raises(ValueError):
            self.salle.capacite = -5

    def test_ajout_equipement(self):
        self.salle.ajouter_equipement("micro")
        assert "micro" in self.salle.equipements

    def test_pas_de_doublon_equipement(self):
        self.salle.ajouter_equipement("projecteur")
        # projesteur etait deja la, il ne doit pas etre en double
        nb = self.salle.equipements.count("projecteur")
        assert nb == 1

    def test_retrait_equipement(self):
        self.salle.retirer_equipement("projecteur")
        assert "projecteur" not in self.salle.equipements

    def test_disponibilite(self):
        self.salle.changer_disponibilite(False)
        assert self.salle.est_disponible == False

    def test_vers_dict(self):
        d = self.salle.vers_dict()
        assert d["nom"] == "A101"
        assert d["capacite"] == 30

    def test_affichage(self):
        texte = str(self.salle)
        assert "A101" in texte

class TestHeritage:
    """Tests pour verifier que l'heritage fonctionne."""

    def setup_method(self):
        Salle._compteur = 0

    def test_salle_cours_est_une_salle(self):
        sc = SalleCours("D101", 25, type_tableau="interactif")
        assert isinstance(sc, Salle)
        assert sc.type_tableau == "interactif"

    def test_salle_tp(self):
        stp = SalleTP("E201", 20, nb_postes=18)
        assert isinstance(stp, Salle)
        assert stp.nb_postes == 18

    def test_amphitheatre(self):
        amphi = Amphitheatre("F001", 300, micro=True)
        assert isinstance(amphi, Salle)
        assert amphi.a_micro == True
        assert amphi.capacite == 300
