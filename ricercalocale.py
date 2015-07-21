from __future__ import division
from random import randint

class RicercaLocale(object):
    """docstring for RicercaLocale"""
    def __init__(self, soluzione, times):
        # soluzione su cui fare la ricerca locale
        self.soluzione = soluzione
        self.length = len(soluzione)
        self.times = times
        # elenco di possibili soluzioni generate
        self.solutions = list()
        # la soluzione migliore
        self.best = None

    def run(self) :
        # per self.times volte
        # genero una nuova soluzione in modo casuale dalla prima
        # controllo che rispetti il vincolo
        # se lo fa, la appendo alle soluzioni
        for i in range(0, self.times):
            # genero sol
            sol = list()
            for i in self.length:
                sol.append(randint(1,5))
            # controllo che rispetti il vincolo
            if self.vincolo(sol):
                self.solutions.append(sol)

    def find(self) :
        # una volta trovato il set di soluzioni trovo quella che ha goal minimo
        # per noi il goal minimo è quella che ha meno occorrenze del valore 5 [pacchi persi]
        pass
        
    def vincolo(self, soluzione):
        # Starts, Durate, Pacchi, Velocita, Dimensione, Durata
        for i in range(0, self.length):
            
         5*Velocita*Start >= I*10*5 + (ValPacco-1)*Dimensione,   /*  I*DISTANZA/VELOCITA */
    
        5*Velocita*Start < I*10*5 + ValPacco*Dimensione,