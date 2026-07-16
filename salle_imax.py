
from salle import Salle


class SalleIMAX(Salle):
    def __init__(self, identifiant, nb_rangees, sieges_par_rangee):
        super().__init__(identifiant, nb_rangees, sieges_par_rangee)


    #supplement imax
    def calculer_supplement(self):
        return 4




    def __str__(self):
        return "Salle IMAX " + self.identifiant + " - supplement : " + str(self.calculer_supplement()) + " $"