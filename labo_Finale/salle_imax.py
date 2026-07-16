from salle import Salle


class SalleIMAX(Salle):
    def calculer_supplement(self):
        return 4

    @classmethod
    def from_dict(cls, donnees):
        return cls(
            donnees["identifiant"],
            donnees["nb_rangees"],
            donnees["sieges_par_rangee"]
        )

    def __str__(self):
        return "Salle IMAX " + self.identifiant
