from client import Client
from film import Film
from reservation import Reservation
from salle_standard import SalleStandard
from salle_imax import SalleIMAX
from salle_vip import SalleVIP
from seance import Seance


class Multiplex:
    def __init__(self, nom):
        self.nom = nom
        self._salles = []
        self._films = []
        self._seances = []
        self._clients = []

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom, str) or nom.strip() == "":
            raise ValueError("nom du multiplex vide")
        self._nom = nom.strip()

    @property
    def salles(self):
        return self._salles

    @property
    def films(self):
        return self._films

    @property
    def seances(self):
        return self._seances

    @property
    def clients(self):
        return self._clients

    @property
    def reservations(self):
        liste = []
        for client in self.clients:
            for reservation in client.reservations:
                liste.append(reservation)
        return liste

    def ajouter_salle(self, salle):
        for salle_existante in self.salles:
            if salle_existante.identifiant == salle.identifiant:
                raise ValueError("une salle avec cet identifiant existe deja")
        self._salles.append(salle)

    def ajouter_film(self, film):
        for film_existant in self.films:
            if film_existant.titre.lower() == film.titre.lower():
                raise ValueError("ce film existe deja")
        self._films.append(film)

    def ajouter_seance(self, seance):
        for seance_existante in self.seances:
            if seance_existante.code() == seance.code():
                raise ValueError("cette seance existe deja")
        self._seances.append(seance)

    def ajouter_client(self, client):
        for client_existant in self.clients:
            if client_existant.courriel == client.courriel:
                raise ValueError("ce courriel est deja utilise")
        self._clients.append(client)

    def trouver_client(self, courriel):
        for client in self.clients:
            if client.courriel == courriel:
                return client
        raise ValueError("client introuvable")

    def trouver_film(self, titre):
        for film in self.films:
            if film.titre == titre:
                return film
        raise ValueError("film introuvable")

    def trouver_salle(self, identifiant):
        for salle in self.salles:
            if salle.identifiant == identifiant:
                return salle
        raise ValueError("salle introuvable")

    def trouver_seance(self, code):
        for seance in self.seances:
            if seance.code() == code:
                return seance
        raise ValueError("seance introuvable")

    def nombre_places_total(self):
        total = 0
        for salle in self.salles:
            total = total + salle.nombre_places()
        return total

    def to_dict(self):
        salles = []
        films = []
        clients = []
        seances = []
        reservations = []

        for salle in self.salles:
            salles.append(salle.to_dict())
        for film in self.films:
            films.append(film.to_dict())
        for client in self.clients:
            clients.append(client.to_dict())
        for seance in self.seances:
            seances.append(seance.to_dict())
        for reservation in self.reservations:
            reservations.append(reservation.to_dict())

        return {
            "nom": self.nom,
            "salles": salles,
            "films": films,
            "clients": clients,
            "seances": seances,
            "reservations": reservations
        }

    @classmethod
    def from_dict(cls, donnees):
        cinema = cls(donnees.get("nom", "CineRoyal"))

        for donnees_salle in donnees.get("salles", []):
            type_salle = donnees_salle["type"]

            if type_salle == "SalleIMAX":
                salle = SalleIMAX.from_dict(donnees_salle)
            elif type_salle == "SalleVIP":
                salle = SalleVIP.from_dict(donnees_salle)
            else:
                salle = SalleStandard.from_dict(donnees_salle)

            cinema.ajouter_salle(salle)

        clients_par_courriel = {}
        for donnees_client in donnees.get("clients", []):
            client = Client.from_dict(donnees_client)
            cinema.ajouter_client(client)
            clients_par_courriel[client.courriel] = client

        for donnees_film in donnees.get("films", []):
            film = Film.from_dict(donnees_film, clients_par_courriel)
            cinema.ajouter_film(film)

        for donnees_seance in donnees.get("seances", []):
            film = cinema.trouver_film(donnees_seance["film"])
            salle = cinema.trouver_salle(donnees_seance["salle"])
            seance = Seance.from_dict(donnees_seance, film, salle)
            cinema.ajouter_seance(seance)

        for donnees_reservation in donnees.get("reservations", []):
            client = cinema.trouver_client(donnees_reservation["client"])
            seance = cinema.trouver_seance(donnees_reservation["seance"])
            siege = seance.salle.trouver_siege(donnees_reservation["siege"])
            Reservation.from_dict(
                donnees_reservation,
                client,
                seance,
                siege
            )

        return cinema

    def __str__(self):
        return self.nom + " - " + str(len(self.salles)) + " salles"
