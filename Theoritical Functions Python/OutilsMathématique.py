import PhaseInitiale as PI

def Union(L1, L2):
    # Retourne l'union de deux listes en éliminant les doublons
    return list(set(L1) | set(L2))

def Intersection(L1, L2):
    # Transforme les éléments de L1 et L2 en tuples contenant les identifiants d'état (si c'est un objet Etat)
    L1 = [tuple(e.get_id() if isinstance(e, PI.Etat) else e for e in sublist) if isinstance(sublist, list) else sublist for sublist in L1]
    L2 = [tuple(e.get_id() if isinstance(e, PI.Etat) else e for e in sublist) if isinstance(sublist, list) else sublist for sublist in L2]
    # Retourne l'intersection de L1 et L2
    return list(set(L1) & set(L2))

def find_subsets(liste):
    # Génère tous les sous-ensembles d'une liste donnée
    subsets = [[]]
    for element in liste:
        subsets += [subset + [element] for subset in subsets]
    return subsets

def find(a, b, S):
    # Vérifie si les éléments 'a' et 'b' se trouvent ensemble dans un quelconque sous-ensemble de S
    for j in S:
        if (a in j) and (b in j):
            return True
    return False

def est_incluse(liste1, liste2):
    # Vérifie si tous les éléments de liste2 sont inclus dans liste1
    ensemble1 = set(tuple(x) if isinstance(x, list) else x for x in liste1)
    ensemble2 = set(tuple(x) if isinstance(x, list) else x for x in liste2)
    return ensemble2.issubset(ensemble1)
