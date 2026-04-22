"""
Module Salle - gestion des salles de l'universite.
On utilise l'heritage pour differencier les types de salles.
Chaque salle a un compteur automatique pour l'ID.
Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""


class Salle:
    """
    Classe de base pour une salle.
    Les attributs sont prives (encapsulation) et on y accede
    avec des proprietes (@property).
    """

    _compteur = 0

    def __init__(self, nom, capacite, equipements=None):
        Salle._compteur += 1
        self._id = Salle._compteur
        self._nom = nom
        self._capacite = capacite
        self._equipements = equipements if equipements else []
        self._disponible = True

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nouveau_nom):
        if not nouveau_nom or len(nouveau_nom) < 2:
            raise ValueError("Le nom doit faire au moins 2 caracteres")
        self._nom = nouveau_nom

    @property
    def capacite(self):
        return self._capacite

    @capacite.setter
    def capacite(self, valeur):
        if valeur <= 0:
            raise ValueError("La capacite doit etre positive")
        self._capacite = valeur

    @property
    def equipements(self):
        return self._equipements.copy()

    @property
    def est_disponible(self):
        return self._disponible

    def ajouter_equipement(self, equip):
        """Ajoute un equipement s'il n'existe pas deja."""
        if equip not in self._equipements:
            self._equipements.append(equip)

    def retirer_equipement(self, equip):
        """Retire un equipement de la salle."""
        if equip in self._equipements:
            self._equipements.remove(equip)

    def changer_disponibilite(self, dispo):
        self._disponible = dispo

    def __str__(self):
        equip = ", ".join(self._equipements) if self._equipements else "aucun"
        statut = "disponible" if self._disponible else "indisponible"
        return (
            f"Salle      : {self._nom}\n"
            f"Capacite   : {self._capacite} places\n"
            f"Equipements: {equip}\n"
            f"Statut     : {statut}"
        )

    def __repr__(self):
        return f"Salle('{self._nom}', {self._capacite})"

    def vers_dict(self):
        """Convertit en dictionnaire pour la sauvegarde."""
        return {
            "id": self._id,
            "nom": self._nom,
            "capacite": self._capacite,
            "equipements": self._equipements,
            "disponible": self._disponible,
            "type": self.__class__.__name__
        }


class SalleCours(Salle):
    """Salle de cours classique."""

    def __init__(self, nom, capacite, equipements=None, type_tableau="blanc"):
        super().__init__(nom, capacite, equipements)
        self._type_tableau = type_tableau

    @property
    def type_tableau(self):
        return self._type_tableau

    def __str__(self):
        return f"[Cours]\n{super().__str__()}\nTableau    : {self._type_tableau}"


class SalleTP(Salle):
    """Salle de travaux pratiques avec ordinateurs."""

    def __init__(self, nom, capacite, equipements=None, nb_postes=0):
        super().__init__(nom, capacite, equipements)
        self._nb_postes = nb_postes

    @property
    def nb_postes(self):
        return self._nb_postes

    def __str__(self):
        return f"[TP]\n{super().__str__()}\nPostes     : {self._nb_postes}"


class Amphitheatre(Salle):
    """Amphitheatre de grande capacite."""

    def __init__(self, nom, capacite, equipements=None, micro=True):
        super().__init__(nom, capacite, equipements)
        self._micro = micro

    @property
    def a_micro(self):
        return self._micro

    def __str__(self):
        mic = "oui" if self._micro else "non"
        return f"[Amphi]\n{super().__str__()}\nMicro      : {mic}"