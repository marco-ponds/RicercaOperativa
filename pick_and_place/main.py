from weppy import App, request
from weppy.tools import service

from random import randint

app = App(__name__)

# greedy nella versione grezza
@app.expose("/greedy1")
@service.json
def greedy_grezzo():

    print request.vars
    # reading parameters
    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)

    # velocita dei pacchi
    vel = 3;

    # le distanze in secondi tra i pacchi sono fisse
    distanze = list()
    randomdistance = randint(vel*3, (vel*3) + 10)
    for i in range(0, npacchi):
        distanze.append(randomdistance/vel)

    print tmov
    print tpresa

    from greedy_grezzo import Greedy

    # lancio algoritmo
    greedy = Greedy(tmov, tpresa, npacchi)
    greedy.run()

    # non ci interessano velocita o dimensione corrette
    return dict(status="OK", pacchi=greedy.pacchi, distanze=distanze, tmov=tmov, tpresa=tpresa, vel=3, dim=10)

# greedy considerando vel e distanze
@app.expose("/greedy2")
@service.json
def greedy_vel_dist():

    # reading parameters
    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)
    vel = int(request.vars.vel)

    #from greedy_velocita_distanze import Greedy
    from greedy_velocita_distanze import Greedy

    # lancio algoritmo
    greedy = Greedy(tmov, tpresa, npacchi, vel, True)
    greedy.run()

    return dict(status="OK", pacchi=greedy.pacchi, distanze=greedy.intertempo, tmov=tmov, tpresa=tpresa, vel=vel, dim=10)

# greedy considerando vel, distanze e movimento
@app.expose("/greedy3")
@service.json
def greedy_vel_dist_mov():

    # reading parameters
    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)
    vel = int(request.vars.vel)
    dim = int(request.vars.dim)

    print tmov
    print tpresa

    from greedy_velocita_distanze_movimento import Greedy

    # lancio algoritmo
    greedy = Greedy(tmov, tpresa, npacchi, vel, dim, True)
    greedy.run()

    return dict(status="OK", pacchi=greedy.pacchi, distanze=greedy.intertempo, tmov=tmov, tpresa=tpresa, vel=vel, dim=dim)

# greedy e ricerca locale
@app.expose("/greedyricercalocale")
@service.json
def greedy_ric_loc():
    
    from greedy_velocita_distanze_movimento import Greedy
    from ricercalocale import RicercaLocale

    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)
    vel = int(request.vars.vel)
    dim = int(request.vars.dim)

    # eseguo greedy
    greedy  = Greedy(tmov, tpresa, npacchi, vel, dim, True)
    (sol, dist) = greedy.run()

    # provo a migliorare usando la ricerca locale
    ricerca = RicercaLocale(100, dist, tmov, tpresa, vel, dim, npacchi)
    # eseguo ricerca locale prima a destra
    ricerca.run(sol)
    best = ricerca.find()

    return dict(status="OK", pacchi=best, distanze=greedy.intertempo, tmov=tmov, tpresa=tpresa, vel=vel, dim=dim)

# grasp
@app.expose("/grasp")
@service.json
def grasp():

    from grasp import Greedy
    from ricercalocale import RicercaLocale

    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)
    vel = int(request.vars.vel)
    dim = int(request.vars.dim)

    greedy  = Greedy(tmov, tpresa, npacchi, vel, dim, True)
    (pright, dist) = greedy.run(2)
    (pleft, dist) = greedy.run(1)

    ricerca = RicercaLocale(100, dist, tmov, tpresa, vel, dim, npacchi)
    
    # eseguo ricerca locale prima a destra
    ricerca.run(pright)
    best1 = ricerca.find()
    # .. poi a sinistra
    ricerca.run(pleft)
    best2 = ricerca.find()

    # a questo punto cerco la soluzione migliore tra queste due
    SOL = best1 if best1.count(5) < best2.count(5) else best2

    return dict(status="OK", pacchi=SOL, distanze=greedy.intertempo, tmov=tmov, tpresa=tpresa, vel=vel, dim=dim)

# tabu search
@app.expose("/taboo")
@service.json
def taboo():

    print request.vars
    # reading parameters
    tmov = int(request.vars.tmov)
    tpresa = int(request.vars.tpresa)
    npacchi = int(request.vars.npacchi)
    dim = int(request.vars.dim)

    # velocita dei pacchi
    vel = 3;

    # le distanze in secondi tra i pacchi sono fisse
    distanze = list()
    randomdistance = randint(vel*3, (vel*3) + 10)
    for i in range(0, npacchi):
        distanze.append(randomdistance/vel)

    print tmov
    print tpresa

    from tabu_search import Taboo
    from greedy_grezzo import Greedy

    # lancio algoritmo
    greedy = Greedy(tmov, tpresa, npacchi)
    greedy.run()

    taboo = Taboo(100, 20, 3, distanze, tmov, tpresa, vel, dim, npacchi)
    
    # eseguo taboo 
    SOL = taboo.run(greedy.pacchi)

    return dict(status="OK", pacchi=SOL, distanze=distanze, tmov=tmov, tpresa=tpresa, vel=vel, dim=dim)


if __name__ == "__main__":
    app.run()