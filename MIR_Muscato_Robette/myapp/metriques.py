# myapp/metriques.py

def average_precision(rappels, precisions):
    somme = sum(precisions)
    print("Somme des précisions:", somme)
    if somme == 0:
        return 0.0
    else:
        ap = somme / len(precisions)
    return ap

def mean_average_precision(liste_AP):
    if not liste_AP:
        return 0.0
    return sum(liste_AP) / len(liste_AP)

def r_precision(liste_pertinentes_recuperees, R):
    top_R = liste_pertinentes_recuperees[:R]
    nb_pertinents_dans_top_R = sum(top_R)
    return nb_pertinents_dans_top_R / R if R != 0 else 0.0

def calculer_metriques(rappels, precisions, pertinents_recup, R):
    ap = average_precision(rappels, precisions)
    map_value = mean_average_precision([ap])
    rp = r_precision(pertinents_recup, R)
    return {
        "ap": round(ap, 4),
        "map": round(map_value, 4),
        "rp": round(rp, 4)
    }

