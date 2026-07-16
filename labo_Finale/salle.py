
from abc import ABC, abstractmethod
from siege import Siege


class Salle(ABC):
    def __init__(self, identifiant, nb_rangees, sieges_par_rangee):
        self.identifiant = identifiant
        self.nb_rangees = nb_rangees
        self.sieges_par_rangee = sieges_par_rangee
        self._sieges = []
        self.generer_sieges()


    #identifiant
    @property
    def identifiant(self):
        return self._identifiant

    @identifiant.setter
    def identifiant(self, identifiant):
        if identifiant.strip() == "":
            raise ValueError("identifiant de la salle vide")
        self._identifiant = identifiant.strip()

    #rangee
    @property
    def nb_rangees(self):
        return self._nb_rangees

    @nb_rangees.setter
    def nb_rangees(self, nb_rangees):
        if nb_rangees <= 0:
            raise ValueError("nombre de rangees invalide")

        if nb_rangees > 26:
            raise ValueError("maximum 26 rangees")

        self._nb_rangees = nb_rangees


    #sieges par rangee
    @property
    def sieges_par_rangee(self):
        return self._sieges_par_rangee

    @sieges_par_rangee.setter
    def sieges_par_rangee(self, sieges_par_rangee):
        if sieges_par_rangee <= 0:
            raise ValueError("nombre de sieges invalide")
        self._sieges_par_rangee = sieges_par_rangee



    #retourne la liste des sieges
    @property
    def sieges(self):
        return self._sieges


    #creer les sieges de la salle
    def generer_sieges(self):
        lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self._sieges = []

        for i in range(self.nb_rangees):
            rangee = lettres[i]

            for numero in range(1, self.sieges_par_rangee + 1):
                siege = Siege(rangee, numero)
                self._sieges.append(siege)


    #nombre de place total
    def nombre_places(self):
        return len(self.sieges)



    #chercher un siege avec son code
    def trouver_siege(self, code):
        if code.strip() == "":
            raise ValueError("code du siege vide")

        code = code.strip().upper()

        for siege in self.sieges:
            if siege.code() == code:
                return siege

        raise ValueError("siege introuvable")


    #afficher plan
    def afficher_plan(self, sieges_reserves=None):
        if sieges_reserves is None:
            sieges_reserves = []

        print()
        print("Plan de la salle", self.identifiant)
        print("-" * 40)

        index = 0

        for i in range(self.nb_rangees):
            ligne = ""

            for j in range(self.sieges_par_rangee):
                siege = self.sieges[index]
                reserve = False

                for siege_reserve in sieges_reserves:
                    if siege.est_pareil(siege_reserve):
                        reserve = True

                if reserve:
                    ligne = ligne + "[XX] "
                else:
                    ligne = ligne + "[" + siege.code() + "] "

                index = index + 1

            print(ligne)

        print("-" * 40)
        print("[XX] = siege reserve")
        print()

    #supplement selon le type de salle
    @abstractmethod
    def calculer_supplement(self):
        pass


    

    
    def __str__(self):
        return "Salle " + self.identifiant + " - " + str(self.nombre_places()) + " places"