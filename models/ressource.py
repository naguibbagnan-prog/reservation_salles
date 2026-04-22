"""
Module Ressource - equipements des salles .
Gere les ressources comme les projecteurs, micros, etc.
Une ressource a une quantite totale et une quantite disponible.
Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""

class Ressource:
    """Represente un equipement reservable."""

    TYPES_POSSIBLES = [
        "projecteur", "micro", "camera", "tableau_interactif", "systeme_son"
    ]
    _compteur = 0

    def __init__(self, nom, type_res, quantite=1):
        if type_res not in self.TYPES_POSSIBLES:
            raise ValueError(f"Type inconnu : {type_res}")
        Ressource._compteur += 1
        self._id = Ressource._compteur
        self._nom = nom
        self._type = type_res
        self._quantite = quantite
        self._dispo = quantite

    @property
    def id(self):
        return self._id
    
    @property
    def nom(self):
        return self._nom

    @property
    def type_ressource(self):
        return self._type

    @property
    def quantite(self):
        return self._quantite

    @property
    def disponible(self):
        return self._dispo

    def reserver(self, nb=1):
        """Reserve une quantite. Retourne True si possible."""
        if nb<= self._dispo:
            self._dispo -=nb
            return True
        return False

    def liberer(self, nb=1):
        """Libere ne quantite."""
        self._dispo = min(self._dispo + nb, self._quantite)

    def __str__(self):
        return(
            f"Ressource   : {self._nom}\n"
            f"Type        : {self._type}\n"
            f"Disponible  : {self._dispo}/{self._quantite}"
        )

    def vers_dict(self):
        return {
            "id": self._id,
            "nom": self._nom,
            "type": self._type,
            "quantite": self._quantite,
            "disponible": self._dispo
        }