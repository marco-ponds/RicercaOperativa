from __future__ import division
from random import randint

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

        # timestamp
        self.seconds = 0

        # lista pacchi
        self.pacchi = list()

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
                random_d = randint(Vel*3, (Vel*3) + 10)
                self.distanze.append(random_d)
        else:
            self.distanze = [0]
            for i in range(1, TotPacchi):
                self.distanze.append(10)

        # secondi tra pacchi
        self.intertempo = []
        for d in self.distanze:
            self.intertempo.append(d/self.Vel)

        # indice di pacco
        self.indexPacco = 0

        # tempo di riferimento pacco
        self.tref = 0

    def run(self):
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
                for R in self.Robots:
                    if R['flag']:
                        # robot occupato, controllo se si libera
                        if (self.seconds + R['reach']) - R['start'] >= self.T:
                            # il robot si libera mentre mi muovo
                            break
                        else:
                            index += 1
                    else:
                        break


                # appendo l'indice alla lista dei pacchi
                self.pacchi.append(index)
                # se index != 5, prendo il robot corrispondente e lo imposto come occupato
                if not index == 5:
                    self.Robots[index-1]['flag'] = True,
                    self.Robots[index-1]['start'] = self.seconds + self.Robots[index-1]['reach']

                # una volta fatta assegnazione, incremento indexPacco
                self.indexPacco += 1

                # salvo nuovo tref
                self.tref = t

            # incremento il timestamp
            self.seconds += 1

            # se ho impostato TotPacchi esco dal ciclo
            if len(self.pacchi) == self.TotPacchi: 
                break

        print "pacchi   ", self.pacchi
        print "distanze ", self.distanze

        return (self.pacchi, self.distanze)


if __name__ == '__main__':
    #            Tm Tp Tot Vel distanze
    test = Greedy(5, 5, 30, 10, 10, True)
    test.run()