from __future__ import division
from random import randint
import pexpect

class RicercaLocale(object):
    """docstring for RicercaLocale"""
    def __init__(self, times, distanze, tmov, tpresa, vel, dim, npacchi):
        self.times = times
       
        # la soluzione migliore
        self.best = None

        # salvo le informazioni
        self.distanze = distanze
        self.tmov = tmov
        self.tpresa = tpresa
        self.vel = vel
        self.dim = dim
        self.npacchi = npacchi

    def run(self, soluzione) :
        # per self.times volte
        # genero una nuova soluzione in modo casuale dalla prima
        # controllo che rispetti il vincolo
        # se lo fa, la appendo alle soluzioni

        # soluzione su cui fare la ricerca locale
        self.soluzione = soluzione
        self.length = len(soluzione)

        # elenco di possibili soluzioni generate
        self.solutions = list()

        # spawn clp using pexpect
        clp = pexpect.spawn("eclipseterminal -f check.ecl")
        # eseguo un comando a vuoto
        clp.sendline("A is 1+1.")
        clp.expect(".*:")
        line = clp.after

        for i in range(0, self.times):
            # genero sol
            sol = list()
            for i in range(0, self.length):
                sol.append(randint(1,5))
            # controllo che rispetti il vincolo
            stringa = "check(" + str(sol) + ", S, " + str(self.tmov) + ", " + str(self.tpresa) + ", " + str(self.vel) + ", " + str(self.dim) + ", " + str(self.npacchi) + ")."
            clp.sendline(stringa)
            clp.expect(".*:")
            if "Yes " in clp.after:
                self.solutions.append(sol)

        # fermiamo clp
        clp.sendline("halt.")
        clp.expect(pexpect.EOF) 

        # se non ha trovato neanche una soluzione buona, ci metto quella arrivata
        if len(self.solutions) == 0:
            self.solutions.append(self.soluzione)

    def find(self) :
        # una volta trovato il set di soluzioni trovo quella che ha goal minimo
        # per noi il goal minimo e' quella che ha meno occorrenze del valore 5 [pacchi persi]
        l = list()
        for s in self.solutions:
            l.append(s.count(5))
        # ritorno il valore minore
        return self.solutions[l.index(min(l))]
            