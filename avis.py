#classe avis

class Avis:
    def __init__(self, client, note, commentaire):
        self.client = client
        self.note = note
        self.commentaire = commentaire

 #client qui donne l'avis
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        if client is None:
            raise ValueError("client invalide")
        self._client = client
#note entre 1 et 5
    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note):
        if note < 1 or note > 5:
            raise ValueError("la note doit etre entre 1 et 5")

        self._note = note



    #commentaire du client
    @property
    def commentaire(self):
        return self._commentaire

    @commentaire.setter
    def commentaire(self, commentaire):
        if commentaire.strip() == "":
            raise ValueError("le commentaire ne peut pas etre vide")

        self._commentaire = commentaire.strip()
#affichage de l'avis
    def __str__(self):
        return "Avis de " + str(self.client) + " : " + str(self.note) + "/5 - " + self.commentaire