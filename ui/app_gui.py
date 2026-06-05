"""
Interface graphique du systeme de reservation.
Universite de Parakou.

Utilise Tkinter avec des onglets (Notebook) pour organiser
les differentes fonctionnalites.

Auteurs : ACODODJA Melaine, BAGNAN Abdel-Naguib

"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from models.salle import Salle, SalleCours, SalleTP, Amphitheatre
from models.utilisateur import Utilisateur
from services.reservation_service import ReservationService
from database.db_manager import DatabaseManager


class Application(tk.Tk):
    """Fenetre principale de l'application."""

    def __init__(self):
        super().__init__()

        self.title("Reservation de Salles - Univ. Parakou")
        self.geometry("950x650")

        # initialiser les services
        self.db = DatabaseManager()
        self.service = ReservationService()

        # charger des donnees de demo
        self._donnees_demo()

        # charger les reservations depuis la base de donnees
        self._charger_reservations()

        # construire l'interface
        self._menu()
        self._interface()

    def _donnees_demo(self):
        """Ajoute quelques salles et utilisateurs pour tester."""

        from models.salle import Salle as S
        from models.utilisateur import Utilisateur as U
        from models.reservation import Reservation as R
        S._compteur = 0
        U._compteur = 0
        R._compteur = 0    

        salles = [
            SalleCours("Solidarite R+1", 200, ["projecteur", "tableau"], "blanc"),
            SalleCours("Solidarite R+2", 180, ["projecteur"], "interactif"),
            SalleTP("Salle 13", 120, ["ordinateurs"], 50),
            SalleTP("Salle 14", 100, ["ordinateurs"], 55),
        ]
        for s in salles:
            self.service.ajouter_salle(s)

        users = [
            Utilisateur("Docteur", "docteur@gmail.com", "Docteur"),
            Utilisateur("Etudiant(e)", "etudiant@gmail.com", "Etudiant(e)"),
            Utilisateur("Secretariat", "secretariat@gmail.com", "Secretariat"),
        ]
        for u in users:
            self.service.ajouter_utilisateur(u)

    def _charger_reservations(self):
        """Charge les reservations depuis la base de donnees."""
        from models.reservation import Reservation
        resas_db = self.db.lire_reservations()
        for r in resas_db:
            salle = self.service.trouver_salle(r["salle_id"])
            user = self.service.trouver_utilisateur(r["utilisateur_id"])
            if salle and user:
                resa = Reservation(
                    salle, user,
                    r["date"], r["heure_debut"], r["heure_fin"],
                    r["motif"]
                )
                resa._statut = r["statut"]
                self.service._reservations.append(resa)

    def _menu(self):
        """Cree la barre de menu."""
        barre = tk.Menu(self)

        menu_fichier = tk.Menu(barre, tearoff=0)
        menu_fichier.add_command(
            label="Nouvelle reservation", command=self._formulaire_reservation
        )
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.quit)
        barre.add_cascade(label="Fichier", menu=menu_fichier)

        menu_aide = tk.Menu(barre, tearoff=0)
        menu_aide.add_command(label="Rafraichir", command=self._rafraichir_tout)
        barre.add_cascade(label="Aide", menu=menu_aide)

        self.config(menu=barre)

    def _interface(self):
        """Construit l'interface avec les 3 onglets."""
        cadre = ttk.Frame(self, padding=10)
        cadre.pack(fill=tk.BOTH, expand=True)

        # titre
        tk.Label(
            cadre, 
            text="Système de Réservation de Salles - Université de Parakou",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#1a73e8",
            pady=10
        ).pack(fill=tk.X,pady=(0, 10))

        # onglets
        self.onglets = ttk.Notebook(cadre)
        self.onglets.pack(fill=tk.BOTH, expand=True)

        self._onglet_salles()
        self._onglet_reservations()
        self._onglet_planning()

        # barre de statut en bas
        self.statut = ttk.Label(cadre, text="Pret.", relief=tk.SUNKEN)
        self.statut.pack(fill=tk.X, pady=(5, 0))

    def _onglet_salles(self):
        """Onglet pour gerer les salles."""
        frame = ttk.Frame(self.onglets, padding=10)
        self.onglets.add(frame, text="  Salles  ")

        colonnes = ("ID", "Nom", "Type", "Capacite", "Equipements", "Statut")
        self.tableau_salles = ttk.Treeview(
            frame, columns=colonnes, show="headings", height=12
        )
        for col in colonnes:
            self.tableau_salles.heading(col, text=col)
            self.tableau_salles.column(col, width=110)

        self.tableau_salles.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # boutons
        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Ajouter", command=self._formulaire_salle).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Supprimer", command=self._suppr_salle).pack(side=tk.LEFT, padx=5)

        self._maj_salles()

    def _onglet_reservations(self):
        """Onglet pour gerer les reservations."""
        frame = ttk.Frame(self.onglets, padding=10)
        self.onglets.add(frame, text="  Reservations  ")

        colonnes = ("ID", "Salle", "Utilisateur", "Date", "Debut", "Fin", "Motif", "Statut")
        self.tableau_resas = ttk.Treeview(
            frame, columns=colonnes, show="headings", height=12
        )
        for col in colonnes:
            self.tableau_resas.heading(col, text=col)
            self.tableau_resas.column(col, width=95)

        self.tableau_resas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Reserver", command=self._formulaire_reservation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Annuler", command=self._annuler_resa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Conflits ?", command=self._voir_conflits).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Rafraichir", command=self._maj_reservations).pack(side=tk.LEFT, padx=5)
        self._maj_reservations()

    def _onglet_planning(self):
        """Onglet pour voir le planning du jour."""
        frame = ttk.Frame(self.onglets, padding=10)
        self.onglets.add(frame, text="  Planning  ")

        # selection de la date
        haut = ttk.Frame(frame)
        haut.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(haut, text="Date (JJ/MM/AAAA) :").pack(side=tk.LEFT)
        self.champ_date = ttk.Entry(haut, width=15)
        self.champ_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.champ_date.pack(side=tk.LEFT, padx=5)
        ttk.Button(haut, text="Afficher", command=self._afficher_planning).pack(side=tk.LEFT)

        # zone de texte pour le planning
        self.zone_planning = tk.Text(frame, height=18, font=("Courier", 10))
        self.zone_planning.pack(fill=tk.BOTH, expand=True)

    # --- Formulaires ---

    def _formulaire_salle(self):
        """Ouvre un formulaire pour ajouter une salle."""
        fen = tk.Toplevel(self)
        fen.title("Ajouter une salle")
        fen.geometry("380x280")

        ttk.Label(fen, text="Nom :").pack(pady=3)
        e_nom = ttk.Entry(fen, width=25)
        e_nom.pack()

        ttk.Label(fen, text="Capacite :").pack(pady=3)
        e_cap = ttk.Entry(fen, width=25)
        e_cap.pack()

        ttk.Label(fen, text="Type :").pack(pady=3)
        c_type = ttk.Combobox(fen, values=["Cours", "TP", "Amphi"], state="readonly")
        c_type.set("Cours")
        c_type.pack()

        ttk.Label(fen, text="Equipements (separes par des virgules) :").pack(pady=3)
        e_equip = ttk.Entry(fen, width=25)
        e_equip.pack()

        def valider():
            nom = e_nom.get().strip()
            try:
                cap = int(e_cap.get().strip())
                if cap <= 0:
                    messagebox.showerror("Erreur", "La capacite doit etre positive")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Capacite invalide")
                return

            equips = [e.strip() for e in e_equip.get().split(",") if e.strip()]
            t = c_type.get()

            if t == "Cours":
                salle = SalleCours(nom, cap, equips)
            elif t == "TP":
                salle = SalleTP(nom, cap, equips)
            else:
                salle = Amphitheatre(nom, cap, equips)

            self.service.ajouter_salle(salle)
            self._maj_salles()
            self.statut.config(text=f"Salle {nom} ajoutee.")
            fen.destroy()

        ttk.Button(fen, text="Ajouter", command=valider).pack(pady=12)

    def _suppr_salle(self):
        """Supprime la salle selectionnee."""
        sel = self.tableau_salles.selection()
        if not sel:
            messagebox.showwarning("Attention", "Selectionnez une salle.")
            return

        vals = self.tableau_salles.item(sel[0])["values"]
        sid = int(vals[0])

        if messagebox.askyesno("Confirmer", "Supprimer cette salle ?"):
            self.service.supprimer_salle(sid)
            self._maj_salles()

    def _formulaire_reservation(self):
        """Ouvre le formulaire de reservation."""
        fen = tk.Toplevel(self)
        fen.title("Nouvelle Reservation")
        fen.geometry("400x380")

        # salle
        ttk.Label(fen, text="Salle :").pack(pady=3)
        salles = self.service.lister_salles()
        choix_salles = [f"{s.id} - {s.nom}" for s in salles]
        c_salle = ttk.Combobox(fen, values=choix_salles, state="readonly", width=28)
        if choix_salles:
            c_salle.set(choix_salles[0])
        c_salle.pack()

        # utilisateur
        ttk.Label(fen, text="Utilisateur :").pack(pady=3)
        users = self.service.lister_utilisateurs()
        choix_users = [f"{u.id} - {u.nom}" for u in users]
        c_user = ttk.Combobox(fen, values=choix_users, state="readonly", width=28)
        if choix_users:
            c_user.set(choix_users[0])
        c_user.pack()

        # date
        ttk.Label(fen, text="Date (JJ/MM/AAAA) :").pack(pady=3)
        e_date = ttk.Entry(fen, width=28)
        e_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        e_date.pack()

        # heures
        ttk.Label(fen, text="Heure debut (HH:MM) :").pack(pady=3)
        e_debut = ttk.Entry(fen, width=28)
        e_debut.insert(0, "07:00")
        e_debut.pack()

        ttk.Label(fen, text="Heure fin (HH:MM) :").pack(pady=3)
        e_fin = ttk.Entry(fen, width=28)
        e_fin.insert(0, "09:00")
        e_fin.pack()

        # motif
        ttk.Label(fen, text="Motif :").pack(pady=3)
        e_motif = ttk.Entry(fen, width=28)
        e_motif.pack()

     
        def valider():
            sid = int(c_salle.get().split(" - ")[0])
            uid = int(c_user.get().split(" - ")[0])

            salle = self.service.trouver_salle(sid)
            user = self.service.trouver_utilisateur(uid)
            
            ok, res = self.service.creer_reservation(
                salle, user,
                e_date.get().strip(),
                e_debut.get().strip(),
                e_fin.get().strip(),
                e_motif.get().strip()
            )

            if ok:
                fen.destroy()
                self._maj_reservations()
                self.update()
                messagebox.showinfo("OK", "Reservation creee !")
                self.statut.config(text="Reservation ajoutee.")
            else:
                messagebox.showerror("Conflit !", res)

        ttk.Button(fen, text="Reserver", command=valider).pack(pady=12)
        

    def _annuler_resa(self):
        """Annule la reservation selectionnee."""
        sel = self.tableau_resas.selection()
        if not sel:
            messagebox.showwarning("Attention", "Selectionnez une reservation.")
            return

        vals = self.tableau_resas.item(sel[0])["values"]
        rid = int(vals[0])

        if messagebox.askyesno("Confirmer", "Annuler cette reservation ?"):
            self.service.annuler_reservation(rid)
            self._maj_reservations()
            self.statut.config(text=f"Reservation #{rid} annulee.")

    def _voir_conflits(self):
        """Affiche un rapport des conflits."""
        rapport = self.service.rapport_conflits()
        msg = (
            f"Total : {rapport['total']}\n"
            f"Actives : {rapport['actives']}\n"
            f"Conflits : {rapport['nb_conflits']}"
        )
        if rapport["nb_conflits"] > 0:
            msg += "\n\nDetails :"
            for r1, r2 in rapport["conflits"]:
                msg += f"\n  {r1} VS {r2}"
        messagebox.showinfo("Rapport", msg)

    def _afficher_planning(self):
        """Affiche le planning du jour dans la zone de texte."""
        date = self.champ_date.get().strip()
        self.zone_planning.delete("1.0", tk.END)

        self.zone_planning.insert(tk.END, f"Planning du {date}\n")
        self.zone_planning.insert(tk.END, "=" * 60 + "\n\n")

        for salle in self.service.lister_salles():
            self.zone_planning.insert(
                tk.END, f"  {salle.nom} ({salle.capacite} places)\n"
            )
            self.zone_planning.insert(tk.END, "-" * 40 + "\n")

            resas = self.service.lister_reservations(salle_id=salle.id, date=date)

            if resas:
                for r in resas:
                    self.zone_planning.insert(
                        tk.END,
                        f"  {r.heure_debut}-{r.heure_fin} | "
                        f"{r.utilisateur.nom} | {r.motif}\n"
                    )
            else:
                self.zone_planning.insert(tk.END, "  Libre\n")

            # creneaux libres
            libres = self.service.trouver_creneaux_libres(salle, date)
            if libres and resas:
                txt = "  Dispo : "
                for d, f in libres:
                    txt += f"[{d}-{f}] "
                self.zone_planning.insert(tk.END, txt + "\n")

            self.zone_planning.insert(tk.END, "\n")

    # --- Mise a jour des tableaux ---

    def _rafraichir_tout(self):
        self._maj_salles()
        self._maj_reservations()

    def _maj_salles(self):
        """Met a jour le tableau des salles."""
        for item in self.tableau_salles.get_children():
            self.tableau_salles.delete(item)

        for s in self.service.lister_salles():
            statut = "Dispo" if s.est_disponible else "Indispo"
            equip = ", ".join(s.equipements) if s.equipements else "-"
            self.tableau_salles.insert("", tk.END, values=(
                s.id, s.nom, s.__class__.__name__,
                s.capacite, equip, statut
            ))

    def _maj_reservations(self):
        """Met a jour le tableau des reservations."""
        for item in self.tableau_resas.get_children():
            self.tableau_resas.delete(item)

        for r in self.service.lister_reservations():
            nom_salle = r.salle.nom if r.salle else "Inconnue"
            nom_user = r.utilisateur.nom if r.utilisateur else "Inconnu"
            self.tableau_resas.insert("", tk.END, values=(
                r.id, nom_salle, nom_user,
                r.date, r.heure_debut, r.heure_fin,
                r.motif, r.statut
        ))


def lancer():
    """Lance l'application."""
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    lancer()