# CinéRoyal - Laboratoire 2

Système de gestion pour un cinéma multiplex : films, salles, séances, clients et réservations.

## Comment lancer le programme

python main.py
Le fichier main.py crée un multiplex, des salles, des films, des clients et des séances, puis fait
plusieurs réservations, des avis et des tests d'erreurs pour montrer que le système fonctionne au
complet.

## Classes du projet

- Multiplex : le cinéma au complet, contient les salles, les séances et les clients.
- Salle (abstraite) : classe de base pour toutes les salles.
- SalleStandard / SalleIMAX / SalleVIP : les 3 types de salles, chacune a son propre supplément.
- Siege : un siège précis (rangée, numéro) dans une salle.
- Film : titre, durée, genre, classification, langue, cinéastes et avis.
- Seance : associe un film, une salle, une date et une heure.
- Client : nom, courriel, âge, carte de fidélité, ses réservations.
- Reservation : lie un client, une séance et un siège, calcule le prix.
- Avis : note et commentaire d'un client sur un film.
- Abonnement : abonnement annuel avec un rabais.

## Nos choix de conception

1. On a fait Salle en classe abstraite parce que chaque type de salle (standard, IMAX, VIP)
   calcule son supplément différemment. Avec ABC, on est obligé de définir calculer_supplement()
   dans chaque sous-classe, sinon le programme ne fonctionne pas.

2. La salle crée elle-même ses sièges dans son constructeur (generer_sieges()). On a trouvé que
   ça ne faisait pas de sens qu'un siège existe sans salle, donc on a fait de la composition
   plutôt que de l'agrégation.

3. On a mis des property/setter sur presque tous les attributs pour valider les données (l'âge ne
   peut pas être négatif, le rabais doit être entre 0 et 1, etc). Ça évite d'avoir des valeurs
   bizarres dans le programme.

4. Reservation vérifie l'âge du client et réserve le siège directement dans le constructeur. Si ça
   ne marche pas, ça lève une erreur tout de suite au lieu de créer une réservation invalide.

5. On a fait un fichier par classe pour pouvoir travailler chacun de notre côté sans se marcher sur
   les pieds sur le même fichier.

## Limites connues et améliorations futures

- On ne vérifie pas si une salle a 2 séances en même temps.

- L'abonnement existe mais n'est pas encore branché avec Reservation pour appliquer le rabais
  automatiquement.

## Répartition des tâches

Voir le fichier equipe.txt.

## Déclaration d'utilisation de l'IA

Pour la méthode afficher_plan() dans salle.py, on s'est retrouvé bloqué sur comment transformer
notre liste de sièges en un affichage de grille (rangées et colonnes), tout en montrant quels
sièges étaient déjà réservés. On a utilisé une IA pour nous aider à comprendre comment faire
cette partie (comment parcourir la grille avec un index et comment comparer avec les sièges
réservés).
