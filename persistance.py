import json
import os

from labo_Finale.multiplex import Multiplex
from labo_Finale.salle_standard import SalleStandard
from labo_Finale.salle_imax import SalleIMAX
from labo_Finale.salle_vip import SalleVIP


DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))
DOSSIER_DATA = os.path.join(DOSSIER_PROJET, "data")
CHEMIN_FICHIER = os.path.join(DOSSIER_DATA, "sauvegarde.json")


def creer_modele_vide():
    cinema = Multiplex("CineRoyal")

    # Les salles de base du Lab 2
    cinema.ajouter_salle(SalleStandard("S1", 3, 4))
    cinema.ajouter_salle(SalleIMAX("I1", 4, 5))
    cinema.ajouter_salle(SalleVIP("V1", 2, 3))

    return cinema


def sauvegarder(modele):
    os.makedirs(DOSSIER_DATA, exist_ok=True)

    with open(CHEMIN_FICHIER, "w", encoding="utf-8") as fichier:
        json.dump(
            modele.to_dict(),
            fichier,
            indent=2,
            ensure_ascii=False
        )


def charger():
    if not os.path.exists(CHEMIN_FICHIER):
        return creer_modele_vide()

    try:
        with open(CHEMIN_FICHIER, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)

        return Multiplex.from_dict(donnees)

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as erreur:
        raise ValueError("le fichier de sauvegarde est invalide") from erreur
