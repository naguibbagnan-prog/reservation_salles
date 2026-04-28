"""
Sercice de gestion des reservations.

Ce module coordonne toutes les operations :
- ajouter/supprimer des salles et utilisateurs
- creer/annuler des reservations
- verifier les conflits avant de confirmer
- trouver les creneaux libres

Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""

from models.reservation import Reservation

class ReservationService:
    """Service central du systeme de reservation."""

    def __init__(self):
        self._salles = []
        self._utilisateurs = []
        self._reservations = []
        self._ressources = []

    # --- Salles ---

    def ajouter_salle(self, salle):
        self._salles.append(salle)

    def supprimer_salle(self, salle_id):
        for i, s in enumerate(self._salles):
            if s.id == salle_id:
                self._salles.pop(i)
                return True
            return False

    def trouver_salle(self, salle_id):
        for s in self._salles:
            if s.id == salle_id:
                return s
            return None

    def lister_salles(self):
        return self._salles.copy()

    # --- Utilisateurs ---
    
    def ajouter_utilisateur(self, user):
        self._utilisateurs.append(user)

    def trouver_utilisateur(self, user_id):
        for u in self._utilisateurs:
            if u.id == user_id:
                return u
        return None

    def lister_utilisateurs(self):
        return self._utilisateurs.copy()

    # --- Ressources ---

    def ajouter_ressource(self, res):
        self._ressources.append(res)

    def lister_ressources(self):
        return self._ressources.copy()

    # ---Reservations ---
    def creer_reservation(self, salle, utilisateur, date, heure_debut, heure_fin, motif=""):
        """
        Cree une reservation apres verification des conflits.
        Retourne (True, reservation) ou (False, message d'erreur).
        """
        nouvelle = Reservation(
            salle, utilisateur, date, heure_debut, heure_fin, motif
        )
        
        # verifier s'il y a des conflits
        conflits = self._detecter_conflits(nouvelle)

        if conflits:
            details = "\n".join([f"  - {c}" for c in conflits])
            msg = f"Conflit avec {len(conflits)} reservation(s) :\n{details}"
            return (False, msg)

        self._reservations.append(nouvelle)
        return (True, nouvelle)

    def annuler_reservation(self, resa_id):
        for r in self._reservations:
            if r.id == resa_id:
                r.annuler()
                return True
        return False

    def lister_reservations(self, salle_id=None, date=None):
        """Liste les reservations avec les filtres optionnels."""
        resultats = self._reservations.copy()

        if salle_id is not None:
            resultats = [r for r in resultats if r.salle.id == salle_id]
        if date is not None:
            resultats = [r for r in resultats if r.date == date]

        return resultats

    # --- Detection de conflits ---

    def _detecter_conflits(self, nouvelle_resa):
        """Retourne la liste des reservations en conflit. """
        conflits = []
        for resa in self._reservations:
            if resa.id == nouvelle_resa.id:
                continue
            if nouvelle_resa.chevauche(resa):
                conflits.append(resa)
        return conflits

    def trouver_creneaux_libres(self, salle, date, duree_min=60):
        """
        Cherche les creneaux disponibles pour une salle a une date.
        Retourne une liste de tuples (debut, fin).
        """
        # recuperer les reservations du jour pour cette salle
        resas_jour = [
            r for r in self._reservations
            if r.salle.id == salle.id
            and r.date == date
            and r.statut != "annulee"
        ]
        resas_jour.sort(key=lambda r: r.get_debut_minutes())

        creneaux = []
        debut_journee = 7 * 60    # 07h00
        fin_journee = 19 * 60    # 19h00
        position = debut_journee

        for resa in resas_jour:
            debut_resa = resa.get_debut_minutes()
            if debut_resa - position >= duree_min:
                h1 = f"{position // 60:02d}:{position % 60:02d}"
                h2 = f"{debut_resa // 60:02d}:{debut_resa % 60:02d}"
                creneaux.append((h1,h2))
            position = max(position, resa.get_fin_minutes())

        # verifier apres la derniere reservation
        if fin_journee - position >= duree_min:
            h1 = f"{position // 60:02d}:{position % 60:02d}"
            h2 = f"{fin_journee // 60:02d}:{fin_journee % 60:02d}"
            creneaux.append((h1, h2))

        return creneaux

    def rapport_conflits(self):
        """Genere un rapport sur les confits exixtants."""
        actives = [r for r in self._reservations if r.statut != "annulee"]
        conflits_trouves = []

        for i in range(len(actives)):
            for j in range(i + 1, len(actives)):
                if actives[i].chevauche(actives[j]):
                    conflits_trouves.append((actives[i], actives[j]))

        return {
            "total": len(self._reservations),
            "actives": len(actives),
            "nb_conflits": len(conflits_trouves),
            "conflits": conflits_trouves
        }