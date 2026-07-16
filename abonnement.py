#classe abonnement

class Abonnement:
    def __init__(self, client, rabais=0.10, actif=True):
        self.client = client
        self.rabais = rabais
        self.actif = actif

    #client de l'abonnement
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        if client is None:
            raise ValueError("client invalide")

        self._client = client

    #rabais de l'abonnement
    @property
    def rabais(self):
        return self._rabais

    @rabais.setter
    def rabais(self, rabais):
        if rabais < 0 or rabais > 1:
            raise ValueError("rabais invalide")

        self._rabais = rabais



    #abonnement actif ou non
    @property
    def actif(self):
        return self._actif

    @actif.setter
    def actif(self, actif):
        self._actif = actif


    #activer abonnement
    def activer(self):
        self.actif = True
    #desactiver abonnement
    def desactiver(self):
        self.actif = False


    #appliquer le rabais sur un prix
    def appliquer_rabais(self, prix):
        if self.actif == False:
            return prix

        montant_rabais = prix * self.rabais
        prix_final = prix - montant_rabais

        return prix_final

    #affichage
    def __str__(self):
        if self.actif:
            etat = "actif"
        else:
            etat = "inactif"

        return "Abonnement de " + str(self.client) + " - " + etat