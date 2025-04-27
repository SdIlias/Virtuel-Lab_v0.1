import PhaseInitiale as PI
import Fonctionnalitees as F

A = PI.Etat(0, 'A', 'initial')
B = PI.Etat(1, 'B', 'inter')
C = PI.Etat(2, 'C', 'final')


a = PI.Alphabet('0', '0')
b = PI.Alphabet('1', '1')

trans1 = PI.Transition(1, A, A, a)
trans2 = PI.Transition(2, A, A, b)
trans3 = PI.Transition(3, A, B, a)
trans4 = PI.Transition(4, B, C, b)


nfa = PI.Automate()
nfa.ajouter_etat(A)
nfa.ajouter_etat(B)
nfa.ajouter_etat(C)


nfa.ajouter_alphabet(a)
nfa.ajouter_alphabet(b)

nfa.ajouter_transition(trans1)
nfa.ajouter_transition(trans2)
nfa.ajouter_transition(trans3)
nfa.ajouter_transition(trans4)


nfa.listInitiaux = [A]
nfa.listFinaux = [C]

dfa = F.determinist(nfa)
print("number of DFA's states: ", len(dfa.listEtats))
print("DFA States:", dfa.listEtats)
print("number of DFA's transitions: ", len(dfa.listTransitions))
print("DFA Transitions:", dfa.listTransitions)
print("DFA final states:", dfa.listFinaux)
print("DFA initial states:", dfa.listInitiaux)

complete_automate = F.complet(nfa)

minimizer = F.minimiser(nfa)
print("Original States:", nfa.listEtats)
print("Minimized States:", minimizer.listEtats)
print("Minimized Transitions:", minimizer.listTransitions)
