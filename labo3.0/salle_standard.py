

from salle import Salle


class SalleStandard(Salle):
    def __init__(self, identifiant, nb_rangees, sieges_par_rangee):
        super().__init__(identifiant, nb_rangees, sieges_par_rangee)



    #supplement de la salle standard
    def calculer_supplement(self):
        return 0


    
    def __str__(self):
        return "Salle standard " + self.identifiant + " - supplement : " + str(self.calculer_supplement()) + " $"