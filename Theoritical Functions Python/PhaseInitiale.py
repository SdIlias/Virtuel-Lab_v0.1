import OutilsMathématique  # Importer le module OutilsMathématique qui contient des outils mathématiques spécifiques

class Etat:
    def __init__(self, idEtat, labelEtat, typeEtat):
        self.idEtat = idEtat  # Identifiant de l'état
        self.labelEtat = labelEtat  # Étiquette de l'état
        self.typeEtat = typeEtat  # Type de l'état (par exemple initial, final)

    def get_id(self):
        return self.idEtat  # Retourne l'identifiant de l'état

    def set_label(self, labelEtat):
        self.labelEtat = labelEtat  # Définit une nouvelle étiquette pour l'état

    def get_label(self):
        return self.labelEtat  # Retourne l'étiquette de l'état

    def set_type(self, typeEtat):
        self.typeEtat = typeEtat  # Définit un nouveau type pour l'état

    def get_type(self):
        return self.typeEtat  # Retourne le type de l'état

    def __repr__(self):
        return "({})".format(self.labelEtat)  # Représentation de l'état sous forme de chaîne de caractères


class Alphabet:
    def __init__(self, idAlphabet, valAlphabet):
        self.idAlphabet = idAlphabet  # Identifiant de l'alphabet
        self.valAlphabet = valAlphabet  # Valeur de l'alphabet

    def get_id(self):
        return self.idAlphabet  # Retourne l'identifiant de l'alphabet

    def set_value(self, valAlphabet):
        self.valAlphabet = valAlphabet  # Définit une nouvelle valeur pour l'alphabet

    def get_value(self):
        return self.valAlphabet  # Retourne la valeur de l'alphabet

    def __repr__(self):
        return "{}".format(self.valAlphabet)  # Représentation de l'alphabet sous forme de chaîne de caractères


class Transition:
    def __init__(self, idTransition, etatSource, etatDestination, alphabet):
        self.idTransition = idTransition  # Identifiant de la transition
        self.etatSource = etatSource  # État source de la transition
        self.etatDestination = etatDestination  # État de destination de la transition
        self.alphabet = alphabet  # Alphabet associé à la transition

    def get_id(self):
        return self.idTransition  # Retourne l'identifiant de la transition

    def set_source(self, etatSource):
        self.etatSource = etatSource  # Définit un nouvel état source pour la transition

    def get_source(self):
        return self.etatSource  # Retourne l'état source de la transition

    def set_destination(self, etatDestination):
        self.etatDestination = etatDestination  # Définit un nouvel état de destination pour la transition

    def get_destination(self):
        return self.etatDestination  # Retourne l'état de destination de la transition

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet  # Définit un nouvel alphabet pour la transition

    def get_alphabet(self):
        return self.alphabet  # Retourne l'alphabet de la transition

    def __repr__(self):
        return "({},{},{})".format(self.etatSource, self.alphabet, self.etatDestination)  # Représentation de la transition sous forme de chaîne de caractères


class Automate:
    def __init__(self):
        self.listAlphabets = []  # Liste des alphabets
        self.listEtats = []  # Liste des états
        self.listInitiaux = []  # Liste des états initiaux
        self.listFinaux = []  # Liste des états finaux
        self.listTransitions = []  # Liste des transitions

    def ajouter_etat(self, etat):
        if isinstance(etat, Etat) and etat not in self.listEtats:
            self.listEtats.append(etat)  # Ajoute un état à la liste des états s'il est du type Etat et n'y figure pas déjà

    def ajouter_etat_initial(self, etat):
        if etat in self.listEtats:
            self.listInitiaux.append(etat)  # Ajoute un état à la liste des états initiaux s'il figure déjà dans la liste des états

    def ajouter_etat_final(self, etat):
        if etat in self.listEtats:
            self.listFinaux.append(etat)  # Ajoute un état à la liste des états finaux s'il figure déjà dans la liste des états

    def supprimer_etat(self, etat):
        if etat in self.listEtats:
            self.listTransitions = [t for t in self.listTransitions if
                                    t.etatSource != etat and t.etatDestination != etat]  # Supprime toutes les transitions impliquant l'état
            self.listEtats.remove(etat)  # Supprime l'état de la liste des états
            if etat in self.listInitiaux:
                self.listInitiaux.remove(etat)  # Supprime l'état de la liste des états initiaux
            if etat in self.listFinaux:
                self.listFinaux.remove(etat)  # Supprime l'état de la liste des états finaux

    def modifier_etat(self, ancien_etat, nouveau_etat):
        if ancien_etat in self.listEtats:  # Vérifie si l'ancien état existe avant de le modifier
            index = self.listEtats.index(ancien_etat)
            if isinstance(nouveau_etat, Etat) and nouveau_etat not in self.listEtats:
                self.listEtats[index] = nouveau_etat  # Remplace l'ancien état par le nouveau dans la liste des états

    def ajouter_alphabet(self, alphabet):
        if isinstance(alphabet, Alphabet) and alphabet not in self.listAlphabets:
            self.listAlphabets.append(alphabet)  # Ajoute un alphabet à la liste des alphabets s'il est du type Alphabet et n'y figure pas déjà

    def supprimer_alphabet(self, alphabet):
        if alphabet in self.listAlphabets:
            self.listAlphabets.remove(alphabet)  # Supprime l'alphabet de la liste des alphabets
            self.listTransitions = [t for t in self.listTransitions if t.alphabet != alphabet]  # Supprime toutes les transitions associées à cet alphabet

    def modifier_alphabet(self, ancien_alphabet, nouveau_alphabet):
        if ancien_alphabet in self.listAlphabets:
            index = self.listAlphabets.index(ancien_alphabet)
            self.listAlphabets[index] = nouveau_alphabet  # Remplace l'ancien alphabet par le nouveau dans la liste des alphabets

    def ajouter_transition(self, transition):
        if isinstance(transition, Transition) and transition not in self.listTransitions:
            if transition.etatSource in self.listEtats and transition.etatDestination in self.listEtats and transition.alphabet in self.listAlphabets:
                self.listTransitions.append(transition)  # Ajoute une transition à la liste des transitions si elle est du type Transition et que ses éléments source, destination et alphabet sont valides

    def supprimer_transition(self, transition):
        if transition in self.listTransitions:
            self.listTransitions.remove(transition)  # Supprime la transition de la liste des transitions

    def modifier_transition(self, ancienne_transition, nouvelle_transition):
        if ancienne_transition in self.listTransitions:
            index = self.listTransitions.index(ancienne_transition)
            if isinstance(nouvelle_transition, Transition) and nouvelle_transition.etatSource in self.listEtats and nouvelle_transition.etatDestination in self.listEtats and nouvelle_transition.alphabet in self.listAlphabets:
                self.listTransitions[index] = nouvelle_transition  # Remplace l'ancienne transition par la nouvelle dans la liste des transitions

    def beta(self, etat, alphabet):
        matches = []
        for transition in self.listTransitions:  # Fonction de transition
            if transition.etatSource == etat and transition.alphabet == alphabet:
                matches.append(transition.etatDestination)
        return matches  # Retourne une liste des états de destination pour un état source et un alphabet donnés

    def beta_dc(self, sommet, alphabet):
        for trans in self.listTransitions:  # Fonction de transition dans le cas où l'automate est complet et déterministe
            if trans.etatSource == sommet and trans.alphabet == alphabet:
                return trans.etatDestination  # Retourne l'état de destination pour un état source et un alphabet donnés

    def equivaux_next(self, etat1, etat2, S=[]):
        t = True
        for a in self.listAlphabets:
            if OutilsMathématique.find(self.beta_dc(etat1, a), self.beta_dc(etat2, a), S) == False:
                t = False
                break
        return t  # Vérifie si deux états sont équivalents pour tous les alphabets donnés

    def isReachable(self, i, j, d):
        t = False
        for a in i:
            for b in j:
                if self.beta_dc(a, d) == b:
                    t = True
                    break
        return t  # Vérifie s'il existe une transition entre deux ensembles d'états pour un alphabet donné

    def Unreachable(self):
        a = set(self.listInitiaux)
        t = True
        while t:
            t = False
            b = set()
            for transition in self.listTransitions:
                if transition.etatSource in a and transition.etatDestination not in a:
                    b.add(transition.etatDestination)
            if b:
                a.update(b)
                t = True
        unreachable_states = [etat for etat in self.listEtats if etat not in a]

        for etat in unreachable_states:
            self.supprimer_etat(etat)  # Supprime les états inaccessibles de l'automate

        return unreachable_states  # Retourne la liste des états inaccessibles

