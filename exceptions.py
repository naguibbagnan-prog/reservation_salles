"""
Exceptions personnalisees pour le systeme de reservation.
Sera complete au Bloc 5.
"""


"""
Exceptions personnalisees pour le systeme de reservation.

On cree des classes d'erreurs specifiques pour pouvoir les attraper precisement avec try/except.

Auteurs: ACODODJA Melaine, BAGNAN Abdel-Naguib
"""


class ReservationError(Exception):
    """Erreur de base pour tout le systeme"""
    pass

class ConflitHoraireError(ReservationError):
    """Quand deux reservations se chevauchent."""

    def __init___(self, resa_existante, nouvelle_resa):
        self.existante = resa_existante
        self.nouvelle = nouvelle_resa
        message = (
            f"Conflit : {resa_existante.salle.nom} est deja reserve "
            f"le {resa_existante.date} de {resa_existante.heure_debut} "
            f"a {resa_existante.heure_fin}"
        )
        super().__init__(message)


class SalleIntrouvableError(ReservationError):
    """Quand on cherche une salle qui n'existe pas.""" 

    def __init__(self, salle_id):
        super().__init__(f"Aucune salle avec l'id {salle_id}")


class CreneauInvalideError(ReservationError):
    """Quand le creneau horaire n'est pas correct."""

    def __init__(self, msg="Creneau invalide"):
        super().__init__(msg)


class CapaciteDepasseeError(ReservationError):
    """Quand on depasse la capacite d'une salle."""

    def __init__(self, nom_salle, capacite):
        super().__init__(
            f"La salle {nom_salle} ne peut accueillir que {capacite} personnes"
        )


class RessourceIndisponibleError(ReservationError):
    """Quand un equipement n'est plus disponible."""

    def __init__(self, nom_ressource):
        super().__init__(f"'{nom_ressource}' n'est pas disponible")

