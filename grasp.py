from __future__ import division
from random import randint
from ricercalocale import RicercaLocale

class Greedy(object):
    """docstring for ClassName"""
    def __init__(self, Tmov, Tstart, TotPacchi, Vel, Size, random):

        self.workArea = Size/4
        reach1 = 0
        reach2 = 1*self.workArea/Vel
        reach3 = 2*(self.workArea/Vel)
        reach4 = 3*(self.workArea/Vel)
        # robots
        self.R1 = {"start": 0, "flag": False, "reach": reach1}
        self.R2 = {"start": 0, "flag": False, "reach": reach2}
        self.R3 = {"start": 0, "flag": False, "reach": reach3}
        self.R4 = {"start": 0, "flag": False, "reach": reach4}
        self.Robots = [self.R1, self.R2, self.R3, self.R4]

        # tempo occupazione macchina
        self.T = Tmov + Tstart

        # totale pacchi
        self.TotPacchi = TotPacchi

        # velocita pacchi
        self.Vel = Vel

        # distanze
        if random:
            self.distanze = [0]
            for i in range(1, TotPacchi):
                self.distanze.append(randint(1, 20))
        else:
            self.distanze = [0]
            for i in range(1, TotPacchi):
                self.distanze.append(10)

        # secondi tra pacchi
        self.intertempo = []
        for d in self.distanze:
            self.intertempo.append(d/self.Vel)

    def run(self, mode):
        # mi salvo il mode selezionato
        self.mode = mode

        # indice di pacco
        self.indexPacco = 0

        # tempo di riferimento pacco
        self.tref = 0

        # timestamp
        self.seconds = 0

        # lista pacchi
        self.pacchi = list()

        self.R1["start"] = 0
        self.R1["flag"] = False
        self.R2["start"] = 0
        self.R2["flag"] = False
        self.R3["start"] = 0
        self.R3["flag"] = False
        self.R4["start"] = 0
        self.R4["flag"] = False

        while True:
            # controllo se i robot sono impegnati
            for R in self.Robots :
                if R['flag']:
                    # robot occupato
                    if (self.seconds - R['start']) >= self.T:
                        # robot non impegnato
                        R['flag'] = False
                # se R.flag = false, robot non impegnato

            t = self.tref + self.intertempo[self.indexPacco]
            if self.seconds >= t:
                # vuol dire che il pacco indexPacco parte
                # assegnazione                
                # prendo il primo robot non impegnato
                index = 1
                soluzioni = list()
                for R in self.Robots:
                    if R['flag']:
                        # robot occupato, controllo se si libera
                        if (self.seconds + R['reach']) - R['start'] >= self.T:
                            # il robot si libera mentre mi muovo
                            soluzioni.append(index)
                            index += 1
                        else:
                            index += 1
                    else:
                        soluzioni.append(index)
                        index += 1

                if len(soluzioni) == 0:
                    soluzioni.append(5)

                if self.mode == 1:
                    toappend = soluzioni[0]
                else:
                    toappend = soluzioni[-1]
                # appendo l'indice alla lista dei pacchi
                self.pacchi.append(toappend)
                # se toappend != 5, prendo il robot corrispondente e lo imposto come occupato
                if not toappend == 5:
                    self.Robots[toappend-1]['flag'] = True,
                    self.Robots[toappend-1]['start'] = self.seconds + self.Robots[toappend-1]['reach']

                # una volta fatta assegnazione, incremento indexPacco
                self.indexPacco += 1

                # salvo nuovo tref
                self.tref = t

            # incremento il timestamp
            self.seconds += 1

            # se ho impostato TotPacchi esco dal ciclo
            if len(self.pacchi) == self.TotPacchi: 
                break

        return (self.pacchi, self.distanze)
        


if __name__ == '__main__':
    '''
        genero un set di soluzioni sfruttando i punti di scelta
        una volta ottenute le due soluzioni (destra e sinistra) eseguo
        l'algoritmo di ricerca locale sulle due soluzioni

        una volta fatto, cerco la soluzione migliore tra le soluzioni migliori ottenute prima.
    '''
    tmov = 5
    tpresa = 5
    npacchi = 15
    dim = 10
    V = 10

    greedy  = Greedy(tmov, tpresa, npacchi, V, dim, False)
    (pright, dist) = greedy.run(2)
    (pleft, dist) = greedy.run(1)

    ricerca = RicercaLocale(100, dist, tmov, tpresa, V, dim, npacchi)
    # eseguo ricerca locale prima a destra
    ricerca.run(pright)
    best1 = ricerca.find()
    # .. poi a sinistra
    ricerca.run(pleft)
    best2 = ricerca.find()

    # a questo punto cerco la soluzione migliore tra queste due
    SOL = best1 if best1.count(5) < best2.count(5) else best2

    # possiamo stampare la maledetta soluzione
    print SOL
