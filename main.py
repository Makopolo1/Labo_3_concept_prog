
from multiplex import Multiplex

from salle_standard import SalleStandard
from salle_imax import SalleIMAX
from salle_vip import SalleVIP

from film import Film
from seance import Seance
from client import Client
from reservation import Reservation
from avis import Avis
from abonnement import Abonnement



#creation du multiplex
cinema = Multiplex("CineRoyal")


#creation des salles
salle1 = SalleStandard("S1", 3, 4)
salle2 = SalleIMAX("I1", 4, 5)
salle3 = SalleVIP("V1", 2, 3)

cinema.ajouter_salle(salle1)
cinema.ajouter_salle(salle2)
cinema.ajouter_salle(salle3)



#creation des films
film1 = Film("Avatar", 180, "Science-fiction", "13+", "Francais")
film2 = Film("Batman", 155, "Action", "16+", "Anglais")
film3 = Film("Le roi lion", 90, "Animation", "G", "Francais")

film1.ajouter_cineaste("James Cameron")
film2.ajouter_cineaste("Matt Reeves")
film3.ajouter_cineaste("Jon Favreau")



#creation des clients
client1 = Client("Nathan", "nathan@test.com", 20, True)
client2 = Client("Marc", "marc@test.com", 17, False)
client3 = Client("Cherry", "cherry@test.com", 10, True)

cinema.ajouter_client(client1)
cinema.ajouter_client(client2)
cinema.ajouter_client(client3)



#abonnement
abonnement1 = Abonnement(client1)

print("----- ABONNEMENT -----")
print(abonnement1)
print("Prix 20$ avec rabais :", abonnement1.appliquer_rabais(20))
print()

#creation des seances
seance1 = Seance(film1, salle2, "mardi", "19h00")
seance2 = Seance(film2, salle1, "vendredi", "21h00")
seance3 = Seance(film3, salle3, "samedi", "14h00")

cinema.ajouter_seance(seance1)
cinema.ajouter_seance(seance2)
cinema.ajouter_seance(seance3)



#afficher les infos du cinema
print("----- CINEMA -----")
print(cinema)
print("Nombre total de places :", cinema.nombre_places_total())
print()

cinema.afficher_salles()
print()

cinema.afficher_seances()
print()



#reservations
print("----- RESERVATIONS -----")

siege1 = salle2.trouver_siege("A1")
reservation1 = Reservation(client1, seance1, siege1, "regulier")
print(reservation1)


siege2 = salle1.trouver_siege("B2")
reservation2 = Reservation(client2, seance2, siege2, "etudiant")
print(reservation2)


siege3 = salle3.trouver_siege("A2")
reservation3 = Reservation(client3, seance3, siege3, "enfant")
print(reservation3)

print()

#afficher les plans avec les reservations
print("----- PLAN DES SALLES -----")

seance1.afficher_plan()
seance2.afficher_plan()
seance3.afficher_plan()


#ajouter des avis
print("----- AVIS -----")

avis1 = Avis(client1, 5, "Tres bon film")
avis2 = Avis(client2, 4, "Bon film aussi")

film1.ajouter_avis(avis1)
film1.ajouter_avis(avis2)

print(avis1)
print(avis2)
print("Note moyenne de", film1.titre, ":", film1.calculer_note_moyenne())
print()



#test erreur siege deja reserve
print("----- TEST ERREUR SIEGE -----")

try:
    reservation_erreur = Reservation(client2, seance1, siege1, "regulier")

except ValueError as erreur:
    print("Erreur :", erreur)

print()



#test erreur age
print("----- TEST ERREUR AGE -----")

try:
    siege4 = salle1.trouver_siege("A3")
    reservation_age = Reservation(client3, seance2, siege4, "enfant")

except ValueError as erreur:
    print("Erreur :", erreur)