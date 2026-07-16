

from salle import Salle


class SalleVIP(Salle):
    def __init__(self, identifiant, nb_rangees, sieges_par_rangee):
        super().__init__(identifiant, nb_rangees, sieges_par_rangee)



    #supplement vip
    def calculer_supplement(self):
        return 8


    #affichage
    def __str__(self):
        return "Salle VIP " + self.identifiant + " - supplement : " + str(self.calculer_supplement()) + " $"