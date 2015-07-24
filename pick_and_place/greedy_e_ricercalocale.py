from greedy_velocita_distanze_movimento import Greedy
from ricercalocale import RicercaLocale

if __name__ == '__main__':
    tmov = 5
    tpresa = 5
    npacchi = 15
    dim = 10
    V = 10

    # eseguo greedy
    greedy  = Greedy(tmov, tpresa, npacchi, V, dim, False)
    (sol, dist) = greedy.run()

    # provo a migliorare usando la ricerca locale
    ricerca = RicercaLocale(100, dist, tmov, tpresa, V, dim, npacchi)
    # eseguo ricerca locale prima a destra
    ricerca.run(sol)
    best = ricerca.find()

    # possiamo stampare la soluzione
    print best