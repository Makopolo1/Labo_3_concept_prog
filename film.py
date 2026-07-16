
class Film:
    def __init__(self, titre, duree, genre, classification, langue):
        self.titre = titre
        self.duree = duree
        self.genre = genre
        self.classification = classification
        self.langue = langue

        self._cineastes = []
        self._avis = []

    @property
    def titre(self):
        return self._titre

    @titre.setter
    def titre(self, titre):
        if titre.strip() == "":
            raise ValueError("titre du film vide")
        self._titre = titre.strip()


    #duree en minutes
    @property
    def duree(self):
        return self._duree

    @duree.setter
    def duree(self, duree):
        if duree <= 0:
            raise ValueError("duree du film invalide")

        self._duree = duree



    #genre du film
    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        if genre.strip() == "":
            raise ValueError("genre vide")
        self._genre = genre.strip()


    #classification du film
    @property
    def classification(self):
        return self._classification

    @classification.setter
    def classification(self, classification):
        classifications = ["G", "13+", "16+", "18+"]

        if classification not in classifications:
            raise ValueError("classification invalide")

        self._classification = classification



    #langue du film
    @property
    def langue(self):
        return self._langue

    @langue.setter
    def langue(self, langue):
        if langue.strip() == "":
            raise ValueError("langue vide")

        self._langue = langue.strip()


    #liste des cineastes
    @property
    def cineastes(self):
        return self._cineastes


    #liste des avis
    @property
    def avis(self):
        return self._avis

    #ajouter un cineaste
    def ajouter_cineaste(self, nom):
        if nom.strip() == "":
            raise ValueError("nom du cineaste vide")

        self._cineastes.append(nom.strip())


    #ajouter un avis au film
    def ajouter_avis(self, avis):
        self._avis.append(avis)



    #calculer la note moyenne
    def calculer_note_moyenne(self):
        if len(self.avis) == 0:
            return 0

        total = 0

        for avis in self.avis:
            total = total + avis.note

        return total / len(self.avis)



    def __str__(self):
        return self.titre + " - " + str(self.duree) + " min - " + self.classification