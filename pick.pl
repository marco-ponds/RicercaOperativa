:-lib(fd).
:-lib(fd_global).
:-lib(cumulative).


pick(Pacchi,Tmov,Tpresa,Velocita,Dimensione,Npacchi):-
		
			D is Tmov + Tpresa,
			length(Risorse,Npacchi),
			length(Durate,Npacchi),
			length(Pacchi,Npacchi),
			riempi(Risorse,1),
			riempi(Durate,D),
			length(Starts,Npacchi),
			primo_pacco_start_zero(Starts),
			Pacchi::1..5,

			%fd_global:alldifferent(Starts),
			vincolo(Starts,Pacchi,0,Velocita,Dimensione),
			cumulative(Starts,Durate,Risorse,5),
			occurrences(5,Pacchi,Noccur),
			minimize(labeling(Pacchi),Noccur).


primo_pacco_start_zero([0|_]).

vincolo([],[],_,_,_).
vincolo([Start|TailStart],[ValPacco|TailPacco],I,Velocita,Dimensione):-

		5*Velocita*Start #>= I*1*5 + (ValPacco-1)*Dimensione,   /*  I*DISTANZA/VELOCITA */
	
		5*Velocita*Start #<= I*1*5 + ValPacco*Dimensione,

		I1 is I + 1,

		vincolo(TailStart,TailPacco,I1,Velocita,Dimensione).
		
		
		
riempi([],_).
riempi([A|T],A):-riempi(T,A).
