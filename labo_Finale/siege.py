
class Siege:

    def __init__(self, rangee, numero):
        self.rangee = rangee
        self.numero = numero

    #rangee du siege
    @property
    def rangee(self):
        return self._rangee

    @rangee.setter
    def rangee(self, rangee):
        if rangee.strip() == "":
            raise ValueError("La rangee ne peut pas etre vide")
        self._rangee = rangee.strip().upper()
#numero du siege
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        if numero <= 0:
            raise ValueError("Le numero doit etre plus grand que 0")
        self._numero = numero


    #retourne le code du siege
    def code(self):
        return self.rangee + str(self.numero)

    
    def __str__(self):
        return self.code()


    #verifie si deux sieges sont pareils
    def est_pareil(self, autre):
        return self.rangee == autre.rangee and self.numero == autre.numero
