
class Reservation:
    def __init__(self, client, seance, siege, type_billet):
        self.client = client
        self.seance = seance
        self.siege = siege
        self.type_billet = type_billet

        self.verifier_age()
        self.seance.reserver_siege(self.siege)

        self.prix_final = self.calculer_prix()
        self.client.ajouter_reservation(self)



    #client
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        if client is None:
            raise ValueError("client invalide")
        self._client = client


    #seance
    @property
    def seance(self):
        return self._seance

    @seance.setter
    def seance(self, seance):
        if seance is None:
            raise ValueError("seance invalide")

        self._seance = seance

    #siege
    @property
    def siege(self):
        return self._siege

    @siege.setter
    def siege(self, siege):
        if siege is None:
            raise ValueError("siege invalide")

        self._siege = siege


    #type de billet
    @property
    def type_billet(self):
        return self._type_billet

    @type_billet.setter
    def type_billet(self, type_billet):
        types = ["regulier", "etudiant", "aine", "enfant"]

        if type_billet not in types:
            raise ValueError("type de billet invalide")

        self._type_billet = type_billet

    #prix final
    @property
    def prix_final(self):
        return self._prix_final

    @prix_final.setter
    def prix_final(self, prix_final):
        if prix_final < 0:
            raise ValueError("prix invalide")

        self._prix_final = prix_final


    #verifier l'age selon la classification
    def verifier_age(self):
        classification = self.seance.film.classification

        if classification == "16+" and self.client.age < 12:
            raise ValueError("le client est trop jeune pour ce film")

        if classification == "18+" and self.client.age < 18:
            raise ValueError("le client est trop jeune pour ce film")



    #prix de base selon le billet
    def prix_de_base(self):
        if self.type_billet == "regulier":
            return 12

        if self.type_billet == "etudiant":
            return 10

        if self.type_billet == "aine":
            return 9

        if self.type_billet == "enfant":
            return 8


    #calculer le prix total
    def calculer_prix(self):
        date = self.seance.date.lower()

        if "mardi" in date:
            prix = 6
        else:
            prix = self.prix_de_base()

        prix = prix + self.seance.salle.calculer_supplement()

        if self.client.carte_fidelite:
            prix = prix - 1

        return prix



    

    
    def __str__(self):
        texte = "Reservation : "
        texte = texte + str(self.client) + " - "
        texte = texte + self.seance.film.titre + " - "
        texte = texte + self.siege.code() + " - "
        texte = texte + str(self.prix_final) + " $"

        return texte