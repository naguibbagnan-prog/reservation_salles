"""
Module Utilisateur.

Represente les differents utilisateurs du systeme :
- etudiant : reserve pour travailler en groupe
- enseignant : reserve pour un cours ou reunion
- admin : gere les salles et supervise

Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib
"""


class Utilisateur:
    """Represente un utilisateur du systeme."""

    ROLES = ("etudiant", "enseignant", "admin")
    _compteur = 0

    def __init__(self, nom, email, role="enseignant"):
        if role not in self.ROLES:
            raise ValueError(f"Role invalide. Choix possibles : {self.ROLES}")

        Utilisateur._compteur += 1
        self._id = Utilisateur._compteur
        self._nom = nom
        self._email = email
        self._role = role

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nouveau):
        if not nouveau or len(nouveau.strip()) < 2:
            raise ValueError("Nom trop court")
        self._nom = nouveau.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, nouveau):
        if "@" not in nouveau:
            raise ValueError("Email invalide")
        self._email = nouveau

    @property
    def role(self):
        return self._role

    def __str__(self):
        return (
            f"Utilisateur : {self._nom}\n"
            f"Role        : {self._role}\n"
            f"Email       : {self._email}"
        )

    def __repr__(self):
        return f"Utilisateur('{self._nom}', '{self._email}')"

    def vers_dict(self):
        return {
            "id": self._id,
            "nom": self._nom,
            "email": self._email,
            "role": self._role
        }