
class Client:
    def __init__(self, nom, courriel, age, carte_fidelite=False):
        self.nom = nom
        self.courriel = courriel
        self.age = age
        self.carte_fidelite = carte_fidelite

        self._reservations = []

 #nom du client
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if nom.strip() == "":
            raise ValueError("nom du client vide")

        self._nom = nom.strip()
#courriel du client
    @property
    def courriel(self):
        return self._courriel

    @courriel.setter
    def courriel(self, courriel):
        if courriel.strip() == "":
            raise ValueError("courriel vide")

        if "@" not in courriel:
            raise ValueError("courriel invalide")

        self._courriel = courriel.strip()
 #age du client
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if age <= 0:
            raise ValueError("age invalide")

        self._age = age
 #carte fidelite
    @property
    def carte_fidelite(self):
        return self._carte_fidelite

    @carte_fidelite.setter
    def carte_fidelite(self, carte_fidelite):
        self._carte_fidelite = carte_fidelite



    #liste des reservations
    @property
    def reservations(self):
        return self._reservations

    def ajouter_reservation(self, reservation):
        self._reservations.append(reservation)



    #dire si le client est mineur
    def est_mineur(self):
        return self.age < 18

    def __str__(self):
        return self.nom + " (" + str(self.age) + " ans)"
    

#testdemergeMoushi