# Ricerca Operativa

sia dato un nastro su cui scorrono degli oggetti disposti in posizione casuale. Lungo il nastro, con spazi di lavoro adiacenti, sono disposti 4 robot che effettuano il picking automatico degli oggetti mentre questi transitano nel proprio spazio di lavoro, e li depositano in una posizione nota nello spazio retrostante. Nota la dimensione e la velocità del nastro, la posizione degli oggetti e il tempo di movimentazione e di presa dei robot, determinare l’assegnazione degli oggetti ai robot in modo tale che sia minimo il numero di pezzi persi (non prelevati).

----

### valori noti

dimensione nastro **dn**

velocità nastro **vn**

posizione oggetti **pos[pos_0, .. , pos_n-1]**

numero oggetti **n**

tempo di movimento **t_mov**

tempo presa **t_presa**

----

Risultato espresso come 

**[R1, R3, R4..]**

posizione 0, primo oggetto assegnato a R1, ecc

