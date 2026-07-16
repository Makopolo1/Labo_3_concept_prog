
class Multiplex:
    def __init__(self, nom):
        self.nom = nom

        self._salles = []
        self._seances = []
        self._clients = []



    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if nom.strip() == "":
            raise ValueError("nom du multiplex vide")

        self._nom = nom.strip()



    #liste des salles
    @property
    def salles(self):
        return self._salles


    #liste des seances
    @property
    def seances(self):
        return self._seances


    #liste des clients
    @property
    def clients(self):
        return self._clients

 #ajouter une salle
    def ajouter_salle(self, salle):
        if salle is None:
            raise ValueError("salle invalide")

        self._salles.append(salle)


    #ajouter une seance
    def ajouter_seance(self, seance):
        if seance is None:
            raise ValueError("seance invalide")

        self._seances.append(seance)



    #ajouter un client
    def ajouter_client(self, client):
        if client is None:
            raise ValueError("client invalide")

        self._clients.append(client)


    #afficher les salles
    def afficher_salles(self):
        print("Salles du multiplex")

        for salle in self.salles:
            print("-", salle)



    #afficher les seances
    def afficher_seances(self):
        print("Seances disponibles")

        for seance in self.seances:
            print("-", seance)


    #afficher les clients
    def afficher_clients(self):
        print("Clients inscrits")

        for client in self.clients:
            print("-", client)



    #chercher un client avec son courriel
    def trouver_client(self, courriel):
        for client in self.clients:
            if client.courriel == courriel:
                return client

        raise ValueError("client introuvable")

 #chercher une salle avec son identifiant
    def trouver_salle(self, identifiant):
        for salle in self.salles:
            if salle.identifiant == identifiant:
                return salle

        raise ValueError("salle introuvable")



    #nombre total de places dans le multiplex
    def nombre_places_total(self):
        total = 0

        for salle in self.salles:
            total = total + salle.nombre_places()

        return total


    
    def __str__(self):
        return self.nom + " - " + str(len(self.salles)) + " salles"