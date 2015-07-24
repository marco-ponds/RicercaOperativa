class Greedy(object):
    """docstring for ClassName"""
    def __init__(self, Tmov, Tstart, TotPacchi):
        # robots
        self.R1 = {"start": 0, "flag": False}
        self.R2 = {"start": 0, "flag": False}
        self.R3 = {"start": 0, "flag": False}
        self.R4 = {"start": 0, "flag": False}
        self.Robots = [self.R1, self.R2, self.R3, self.R4]

        # timestamp
        self.seconds = 0

        # lista pacchi
        self.pacchi = list()

        # tempo occupazione macchina
        self.T = Tmov + Tstart

        # totale pacchi
        self.TotPacchi = TotPacchi

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
            # prendo il primo robot non impegnato
            index = 1
            for R in self.Robots:
                if not R['flag']:
                    break
                else:
                    index += 1

            # appendo l'indice alla lista dei pacchi
            self.pacchi.append(index)
            # se index != 5, prendo il robot corrispondente e lo imposto come occupato
            if not index == 5:
                self.Robots[index-1]['flag'] = True,
                self.Robots[index-1]['start'] = self.seconds

            # incremento il timestamp
            self.seconds += 1

            # se ho impostato TotPacchi esco dal ciclo
            if len(self.pacchi) == self.TotPacchi: 
                break

        print self.pacchi