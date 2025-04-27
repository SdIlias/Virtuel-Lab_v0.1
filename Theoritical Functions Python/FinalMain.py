import PhaseInitiale as PI
import Fonctionnalitees as F


automate = PI.Automate()

while True:
    action = input(
        "Choose action: Add State (s), Add Transition (t), Show Automate (v), Show Deterministic Automate (d), Show Complete Automate (c), Show Minimized Automate (m), Delete State (ds), Delete Alphabet (da), Delete Transition (dt), Exit (e): ")
    if action.lower() == 'e':
        break
    elif action.lower() == 's':
        id = input("Enter state ID: ")
        label = input("Enter state label: ")
        type_etat = input("Enter state type (initial/final/intermediate/initialFinal): ")
        new_state = PI.Etat(id, label, type_etat)
        if type_etat == 'initial':
            automate.listInitiaux.append(new_state)
        elif type_etat == 'final':
            automate.listFinaux.append(new_state)
        elif type_etat == 'initialFinal':
            automate.listInitiaux.append(new_state)
            automate.listFinaux.append(new_state)
        automate.ajouter_etat(new_state)
    elif action.lower() == 't':
        source_id = input("Enter source state ID: ")
        dest_id = input("Enter destination state ID: ")
        symbol = input("Enter transition symbol: ")
        source = next((s for s in automate.listEtats if s.get_id() == source_id), None)
        destination = next((s for s in automate.listEtats if s.get_id() == dest_id), None)
        alphabet = next((a for a in automate.listAlphabets if a.get_value() == symbol), None)
        if not alphabet:
            alphabet = PI.Alphabet(symbol, symbol)
            automate.ajouter_alphabet(alphabet)
        transition = PI.Transition(len(automate.listTransitions) + 1, source, destination, alphabet)
        automate.ajouter_transition(transition)
    elif action.lower() == 'v':
        try:
            F.afficher_automate(automate)
        except Exception as e:
            print(f"An error has occurred while displaying the automate: {e}")
    elif action.lower() == 'd':
        try:
            dfa = F.determinist(automate)
            F.afficher_automate(dfa)
        except Exception as e:
            print(f"An error has occurred while displaying the deterministic automate: {e}")
    elif action.lower() == 'c':
        try:
            dfa = F.determinist(automate)
            complete_automate = F.complet(dfa)
            F.afficher_automate(complete_automate)
        except Exception as e:
            print(f"An error has occurred while displaying the complete automate: {e}")
    elif action.lower() == 'm':
        try:
            dfa = F.determinist(automate)
            complete_automate = F.complet(dfa)
            minimized_automate = F.minimiser(complete_automate)
            F.afficher_automate(minimized_automate)
        except Exception as e:
            print(f"An error has occurred while displaying the minimized automate: {e}")
    elif action.lower() == 'ds':
        state_id = input("Enter the ID of the state to delete: ")
        state = next((s for s in automate.listEtats if s.get_id() == state_id), None)
        if state:
            automate.supprimer_etat(state)
        else:
            print("State not found.")
    elif action.lower() == 'da':
        alphabet_value = input("Enter the value of the alphabet to delete: ")
        alphabet = next((a for a in automate.listAlphabets if a.get_value() == alphabet_value), None)
        if alphabet:
            automate.supprimer_alphabet(alphabet)
        else:
            print("Alphabet not found.")
    elif action.lower() == 'dt':
        source_id = input("Enter the source state ID of the transition to delete: ")
        dest_id = input("Enter the destination state ID of the transition to delete: ")
        symbol = input("Enter the symbol of the transition to delete: ")
        transition = next((t for t in automate.listTransitions if
                           t.etatSource.get_id() == source_id and t.etatDestination.get_id() == dest_id and t.alphabet.get_value() == symbol),
                          None)
        if transition:
            automate.supprimer_transition(transition)
        else:
            print("Transition not found.")
    else:
        print("Invalid action. Please choose again.")
