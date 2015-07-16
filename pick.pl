:-lib(fd).
:-lib(fd_global).
:-lib(cumulative).


pick(Starts,Tmov,Tpresa,Velocita,Dimensione):-
			Npacchi = 2,
			
			D = Tmov + Tpresa,
			length(Risorse,Npacchi),
			length(Durate,Npacchi),
			length(Pacchi,Npacchi),
			riempi(Risorse,1),
			riempi(Durate,D),
			length(Starts,Npacchi),
			Pacchi::1..5,
			
			vincolo(Starts,Pacchi,0,Velocita,Dimensione),
			cumulative([0|Starts],[0|Durate],[0|Risorse],5),
			occurrences(5,Pacchi,Noccur),
			minimize(labeling(Pacchi),Noccur).


vincolo([],[],2,_,_).
vincolo([Start|TailStart],[ValPacco|TailPacco],I,Velocita,Dimensione):-

		4*Velocita*Start #>= I*10*4 + (ValPacco-1)*Dimensione,   /*  I*DISTANZA/VELOCITA */
	
		4*Velocita*Start #<= I*10*4 + ValPacco*Dimensione,
	
		I1 = I + 1,

		vincolo(TailStart,TailPacco,I1,Velocita,Dimensione).





riempi([],_).
riempi([A|T],A):-riempi(T,A).
