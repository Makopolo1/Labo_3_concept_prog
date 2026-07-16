import tkinter as tk
from tkinter import ttk


class FenetreBillet(tk.Toplevel):
    def __init__(self, parent, reservation):
        super().__init__(parent)

        self.title("Billet CineRoyal")
        self.geometry("420x390")
        self.resizable(False, False)
        self.configure(bg="#1c2331")

        # La fenetre reste au-dessus de la fenetre principale
        self.transient(parent)
        self.grab_set()

        titre = tk.Label(
            self,
            text="CINEROYAL",
            font=("Arial", 22, "bold"),
            bg="#1c2331",
            fg="#f5c542"
        )
        titre.pack(pady=(20, 10))

        contenu = ttk.Frame(self, padding=20)
        contenu.pack(fill="both", expand=True, padx=25, pady=10)

        informations = [
            ("Client", reservation.client.nom),
            ("Film", reservation.seance.film.titre),
            ("Date", reservation.seance.date),
            ("Heure", reservation.seance.heure),
            ("Salle", reservation.seance.salle.identifiant),
            ("Siege", reservation.siege.code()),
            ("Billet", reservation.type_billet),
            ("Prix", str(reservation.prix_final) + " $")
        ]

        ligne = 0
        for nom, valeur in informations:
            ttk.Label(
                contenu,
                text=nom + " :",
                font=("Arial", 10, "bold")
            ).grid(row=ligne, column=0, sticky="w", padx=5, pady=5)

            ttk.Label(
                contenu,
                text=valeur
            ).grid(row=ligne, column=1, sticky="w", padx=5, pady=5)

            ligne = ligne + 1

        ttk.Button(
            self,
            text="Fermer",
            command=self.destroy
        ).pack(pady=15)
