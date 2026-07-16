
class Seance:
    def __init__(self, film, salle, date, heure):
        self.film = film
        self.salle = salle
        self.date = date
        self.heure = heure

        self._sieges_reserves = []



    #film de la seance
    @property
    def film(self):
        return self._film

    @film.setter
    def film(self, film):
        if film is None:
            raise ValueError("film invalide")
        self._film = film


    #salle de la seance
    @property
    def salle(self):
        return self._salle

    @salle.setter
    def salle(self, salle):
        if salle is None:
            raise ValueError("salle invalide")

        self._salle = salle



    #date de la seance
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if date.strip() == "":
            raise ValueError("date vide")

        self._date = date.strip()


    #heure de la seance
    @property
    def heure(self):
        return self._heure

    @heure.setter
    def heure(self, heure):
        if heure.strip() == "":
            raise ValueError("heure vide")
        self._heure = heure.strip()



    #liste des sieges reserves
    @property
    def sieges_reserves(self):
        return self._sieges_reserves


    #verifie si le siege existe dans la salle
    def siege_existe(self, siege):
        for siege_salle in self.salle.sieges:
            if siege_salle.est_pareil(siege):
                return True

        return False



    #verifie si le siege est libre
    def est_siege_libre(self, siege):
        for siege_reserve in self.sieges_reserves:
            if siege_reserve.est_pareil(siege):
                return False

        return True


    #reserver un siege
    def reserver_siege(self, siege):
        if not self.siege_existe(siege):
            raise ValueError("ce siege n'existe pas dans la salle")

        if not self.est_siege_libre(siege):
            raise ValueError("ce siege est deja reserve")

        self._sieges_reserves.append(siege)



    #nombre de places restantes
    def places_restantes(self):
        return self.salle.nombre_places() - len(self.sieges_reserves)


    #afficher le plan avec les reservations
    def afficher_plan(self):
        self.salle.afficher_plan(self.sieges_reserves)



    
    def __str__(self):
        return self.film.titre + " - " + self.date + " a " + self.heure + " - salle " + self.salle.identifiant