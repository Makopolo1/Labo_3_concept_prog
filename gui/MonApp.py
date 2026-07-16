import tkinter as tk
from tkinter import ttk, messagebox

from labo_Finale.client import Client
from labo_Finale.film import Film
from labo_Finale.reservation import Reservation
from labo_Finale.seance import Seance
from persistance import sauvegarder, charger
from gui.FenetreBillet import FenetreBillet


class MonApp(tk.Tk):
    def __init__(self, modele):
        super().__init__()

        self.modele = modele

        self.title("CineRoyal - Gestion du cinema")
        self.geometry("1100x700")
        self.minsize(950, 600)
        self.configure(bg="#1c2331")

        self._configurer_style()
        self._creer_menu()
        self._creer_widgets()
        self._creer_raccourcis()
        self.rafraichir_tout()

    def _configurer_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background="#1c2331",
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            padding=(18, 9),
            font=("Arial", 10, "bold")
        )
        style.configure(
            "Titre.TLabel",
            font=("Arial", 20, "bold"),
            foreground="#b8860b"
        )
        style.configure(
            "SousTitre.TLabel",
            font=("Arial", 12, "bold")
        )
        style.configure(
            "Treeview",
            rowheight=27,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def _creer_menu(self):
        barre_menu = tk.Menu(self)

        menu_fichier = tk.Menu(barre_menu, tearoff=False)
        menu_fichier.add_command(
            label="Sauvegarder",
            command=self.sauvegarder_manuel,
            accelerator="Ctrl+S"
        )
        menu_fichier.add_command(
            label="Charger",
            command=self.charger_manuel
        )
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.destroy)

        menu_aide = tk.Menu(barre_menu, tearoff=False)
        menu_aide.add_command(label="A propos", command=self.afficher_a_propos)

        barre_menu.add_cascade(label="Fichier", menu=menu_fichier)
        barre_menu.add_cascade(label="Aide", menu=menu_aide)

        self.config(menu=barre_menu)

    def _creer_raccourcis(self):
        self.bind("<Control-s>", lambda evenement: self.sauvegarder_manuel())
        self.bind("<Control-n>", lambda evenement: self.entree_titre.focus_set())

    def _creer_widgets(self):
        entete = tk.Frame(self, bg="#1c2331", height=70)
        entete.pack(fill="x")

        tk.Label(
            entete,
            text="CINEROYAL",
            font=("Arial", 24, "bold"),
            bg="#1c2331",
            fg="#f5c542"
        ).pack(side="left", padx=25, pady=15)

        tk.Label(
            entete,
            text="Systeme de gestion du cinema",
            font=("Arial", 11),
            bg="#1c2331",
            fg="white"
        ).pack(side="left", pady=20)

        self.onglets = ttk.Notebook(self)
        self.onglets.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.onglet_accueil = ttk.Frame(self.onglets, padding=20)
        self.onglet_films = ttk.Frame(self.onglets, padding=15)
        self.onglet_clients = ttk.Frame(self.onglets, padding=15)
        self.onglet_seances = ttk.Frame(self.onglets, padding=15)
        self.onglet_reservations = ttk.Frame(self.onglets, padding=15)

        self.onglets.add(self.onglet_accueil, text="Accueil")
        self.onglets.add(self.onglet_films, text="Films")
        self.onglets.add(self.onglet_clients, text="Clients")
        self.onglets.add(self.onglet_seances, text="Seances")
        self.onglets.add(self.onglet_reservations, text="Reservations")

        self._creer_accueil()
        self._creer_section_films()
        self._creer_section_clients()
        self._creer_section_seances()
        self._creer_section_reservations()

    def _creer_accueil(self):
        ttk.Label(
            self.onglet_accueil,
            text="Tableau de bord",
            style="Titre.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        cadre_statistiques = ttk.Frame(self.onglet_accueil)
        cadre_statistiques.pack(fill="x")

        self.texte_films = tk.StringVar()
        self.texte_clients = tk.StringVar()
        self.texte_seances = tk.StringVar()
        self.texte_reservations = tk.StringVar()

        statistiques = [
            ("Films", self.texte_films),
            ("Clients", self.texte_clients),
            ("Seances", self.texte_seances),
            ("Reservations", self.texte_reservations)
        ]

        colonne = 0
        for titre, variable in statistiques:
            cadre = ttk.LabelFrame(
                cadre_statistiques,
                text=titre,
                padding=20
            )
            cadre.grid(row=0, column=colonne, padx=8, sticky="nsew")

            ttk.Label(
                cadre,
                textvariable=variable,
                font=("Arial", 24, "bold")
            ).pack()

            cadre_statistiques.columnconfigure(colonne, weight=1)
            colonne = colonne + 1

        cadre_places = ttk.LabelFrame(
            self.onglet_accueil,
            text="Occupation des seances",
            padding=20
        )
        cadre_places.pack(fill="x", pady=25)

        self.texte_occupation = tk.StringVar()
        ttk.Label(
            cadre_places,
            textvariable=self.texte_occupation
        ).pack(anchor="w", pady=(0, 10))

        self.barre_occupation = ttk.Progressbar(
            cadre_places,
            maximum=100
        )
        self.barre_occupation.pack(fill="x")

        cadre_actions = ttk.Frame(self.onglet_accueil)
        cadre_actions.pack(anchor="w", pady=10)

        ttk.Button(
            cadre_actions,
            text="Sauvegarder maintenant",
            command=self.sauvegarder_manuel
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            cadre_actions,
            text="Charger la sauvegarde",
            command=self.charger_manuel
        ).pack(side="left")

    def _creer_section_films(self):
        self.onglet_films.columnconfigure(1, weight=1)
        self.onglet_films.rowconfigure(1, weight=1)

        ttk.Label(
            self.onglet_films,
            text="Gestion des films",
            style="Titre.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        formulaire = ttk.LabelFrame(
            self.onglet_films,
            text="Formulaire du film",
            padding=15
        )
        formulaire.grid(row=1, column=0, sticky="ns", padx=(0, 15))

        ttk.Label(formulaire, text="Titre").grid(row=0, column=0, sticky="w")
        self.entree_titre = ttk.Entry(formulaire, width=28)
        self.entree_titre.grid(row=1, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Duree en minutes").grid(row=2, column=0, sticky="w")
        self.entree_duree = ttk.Entry(formulaire, width=28)
        self.entree_duree.grid(row=3, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Genre").grid(row=4, column=0, sticky="w")
        self.entree_genre = ttk.Entry(formulaire, width=28)
        self.entree_genre.grid(row=5, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Classification").grid(row=6, column=0, sticky="w")
        self.combo_classification = ttk.Combobox(
            formulaire,
            values=["G", "13+", "16+", "18+"],
            state="readonly",
            width=25
        )
        self.combo_classification.grid(row=7, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Langue").grid(row=8, column=0, sticky="w")
        self.entree_langue = ttk.Entry(formulaire, width=28)
        self.entree_langue.grid(row=9, column=0, pady=(2, 15))

        ttk.Button(formulaire, text="Ajouter", command=self.ajouter_film).grid(row=10, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Modifier", command=self.modifier_film).grid(row=11, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Supprimer", command=self.supprimer_film).grid(row=12, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Vider", command=self.vider_formulaire_film).grid(row=13, column=0, sticky="ew", pady=2)

        zone_liste = ttk.Frame(self.onglet_films)
        zone_liste.grid(row=1, column=1, sticky="nsew")
        zone_liste.columnconfigure(0, weight=1)
        zone_liste.rowconfigure(1, weight=1)

        recherche = ttk.Frame(zone_liste)
        recherche.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(recherche, text="Rechercher :").pack(side="left")

        self.recherche_film = tk.StringVar()
        self.recherche_film.trace_add("write", lambda *args: self.rafraichir_films())
        ttk.Entry(recherche, textvariable=self.recherche_film).pack(side="left", fill="x", expand=True, padx=8)

        colonnes = ("titre", "duree", "genre", "classification", "langue")
        self.liste_films = ttk.Treeview(zone_liste, columns=colonnes, show="headings")
        self.liste_films.grid(row=1, column=0, sticky="nsew")

        titres = ["Titre", "Duree", "Genre", "Classification", "Langue"]
        self._preparer_colonnes(self.liste_films, colonnes, titres)
        self.liste_films.bind("<<TreeviewSelect>>", self.selectionner_film)

    def _creer_section_clients(self):
        self.onglet_clients.columnconfigure(1, weight=1)
        self.onglet_clients.rowconfigure(1, weight=1)

        ttk.Label(
            self.onglet_clients,
            text="Gestion des clients",
            style="Titre.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        formulaire = ttk.LabelFrame(
            self.onglet_clients,
            text="Formulaire du client",
            padding=15
        )
        formulaire.grid(row=1, column=0, sticky="ns", padx=(0, 15))

        ttk.Label(formulaire, text="Nom").grid(row=0, column=0, sticky="w")
        self.entree_nom = ttk.Entry(formulaire, width=28)
        self.entree_nom.grid(row=1, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Courriel").grid(row=2, column=0, sticky="w")
        self.entree_courriel = ttk.Entry(formulaire, width=28)
        self.entree_courriel.grid(row=3, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Age").grid(row=4, column=0, sticky="w")
        self.entree_age = ttk.Spinbox(formulaire, from_=1, to=120, width=26)
        self.entree_age.grid(row=5, column=0, pady=(2, 10))

        self.valeur_fidelite = tk.BooleanVar()
        ttk.Checkbutton(
            formulaire,
            text="Carte de fidelite",
            variable=self.valeur_fidelite
        ).grid(row=6, column=0, sticky="w", pady=(2, 15))

        ttk.Button(formulaire, text="Ajouter", command=self.ajouter_client).grid(row=7, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Modifier", command=self.modifier_client).grid(row=8, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Supprimer", command=self.supprimer_client).grid(row=9, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Vider", command=self.vider_formulaire_client).grid(row=10, column=0, sticky="ew", pady=2)

        zone_liste = ttk.Frame(self.onglet_clients)
        zone_liste.grid(row=1, column=1, sticky="nsew")
        zone_liste.columnconfigure(0, weight=1)
        zone_liste.rowconfigure(1, weight=1)

        recherche = ttk.Frame(zone_liste)
        recherche.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(recherche, text="Rechercher :").pack(side="left")

        self.recherche_client = tk.StringVar()
        self.recherche_client.trace_add("write", lambda *args: self.rafraichir_clients())
        ttk.Entry(recherche, textvariable=self.recherche_client).pack(side="left", fill="x", expand=True, padx=8)

        colonnes = ("nom", "courriel", "age", "fidelite")
        self.liste_clients = ttk.Treeview(zone_liste, columns=colonnes, show="headings")
        self.liste_clients.grid(row=1, column=0, sticky="nsew")

        titres = ["Nom", "Courriel", "Age", "Fidelite"]
        self._preparer_colonnes(self.liste_clients, colonnes, titres)
        self.liste_clients.bind("<<TreeviewSelect>>", self.selectionner_client)

    def _creer_section_seances(self):
        self.onglet_seances.columnconfigure(1, weight=1)
        self.onglet_seances.rowconfigure(1, weight=1)

        ttk.Label(
            self.onglet_seances,
            text="Gestion des seances",
            style="Titre.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        formulaire = ttk.LabelFrame(
            self.onglet_seances,
            text="Formulaire de la seance",
            padding=15
        )
        formulaire.grid(row=1, column=0, sticky="ns", padx=(0, 15))

        ttk.Label(formulaire, text="Film").grid(row=0, column=0, sticky="w")
        self.combo_film_seance = ttk.Combobox(formulaire, state="readonly", width=29)
        self.combo_film_seance.grid(row=1, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Salle").grid(row=2, column=0, sticky="w")
        self.combo_salle_seance = ttk.Combobox(formulaire, state="readonly", width=29)
        self.combo_salle_seance.grid(row=3, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Date ou jour").grid(row=4, column=0, sticky="w")
        self.entree_date = ttk.Entry(formulaire, width=32)
        self.entree_date.grid(row=5, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Heure").grid(row=6, column=0, sticky="w")
        self.entree_heure = ttk.Entry(formulaire, width=32)
        self.entree_heure.grid(row=7, column=0, pady=(2, 15))

        ttk.Button(formulaire, text="Ajouter", command=self.ajouter_seance).grid(row=8, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Modifier", command=self.modifier_seance).grid(row=9, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Supprimer", command=self.supprimer_seance).grid(row=10, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Vider", command=self.vider_formulaire_seance).grid(row=11, column=0, sticky="ew", pady=2)

        colonnes = ("film", "date", "heure", "salle", "places")
        self.liste_seances = ttk.Treeview(self.onglet_seances, columns=colonnes, show="headings")
        self.liste_seances.grid(row=1, column=1, sticky="nsew")

        titres = ["Film", "Date", "Heure", "Salle", "Places libres"]
        self._preparer_colonnes(self.liste_seances, colonnes, titres)
        self.liste_seances.bind("<<TreeviewSelect>>", self.selectionner_seance)

    def _creer_section_reservations(self):
        self.onglet_reservations.columnconfigure(1, weight=1)
        self.onglet_reservations.rowconfigure(1, weight=1)

        ttk.Label(
            self.onglet_reservations,
            text="Gestion des reservations",
            style="Titre.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        formulaire = ttk.LabelFrame(
            self.onglet_reservations,
            text="Nouvelle reservation",
            padding=15
        )
        formulaire.grid(row=1, column=0, sticky="ns", padx=(0, 15))

        ttk.Label(formulaire, text="Client").grid(row=0, column=0, sticky="w")
        self.combo_client_reservation = ttk.Combobox(formulaire, state="readonly", width=33)
        self.combo_client_reservation.grid(row=1, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Seance").grid(row=2, column=0, sticky="w")
        self.combo_seance_reservation = ttk.Combobox(formulaire, state="readonly", width=33)
        self.combo_seance_reservation.grid(row=3, column=0, pady=(2, 10))
        self.combo_seance_reservation.bind("<<ComboboxSelected>>", self.mettre_a_jour_sieges)

        ttk.Label(formulaire, text="Type de billet").grid(row=4, column=0, sticky="w")
        self.combo_type_billet = ttk.Combobox(
            formulaire,
            values=["regulier", "etudiant", "aine", "enfant"],
            state="readonly",
            width=33
        )
        self.combo_type_billet.grid(row=5, column=0, pady=(2, 10))

        ttk.Label(formulaire, text="Siege disponible").grid(row=6, column=0, sticky="w")
        self.combo_siege = ttk.Combobox(formulaire, state="readonly", width=33)
        self.combo_siege.grid(row=7, column=0, pady=(2, 15))

        ttk.Button(formulaire, text="Reserver", command=self.ajouter_reservation).grid(row=8, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Annuler la reservation", command=self.annuler_reservation).grid(row=9, column=0, sticky="ew", pady=2)
        ttk.Button(formulaire, text="Afficher le billet", command=self.afficher_billet_selectionne).grid(row=10, column=0, sticky="ew", pady=2)

        colonnes = ("client", "film", "date", "siege", "type", "prix")
        self.liste_reservations = ttk.Treeview(
            self.onglet_reservations,
            columns=colonnes,
            show="headings"
        )
        self.liste_reservations.grid(row=1, column=1, sticky="nsew")

        titres = ["Client", "Film", "Date", "Siege", "Billet", "Prix"]
        self._preparer_colonnes(self.liste_reservations, colonnes, titres)

    def _preparer_colonnes(self, tableau, colonnes, titres):
        index = 0
        for colonne in colonnes:
            tableau.heading(
                colonne,
                text=titres[index],
                command=lambda c=colonne: self.trier_tableau(tableau, c, False)
            )
            tableau.column(colonne, width=125, anchor="center")
            index = index + 1

    def trier_tableau(self, tableau, colonne, inverse):
        donnees = []
        for element in tableau.get_children(""):
            donnees.append((tableau.set(element, colonne), element))

        donnees.sort(reverse=inverse)

        position = 0
        for valeur, element in donnees:
            tableau.move(element, "", position)
            position = position + 1

        tableau.heading(
            colonne,
            command=lambda: self.trier_tableau(tableau, colonne, not inverse)
        )

    def obtenir_index_selectionne(self, tableau):
        selection = tableau.selection()
        if len(selection) == 0:
            raise ValueError("vous devez selectionner un element")
        return int(selection[0])

    # ---------------- FILMS ----------------

    def ajouter_film(self):
        try:
            film = Film(
                self.entree_titre.get(),
                int(self.entree_duree.get()),
                self.entree_genre.get(),
                self.combo_classification.get(),
                self.entree_langue.get()
            )
            self.modele.ajouter_film(film)
            self.apres_modification("Film ajoute")
            self.vider_formulaire_film()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def modifier_film(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_films)
            film = self.modele.films[index]

            nouveau_titre = self.entree_titre.get().strip()
            for autre_film in self.modele.films:
                if autre_film is not film and autre_film.titre.lower() == nouveau_titre.lower():
                    raise ValueError("ce film existe deja")

            film.titre = nouveau_titre
            film.duree = int(self.entree_duree.get())
            film.genre = self.entree_genre.get()
            film.classification = self.combo_classification.get()
            film.langue = self.entree_langue.get()

            self.apres_modification("Film modifie")
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def supprimer_film(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_films)
            film = self.modele.films[index]

            for seance in self.modele.seances:
                if seance.film is film:
                    raise ValueError("ce film est utilise dans une seance")

            if messagebox.askyesno("Confirmation", "Supprimer ce film?"):
                self.modele.films.remove(film)
                self.apres_modification("Film supprime")
                self.vider_formulaire_film()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def selectionner_film(self, evenement=None):
        try:
            index = self.obtenir_index_selectionne(self.liste_films)
            film = self.modele.films[index]

            self.vider_formulaire_film()
            self.entree_titre.insert(0, film.titre)
            self.entree_duree.insert(0, str(film.duree))
            self.entree_genre.insert(0, film.genre)
            self.combo_classification.set(film.classification)
            self.entree_langue.insert(0, film.langue)
        except ValueError:
            pass

    def vider_formulaire_film(self):
        self.entree_titre.delete(0, "end")
        self.entree_duree.delete(0, "end")
        self.entree_genre.delete(0, "end")
        self.combo_classification.set("")
        self.entree_langue.delete(0, "end")

    # ---------------- CLIENTS ----------------

    def ajouter_client(self):
        try:
            client = Client(
                self.entree_nom.get(),
                self.entree_courriel.get(),
                int(self.entree_age.get()),
                self.valeur_fidelite.get()
            )
            self.modele.ajouter_client(client)
            self.apres_modification("Client ajoute")
            self.vider_formulaire_client()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def modifier_client(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_clients)
            client = self.modele.clients[index]
            nouveau_courriel = self.entree_courriel.get().strip().lower()

            for autre_client in self.modele.clients:
                if autre_client is not client and autre_client.courriel == nouveau_courriel:
                    raise ValueError("ce courriel est deja utilise")

            client.nom = self.entree_nom.get()
            client.courriel = nouveau_courriel
            client.age = int(self.entree_age.get())
            client.carte_fidelite = self.valeur_fidelite.get()

            self.apres_modification("Client modifie")
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def supprimer_client(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_clients)
            client = self.modele.clients[index]

            if len(client.reservations) > 0:
                raise ValueError("ce client possede des reservations")

            if messagebox.askyesno("Confirmation", "Supprimer ce client?"):
                self.modele.clients.remove(client)
                self.apres_modification("Client supprime")
                self.vider_formulaire_client()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def selectionner_client(self, evenement=None):
        try:
            index = self.obtenir_index_selectionne(self.liste_clients)
            client = self.modele.clients[index]

            self.vider_formulaire_client()
            self.entree_nom.insert(0, client.nom)
            self.entree_courriel.insert(0, client.courriel)
            self.entree_age.delete(0, "end")
            self.entree_age.insert(0, str(client.age))
            self.valeur_fidelite.set(client.carte_fidelite)
        except ValueError:
            pass

    def vider_formulaire_client(self):
        self.entree_nom.delete(0, "end")
        self.entree_courriel.delete(0, "end")
        self.entree_age.delete(0, "end")
        self.valeur_fidelite.set(False)

    # ---------------- SEANCES ----------------

    def ajouter_seance(self):
        try:
            film = self.modele.trouver_film(self.combo_film_seance.get())
            salle = self.modele.trouver_salle(self.combo_salle_seance.get())
            seance = Seance(film, salle, self.entree_date.get(), self.entree_heure.get())

            self.modele.ajouter_seance(seance)
            self.apres_modification("Seance ajoutee")
            self.vider_formulaire_seance()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def modifier_seance(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_seances)
            seance = self.modele.seances[index]

            if len(seance.sieges_reserves) > 0:
                raise ValueError("une seance reservee ne peut pas etre modifiee")

            seance.film = self.modele.trouver_film(self.combo_film_seance.get())
            seance.salle = self.modele.trouver_salle(self.combo_salle_seance.get())
            seance.date = self.entree_date.get()
            seance.heure = self.entree_heure.get()

            self.apres_modification("Seance modifiee")
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def supprimer_seance(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_seances)
            seance = self.modele.seances[index]

            if len(seance.sieges_reserves) > 0:
                raise ValueError("cette seance possede des reservations")

            if messagebox.askyesno("Confirmation", "Supprimer cette seance?"):
                self.modele.seances.remove(seance)
                self.apres_modification("Seance supprimee")
                self.vider_formulaire_seance()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def selectionner_seance(self, evenement=None):
        try:
            index = self.obtenir_index_selectionne(self.liste_seances)
            seance = self.modele.seances[index]

            self.combo_film_seance.set(seance.film.titre)
            self.combo_salle_seance.set(seance.salle.identifiant)
            self.entree_date.delete(0, "end")
            self.entree_date.insert(0, seance.date)
            self.entree_heure.delete(0, "end")
            self.entree_heure.insert(0, seance.heure)
        except ValueError:
            pass

    def vider_formulaire_seance(self):
        self.combo_film_seance.set("")
        self.combo_salle_seance.set("")
        self.entree_date.delete(0, "end")
        self.entree_heure.delete(0, "end")

    # ---------------- RESERVATIONS ----------------

    def mettre_a_jour_sieges(self, evenement=None):
        try:
            seance = self.modele.trouver_seance(self.combo_seance_reservation.get())
            sieges_libres = []

            for siege in seance.salle.sieges:
                if seance.est_siege_libre(siege):
                    sieges_libres.append(siege.code())

            self.combo_siege["values"] = sieges_libres
            self.combo_siege.set("")
        except ValueError:
            self.combo_siege["values"] = []

    def ajouter_reservation(self):
        try:
            client = self.modele.trouver_client(self.combo_client_reservation.get())
            seance = self.modele.trouver_seance(self.combo_seance_reservation.get())
            siege = seance.salle.trouver_siege(self.combo_siege.get())

            reservation = Reservation(
                client,
                seance,
                siege,
                self.combo_type_billet.get()
            )

            self.apres_modification("Reservation creee")
            self.mettre_a_jour_sieges()
            FenetreBillet(self, reservation)
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def annuler_reservation(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_reservations)
            reservation = self.modele.reservations[index]

            if messagebox.askyesno("Confirmation", "Annuler cette reservation?"):
                reservation.annuler()
                self.apres_modification("Reservation annulee")
                self.mettre_a_jour_sieges()
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def afficher_billet_selectionne(self):
        try:
            index = self.obtenir_index_selectionne(self.liste_reservations)
            FenetreBillet(self, self.modele.reservations[index])
        except ValueError as erreur:
            messagebox.showerror("Erreur", str(erreur))

    # ---------------- RAFRAICHISSEMENT ----------------

    def vider_tableau(self, tableau):
        for element in tableau.get_children():
            tableau.delete(element)

    def rafraichir_films(self):
        self.vider_tableau(self.liste_films)
        recherche = self.recherche_film.get().strip().lower()

        index = 0
        for film in self.modele.films:
            texte = film.titre.lower() + " " + film.genre.lower()
            if recherche in texte:
                self.liste_films.insert(
                    "",
                    "end",
                    iid=str(index),
                    values=(film.titre, film.duree, film.genre, film.classification, film.langue)
                )
            index = index + 1

    def rafraichir_clients(self):
        self.vider_tableau(self.liste_clients)
        recherche = self.recherche_client.get().strip().lower()

        index = 0
        for client in self.modele.clients:
            texte = client.nom.lower() + " " + client.courriel.lower()
            if recherche in texte:
                if client.carte_fidelite:
                    fidelite = "Oui"
                else:
                    fidelite = "Non"

                self.liste_clients.insert(
                    "",
                    "end",
                    iid=str(index),
                    values=(client.nom, client.courriel, client.age, fidelite)
                )
            index = index + 1

    def rafraichir_seances(self):
        self.vider_tableau(self.liste_seances)

        index = 0
        for seance in self.modele.seances:
            self.liste_seances.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    seance.film.titre,
                    seance.date,
                    seance.heure,
                    seance.salle.identifiant,
                    seance.places_restantes()
                )
            )
            index = index + 1

    def rafraichir_reservations(self):
        self.vider_tableau(self.liste_reservations)

        index = 0
        for reservation in self.modele.reservations:
            self.liste_reservations.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    reservation.client.nom,
                    reservation.seance.film.titre,
                    reservation.seance.date,
                    reservation.siege.code(),
                    reservation.type_billet,
                    str(reservation.prix_final) + " $"
                )
            )
            index = index + 1

    def rafraichir_combobox(self):
        films = []
        salles = []
        clients = []
        seances = []

        for film in self.modele.films:
            films.append(film.titre)
        for salle in self.modele.salles:
            salles.append(salle.identifiant)
        for client in self.modele.clients:
            clients.append(client.courriel)
        for seance in self.modele.seances:
            seances.append(seance.code())

        self.combo_film_seance["values"] = films
        self.combo_salle_seance["values"] = salles
        self.combo_client_reservation["values"] = clients
        self.combo_seance_reservation["values"] = seances

    def rafraichir_statistiques(self):
        self.texte_films.set(str(len(self.modele.films)))
        self.texte_clients.set(str(len(self.modele.clients)))
        self.texte_seances.set(str(len(self.modele.seances)))
        self.texte_reservations.set(str(len(self.modele.reservations)))

        places_total = 0
        for seance in self.modele.seances:
            places_total = places_total + seance.salle.nombre_places()

        places_reservees = len(self.modele.reservations)

        if places_total == 0:
            pourcentage = 0
        else:
            pourcentage = (places_reservees / places_total) * 100

        self.texte_occupation.set(
            str(places_reservees)
            + " places reservees sur "
            + str(places_total)
        )
        self.barre_occupation["value"] = pourcentage

    def rafraichir_tout(self):
        self.rafraichir_films()
        self.rafraichir_clients()
        self.rafraichir_seances()
        self.rafraichir_reservations()
        self.rafraichir_combobox()
        self.rafraichir_statistiques()

    def apres_modification(self, message):
        self.rafraichir_tout()

        try:
            sauvegarder(self.modele)
        except OSError as erreur:
            messagebox.showerror("Erreur de sauvegarde", str(erreur))
            return

        messagebox.showinfo("Succes", message)

    def sauvegarder_manuel(self):
        try:
            sauvegarder(self.modele)
            messagebox.showinfo("Sauvegarde", "Les donnees ont ete sauvegardees")
        except OSError as erreur:
            messagebox.showerror("Erreur de sauvegarde", str(erreur))

    def charger_manuel(self):
        try:
            self.modele = charger()
            self.rafraichir_tout()
            messagebox.showinfo("Chargement", "Les donnees ont ete chargees")
        except (ValueError, OSError) as erreur:
            messagebox.showerror("Erreur de chargement", str(erreur))

    def afficher_a_propos(self):
        messagebox.showinfo(
            "A propos",
            "CineRoyal - Laboratoire 3\n\n"
            "Nathan Demers\n"
            "Marc Rolen\n"
            "Cherry Emnley Moushi"
        )
