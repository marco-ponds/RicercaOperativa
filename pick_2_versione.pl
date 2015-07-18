:-lib(fd).
:-lib(fd_global).
:-lib(propia).
:-lib(cumulative).


/*
IN QUESTA SECONDA VERSIONE RAGIONIAMO IN MANIERA UN PO' DIVERSA:

PRIMA: 

-I pacchi considerati "persi" erano quelli che finivano nel robot fittizzio n° 5 ,
e per minimizzarli bastava minimizzare le occorrenze dei pacchi marcati con il "5".
Il problema era riuscire a definire un vincolo che imponesse ad un pacco di finire nella 
successiva macchina libera: di fatti, nei test , il primo pacco finiva correttamente nel primo robot,
ma i successivi finivano subito nella macchina 5 (sbagliato, devono finire nelle macchine 2,3,4 e POI 
nella 5° , se le precedenti sono "occupate".
-le durate dei task erano tutte uguali (sia che fossero nelle macchine 1..4 che nella 5°)
-DIFFICILE trovare un esempio di scheduling dove vengono minimizzati i pacchi che finiscono nella
macchina n°5 (ad esempio).

ADESSO: 

-i task che finiscono nella macchina n°5 hanno imposta una durata MOLTO ELEVATA rispetto a quelli che finiscono
nelle macchine precedenti
Facendo cosi, se vogliamo minimizzare i pacchetti che finiscono nella macchina 5, basta minimizzare
il tempo totale di esecuzione di tutti i task (Meno task finiscono nella macchina 5, minore sara' il tempo
totale di esecuzione di tutti i task)
-Esprimere questo vincolo è piu semplice del problema precedente, e ci sono gia molti esempi di scheduling dove si
vuole minimizzare il tempo totale di esecuzione.

*/

pick(Pacchi,Tmov,Tpresa,Velocita,Dimensione,Npacchi):-
		
			D is Tmov + Tpresa,
			length(Risorse,Npacchi),
			length(Durate,Npacchi),
			length(Pacchi,Npacchi),
			riempi(Risorse,1),
			%vincolo_durata(Pacchi,Durate,D) infers fd,  /* I pacchi marcati 1..4 hanno durata fissa come prima, quelli marcati 5 hanno durata molto piu elevata*/
			riempi(Durate,D),
			length(Starts,Npacchi),
			primo_pacco_start_zero(Starts),
			Pacchi::1..5,
			
			vincolo(Starts,Pacchi,0,Velocita,Dimensione),
			cumulative(Starts,Durate,Risorse,5),
			sumlist(Pacchi,VAL),

			%fd_global:occurrences(5,Pacchi,Noccur),
			%sumlist(Pacchi,SUM),
			minimize(labeling(Pacchi),VAL).


vincolo_durata([],[],_).
vincolo_durata([Pk|Tail],[A|TailDur],D):-
	
	Pk #= 5 ,
	A #= 10*D,
	vincolo_durata(Tail,TailDur,D).

vincolo_durata([Pk|Tail],[A|TailDur],D):-

	Pk #\= 5,
	A #= D,
	vincolo_durata(Tail,TailDur,D).

primo_pacco_start_zero([0|_]).

vincolo([],[],_,_,_).
vincolo([Start|TailStart],[ValPacco|TailPacco],I,Velocita,Dimensione):-

		5*Velocita*Start #>= I*10*5 + (ValPacco-1)*Dimensione,   /*  I*DISTANZA/VELOCITA */
	
		5*Velocita*Start #=< I*10*5 + ValPacco*Dimensione,

		I1 is I + 1,

		vincolo(TailStart,TailPacco,I1,Velocita,Dimensione).
	
riempi([],_).
riempi([A|T],A):-riempi(T,A).
