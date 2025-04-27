import OutilsMathématique as OM  # Importer le module OutilsMathématique en utilisant l'alias OM
from PhaseInitiale import Transition, Automate  # Importer les classes Transition et Automate du module PhaseInitiale
import PhaseInitiale as PI  # Importer le module PhaseInitiale en utilisant l'alias PI
from graphviz import Digraph  # Importer le module graphviz pour la manipulation des graphes
from PIL import Image as PILImage  # Importer PIL pour ouvrir et afficher les images
import matplotlib.pyplot as plt  # Importer matplotlib.pyplot pour l'affichage des images

def est_deterministe(automate):
    # Vérifie si l'automate est déterministe
    transitions_verifiees = {}

    for transition in automate.listTransitions:
        etat_source = transition.etatSource.get_id()
        symbole = transition.alphabet.get_value()
        # Si une transition avec le même état source et symbole existe déjà, l'automate n'est pas déterministe
        if (etat_source, symbole) in transitions_verifiees:
            return False
        transitions_verifiees[(etat_source, symbole)] = transition.etatDestination

    return True

def determinist(automate):
    # Déterminise l'automate donné
    if est_deterministe(automate):
        print("L'automate est déjà déterministe.")
        return automate

    A = Automate()  # Créer un nouvel automate

    queue = []  # Utiliser une file d'attente pour les nouveaux états à traiter
    etats_traite = set()  # Ensemble des états déjà traités
    state_mapping = {}  # Mapping de l'ensemble des états vers les nouveaux états déterministes
    c = 0  # Compteur pour les nouveaux états

    def get_or_create_state(subset):
        nonlocal c
        subset_key = tuple(sorted(subset, key=lambda x: x.get_id()))  # Clé unique pour le sous-ensemble
        if subset_key not in state_mapping:
            my_string = ''.join([state.get_label() for state in subset])  # Créer une étiquette pour le nouvel état
            state_type = 'intermediaire'
            if any(state in automate.listFinaux for state in subset):
                state_type = 'final'  # Déterminer le type de l'état (final)
            if set(subset) == set(automate.listInitiaux):
                state_type = 'initial'  # Déterminer le type de l'état (initial)
            new_state = PI.Etat(c, my_string, state_type)  # Créer le nouvel état
            state_mapping[subset_key] = new_state
            queue.append(subset)
            A.ajouter_etat(new_state)
            if state_type == 'final':
                A.ajouter_etat_final(new_state)
            if state_type == 'initial':
                A.ajouter_etat_initial(new_state)
            c += 1
        return state_mapping[subset_key]

    S = OM.find_subsets(automate.listEtats)  # Trouver tous les sous-ensembles des états
    for i in S:
        get_or_create_state(i)  # Créer ou récupérer les nouveaux états pour chaque sous-ensemble

    A.listAlphabets = automate.listAlphabets  # Copier les alphabets de l'automate original

    while queue:
        current_subset = queue.pop(0)  # Extraire le premier sous-ensemble de la file d'attente
        current_state = get_or_create_state(current_subset)  # Créer ou récupérer l'état courant
        etats_traite.add(tuple(sorted(current_subset, key=lambda x: x.get_id())))

        for alphabet in automate.listAlphabets:
            next_subset = set()
            for state in current_subset:
                next_subset.update(automate.beta(state, alphabet))  # Obtenir le prochain sous-ensemble d'états
            if next_subset:
                next_state = get_or_create_state(next_subset)  # Créer ou récupérer le prochain état
                new_transition = Transition(len(A.listTransitions), current_state, next_state,
                                            alphabet)  # Créer une nouvelle transition
                A.ajouter_transition(new_transition)  # Ajouter la transition à l'automate
    return A  # Retourner le nouvel automate déterministe

def complet(nfa):
    # Complète un automate non complet
    etat_puit = PI.Etat(len(nfa.listEtats), 'p', 'intermediaire')  # Créer un état puits
    all_transitions_present = True  # Vérifier si toutes les transitions nécessaires sont présentes

    for state in nfa.listEtats:
        for symbol in nfa.listAlphabets:
            if not any(transition.alphabet == symbol and transition.etatSource == state for transition in
                       nfa.listTransitions):
                all_transitions_present = False
                break
        if not all_transitions_present:
            break

    if all_transitions_present:
        print("L'automate est déjà complet.")
        return nfa  # Retourner l'automate original s'il est déjà complet

    nfa.ajouter_etat(etat_puit)  # Ajouter l'état puits à l'automate
    print("Ajout de l'état puits :", etat_puit.labelEtat)

    for state in nfa.listEtats:
        print("Vérification de l'état :", state.labelEtat)
        for symbol in nfa.listAlphabets:
            if not any(transition.alphabet == symbol and transition.etatSource == state for transition in
                       nfa.listTransitions):
                print(
                    f"Transition manquante de {state.labelEtat} pour le symbole '{symbol}'. Ajout de la transition vers l'état puits.")
                new_transition = PI.Transition(len(nfa.listTransitions) + 1, state, etat_puit,
                                               symbol)  # Créer une nouvelle transition vers l'état puits
                nfa.ajouter_transition(new_transition)  # Ajouter la transition à l'automate
                print(f"Ajout de la transition de {state.labelEtat} à {etat_puit.labelEtat} avec le symbole '{symbol}'")

    return nfa  # Retourner l'automate complété

def minimiser(automate):
    # Minimise l'automate donné
    a = automate.Unreachable()  # Étape 1: Éliminer les états inaccessibles

    A = Automate()  # Créer un nouvel automate minimisé
    etats_terminaux = [etat for etat in automate.listFinaux if etat not in a]  # Obtenir les états terminaux accessibles
    etats_non_terminaux = [etat for etat in automate.listEtats if
                           etat not in etats_terminaux and etat not in a]  # Obtenir les états non terminaux accessibles
    s = [etats_terminaux, etats_non_terminaux]

    while True:
        new_partition = []
        for group in s:
            temp_group = group.copy()
            while temp_group:
                i = temp_group.pop(0)
                makeset = [i]
                to_remove = []
                for n in temp_group:
                    if automate.equivaux_next(i, n, s) and i != n:
                        to_remove.append(n)
                        makeset.append(n)
                for item in to_remove:
                    temp_group.remove(item)
                new_partition.append(makeset)
        if s == new_partition:
            break
        s = new_partition

    state_mapping = {}
    for idx, subset in enumerate(s):
        label = ''.join(sorted([etat.get_label() for etat in subset]))  # Créer une étiquette pour le nouvel état
        etat_type = 'intermediaire'
        if OM.Intersection(subset, automate.listFinaux):
            etat_type = 'final'  # Déterminer le type de l'état (final)
        if OM.est_incluse(subset, automate.listInitiaux):
            etat_type = 'initial'  # Déterminer le type de l'état (initial)
        new_state = PI.Etat(str(idx), label, etat_type)  # Créer le nouvel état
        sorted_subset = sorted(subset, key=lambda x: int(x.get_id()))
        state_mapping[tuple(sorted_subset)] = new_state
        A.ajouter_etat(new_state)
        if etat_type == 'final':
            A.ajouter_etat_final(new_state)
        if etat_type == 'initial':
            A.ajouter_etat_initial(new_state)

    A.listAlphabets = automate.listAlphabets  # Copier les alphabets de l'automate original

    for alphabet in automate.listAlphabets:
        for from_group in s:
            from_state = state_mapping[tuple(sorted(from_group, key=lambda x: x.get_id()))]
            for to_group in s:
                if automate.isReachable(from_group, to_group, alphabet):
                    to_state = state_mapping[tuple(sorted(to_group, key=lambda x: x.get_id()))]
                    new_transition = Transition(len(A.listTransitions), from_state, to_state,
                                                alphabet)  # Créer une nouvelle transition
                    A.ajouter_transition(new_transition)  # Ajouter la transition à l'automate

    return A  # Retourner l'automate minimisé


def afficher_automate(automate):
    # Créer un nouveau graphe orienté
    dot = Digraph(strict=False)

    # Ajouter des nœuds pour les états
    for etat in automate.listEtats:
        if isinstance(etat, PI.Etat):
            etat_id = str(etat.get_id())
            etat_label = etat.get_label()
            etat_type = etat.get_type()

            # Définir la forme du nœud en fonction du type d'état
            if etat_type == 'initial':
                shape = 'ellipse'
            elif etat_type == 'final':
                shape = 'doublecircle'
            elif etat_type == 'initialFinal':
                shape = 'doublecircle'
            else:
                shape = 'circle'

            dot.node(etat_id, label=etat_label, shape=shape)
        else:
            etat_id = ','.join([str(e.get_id()) if isinstance(e, PI.Etat) else str(e) for e in etat])
            dot.node(etat_id, label=etat_id, shape='circle')

    # Ajouter des transitions
    for transition in automate.listTransitions:
        source_id = str(transition.etatSource.get_id()) if isinstance(transition.etatSource, PI.Etat) else ','.join(
            [str(e.get_id()) if isinstance(e, PI.Etat) else str(e) for e in transition.etatSource])
        destination_id = str(transition.etatDestination.get_id()) if isinstance(transition.etatDestination, PI.Etat) else ','.join(
            [str(e.get_id()) if isinstance(e, PI.Etat) else str(e) for e in transition.etatDestination])
        label = transition.alphabet.get_value()

        dot.edge(source_id, destination_id, label=label)

    # Ajouter des flèches pour les états initiaux
    for etat in automate.listEtats:
        if isinstance(etat, PI.Etat) and etat.get_type() in ['initial', 'initialFinal']:
            etat_id = str(etat.get_id())
            # Ajouter une flèche pointant vers l'état initial
            dot.edge('start', etat_id, label='')

    # Ajouter un nœud invisible pour les flèches des états initiaux
    dot.node('start', shape='point', width='0')

    # Rendre le graphe et l'enregistrer dans un fichier
    output_path = r'C:\Users\PRO GAMER\Desktop\PI-24\automate'
    dot.render(output_path, format='png', cleanup=False)

    # Ouvrir et afficher l'image
    img = PILImage.open(f'{output_path}.png')
    plt.imshow(img)
    plt.axis('off')  # Désactiver les axes pour une meilleure visualisation
    plt.show()