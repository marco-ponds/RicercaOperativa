from __future__ import division
from random import randint
import pexpect
import itertools

class Taboo(object):
    """docstring for Tabu"""
    def __init__(self, times, tentativi, maxnotfound, distanze, tmov, tpresa, vel, dim, npacchi):

        # numero massimo di tentativi
        self.times = times
        self.k = 0

        # numero massimo di passi senza soluzione
        self.maxtentativi = tentativi
        self.passi = 0;
        self.fail = 0;

        # numero massimo di soluzionoi migliori non trovate
        self.maxnotfound = maxnotfound
        self.notfound = 0
       
        # la soluzione migliore
        self.best = None

        # taboo list, passo proibito
        # dato che le soluzioni sono delle liste, le appendo
        self.taboo = []

        # salvo le informazioni
        self.distanze = distanze
        self.tmov = tmov
        self.tpresa = tpresa
        self.vel = vel
        self.dim = dim
        self.npacchi = npacchi

    def run(self, soluzione):
        '''
            finche non incontro la condizione di fine:
                genero un intorno della soluzione
                pesco a caso una soluzione ammissibile

                se il goal raggiungo dalla nuova soluzione e' minore della best
                Sbest = attuale soluzione
        '''

        # attuale soluzione migliore e' quella che ci siamo salvati
        self.best = soluzione
        self.Sk = soluzione

        while (True) :
            # genero un intorno di soluzioni di Sk
            intorno = list()

            # spawn clp using pexpect
            clp = pexpect.spawn("eclipseterminal -f check.ecl")
            # eseguo un comando a vuoto
            clp.sendline("A is 1+1.")
            clp.expect(".*:")
            line = clp.after

            for i in range(0, 100):
                # genero sol
                sol = list()
                for i in range(0, self.npacchi):
                    sol.append(randint(1,5))
                # controllo che rispetti il vincolo
                stringa = "check(" + str(sol) + ", " + str(self.distanze) + ", S, " + str(self.tmov) + ", " + str(self.tpresa) + ", " + str(self.vel) + ", " + str(self.dim) + ", " + str(self.npacchi) + ")."
                clp.sendline(stringa)
                clp.expect(".*:")
                if "Yes " in clp.after:
                    intorno.append(sol)

            # fermiamo clp
            clp.sendline("halt.")
            clp.expect(pexpect.EOF) 

            # chiudo eclipse, poraccio
            if clp.isalive():
                clp.close()

            # se non ha trovato neanche una soluzione buona, ho fallito e riprovo
            if len(intorno) == 0:
                self.fail += 1
                if self.check():
                    return self.best
                continue

            # scelgo a caso la soluzione da intorno
            index = randint(0, len(intorno)-1)
            Sc = intorno[index]
            while (Sc == self.Sk):
                self.fail += 1
                # se fallisco troppe volte ritorno Sbest
                if self.check():
                    return self.best
                index = randint(0, len(intorno)-1)
                Sc = intorno[index]

            # controllo se Sc e' migliore di Sbest
            # se il numero di 5 contenuti in Sc e' minore del numero di 5 contenuti in Sbest
            if Sc.count(5) < self.best.count(5):
                # se e' migliore, sbest = sc e ricomincio il ciclo
                self.best = Sc
                # resetto il contatore di soluzioni migliore non trovate
                self.notfound = 0
                self.k += 1
                if self.check():
                    return self.best
            else:
                # non ho trovato una soluzione migliore
                self.notfound += 1
                # controllo se passaggio Sk -> Sc e' proibito o no
                # se proibito ricomincio il ciclo
                # creo una versione fittizia del passaggio
                l = [i for i in itertools.chain(self.Sk, Sc)]
                if not self.taboo == l :
                    # se non e' proibito, Sref = Sc, e imposto self.taboo = [Sc|SK]
                    self.Sref = Sc
                    inverse = [i for i in itertools.chain(Sc, self.Sk)]
                    self.taboo = inverse
                    # incremento k
                    self.k += 1
                    # controllo se ho finito
                    if self.check():
                        # ho finito e ritorno best
                        return self.best
                    # altrimenti ricomincio il ciclo while

    def check(self) :
        # controllo se 
        return (self.fail > self.maxtentativi) or (self.k > self.times) or (self.notfound > self.maxnotfound) 




