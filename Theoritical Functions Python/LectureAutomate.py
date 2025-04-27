import PhaseInitiale as PI

def lireAutomate(alphabets, etats, etats_initiaux, etats_finaux, transitions):
    automate = PI.Automate()
    if all(isinstance(x, list) for x in [alphabets, etats, etats_initiaux, etats_finaux, transitions]):
        automate.listAlphabets = alphabets
        automate.listEtats = etats
        automate.listInitiaux = etats_initiaux
        automate.listFinaux = etats_finaux
        automate.listTransitions = transitions
        return automate
    else:
        raise ValueError("All inputs must be lists.")
