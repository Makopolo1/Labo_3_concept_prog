from salle import Salle


class SalleVIP(Salle):
    def calculer_supplement(self):
        return 8

    @classmethod
    def from_dict(cls, donnees):
        return cls(
            donnees["identifiant"],
            donnees["nb_rangees"],
            donnees["sieges_par_rangee"]
        )

    def __str__(self):
        return "Salle VIP " + self.identifiant
