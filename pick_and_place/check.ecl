:-lib(ic).
%:-lib(ic_global).
:-lib(propia).
:-lib(ic_cumulative).


/*
    questo programma viene usato solamente per controllare la validità di una soluzione
    se clp è in grado di trovare una soluzione, facendo il labeling di Starts, allora
    la soluzione passata è valida.
*/

pick(Pacchi, Distanze, Starts, Tmov, Tpresa, Velocita, Dimensione, Npacchi):-
        
    D is Tmov + Tpresa,
    length(Risorse, Npacchi),
    length(Durate, Npacchi),
    length(Pacchi ,Npacchi),
    riempi(Risorse, 1),
    riempi(Durate,D),
    length(Starts, Npacchi),
    Pacchi::[1,2,3,4,5],
    
    vincolo(Starts, Distanze, Pacchi, 0, Velocita, Dimensione, D),
    cumulative(Starts,Durate,Risorse,5),

    labeling(Starts).


vincolo([],[],[],_,_,_,_).
vincolo([HStart|TailStart], [Hdist|Taildist], [Hpacchi|Tailpacchi], 0, V, Dim, Dur) :-
    HStart #= 0,
    vincolo(TailStart, Taildur, Tailpacchi, 1, V, Dim, Dur).
vincolo([Start|TailStart], [Hdist|Taildist], [ValPacco|TailPacco],I,Velocita,Dimensione, Dur):-
    
    5*Velocita*Start #>= I*Hdist*5 + (ValPacco-1)*Dimensione,
    5*Velocita*Start #=< I*Hdist*5 + ValPacco*Dimensione,

    I1 is I + 1,

    vincolo(TailStart, Taildur, TailPacco,I1,Velocita,Dimensione, Dur).

riempi([],_).
riempi([A|T],A):-riempi(T,A).

