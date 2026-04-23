"""
Gestionnaire de base de donnees SQLite.

Cree les tables, insere, lit, modifie et supprime les donnees.
SQLite est inclus dans Python donc pas besoin de pip install.

Auteurs: ACODODJA Melaine, BAGNAN Abdel-Naguib
"""

import sqlite3
import os


class DatabaseManager:
    """Gere toutes les operations avec la base de donnees."""

    def __init__(self, chemin="reservation_salles.db"):
        self._chemin = chemin
        self._conn = None
        self._creer_tables()

    def _connecter(self):
        """Ouvre la connexion si elle n'est pas deja ouverte."""
        if self._conn is None:
            self._conn = sqlite3.connect(self._chemin)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    def _creer_tables(self):
        """Cree les tables si elles n'existent pas encore."""
        conn = self._connecter()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS salles (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom TEXT NOT NULL UNIQUE,
                  capacite INTEGER NOT NULL,
                  equipements TEXT DEFAULT  '',
                  type_salle TEXT DEFAULT 'Salle',
                  disponible INTEGER DEFAULT 1
            )
        """)
      
        c.execute("""
          CREATE TABLE IF NOT EXISTS utilisateurs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                role TEXT DEFAULT 'enseignant'
          )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                  salle_id INTEGER NOT NULL,
                  utilisateur_id INTEGER NOT NULL,
                  date TEXT NOT NULL,
                  heure_debut TEXT NOT NULL,
                  heure_fin TEXT NOT NULL,
                  motif TEXT DEFAULT '',
                  statut TEXT DEFAULT 'confirmee',
                  cree_le TEXT NOT NULL,
                  FOREIGN KEY (salle_id) REFERENCES salles(id),
                  FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            ) 
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS ressources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom TEXT NOT NULL,
                  type_res TEXT NOT NULL,
                  quantite INTEGER DEFAULT 1,
                  disponible INTEGER DEFAULT 1
            )
        """)

        conn.commit()

    # --- Operations sur les salles ---

    def ajouter_salle(self, nom, capacite, equipements, type_salle):
        """Insere une salle. Retourne l'ID genere."""
        conn = self._connecter()
        c = conn.cursor()
        c.execute(
            "INSERT INTO salles (nom, capacite, equipements, type_salle) VALUES (?, ?, ?, ?)",
            (nom, capacite, equipements, type_salle)
        )   
        conn.commit()
        return c.lastrowid
    
    def lire_salles(self):
        """Retourne toutes les salles sous forme de liste de dicts."""
        conn = self._connecter()
        c = conn.cursor()
        c.execute("SELECT * FROM salles")
        return [dict(row) for row in c.fetchall()]
    
    def modifier_salle(self, salle_id, **kwargs):
        """Modifie les champs d'une salle."""
        conn = self._connecter()
        c = conn.cursor()
        for champ, valeur in kwargs.items():
            c.execute(
                f"UPDATE salles SET {champ} = ? WHERE id = ?",
                (valeur, salle_id)
            )
        conn.commit()

    def supprimer_salle(self, salle_id):
        conn = self._connecter()
        c = conn.cursor()
        c.execute("DELETE FROM salles WHERE id = ?", (salle_id,))
        conn.commit()

    # --- Operations sur les utilisateurs ---

    def ajouter_utilisateur(self, nom, email, rolr="enseignant"):
        conn = self._connecter()
        c = conn.cursor()
        c.execute(
            "INSERT INTO utilisateurs (nom, email, role) VALUES (?, ?, ?)",
            (nom, email, role)         
        ) 
        conn.commit()
        return c.lastrowid
    def lire_utilisateurs(self):
        conn = self._connecter()
        c = conn.cursor()
        c.execute("SELECT * FROM utilisateurs")
        return [dict(row) for row in c.fetchall()]
    
    # --- Operations sur les reservations ---

    def ajouter_reservation(self, salle_id, user_id, date, heure_debut, heure_fin, mptif, cree_le):
        conn = self._connecter()
        c = conn.cursor()
        c.execute(
            """INSERT INTO reservations
            (salle_id, utilisateur_id, date, heure_debut, heure_fin, motif, cree_le)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (salle_id, user_id, date, heure_debut, heure_fin, motif, cree_le)
        )
        conn.commit()
        return c.lastrowid
    def lire_reservations(self, salle_id=None, date=None):
        conn = self._connecter()
        c = conn.cursor()
        requete = "SELECT * FROM reservations WHERE statut != 'annulee'"
        params = []

        if salle_id:
            requete += " AND salle_id = ?"
            params.append(salle_id)
        if date:
            requete += " AND date = ?"
            params.append(date)

        requete += " ORDER BY date, heure_debut"
        c.execute(requete, params)
        return [dict(row) for row in c.fetchall()]
    
    def changer_statut_reservation(self, resa_id, statut):
        conn = self._connecter()
        c = conn.connecter()
        c.execute(
            "UPDATE reservations SET statut = ? WHERE id = ?",
            (statut, resa_id)
        )
        conn.commit()

    # --- Operations sur les ressources ---

    def ajouter_ressource(self, nom, type_res, quantite):
        conn = self._connecter()
        c = conn.cursor()
        c.execute(
            "INSERT INTO ressources (nom, type_res, quantite, disponible) VALUES (?, ?, ?, ?)",
            (nom, type_res, quantite, quantite)
        )
        conn.commit()
        return c.lastrowid
    def lire_ressources(self):
        conn = self._connecter()
        c = conn.cursor()
        c.execute("SELECT * FROM ressources")
        return [dict(row) for row in c.fetchall()]
    
    # --- Utilisataires ---

    def fermer(self):
        """Ferme la connexion."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def reinitialiser(self):
        """Supprime et recree la base (utile pour les tests)."""
        self.fermer()
        if os.path.exists(self._chemin):
            os.remove(self._chemin)
            self._creer_tables()

      

    


    
