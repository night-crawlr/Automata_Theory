# Automata Theory

## Submitted by

Manubolu Narain Sreehith, 2019101116

## Question 1

## 1 . Regex to NFA

- First converted Regex from infix ot outfix
- Later wrote funcitons for each of operations UNION, STAR, CONCAT
- Converting regex to NFA by poping elemts from stack and performing corresponding operation

## 2. NFA to DFA

- NFA is taken as input
- converting the n states of NFA to 2^n states in DFA where each is the combination of any number of states from NFA
- Wrote a funciton to get final states of a corresponding transition in DFA from NFA and appednde it to the DFA transition
- DFA is dumped to the mentioned OUTPUT file

## 3. DFA to Regex

- Converted DFA to GNFA
- Choosing a Rip state at an iteration
- In that iteration , we will update the other transition ie from any qi to qj with formula R1R2\*R3 U R4
  where R1 is transiiton from qi, RIP , R2 is transition from RIP to RIP , R3 is transition from RIP to qj, R4 is transition from qi to qj

- Repeat above process untill no of states are only 2

## 4. Minimization Of DFA

- In this step we will make a partition of all sates into final and non final states and name the set of partitions as P0
- Next we will try to further partion the each set , partition is based on the equivalence of states in that partition, ie states in same partition are treated as same stated in the DFA
- Equivalency is decided by checking if all transitions of 2 states corresponds to same partiton or not , if they belong to same partition they will be treated as equivalence else not
- now each set in P0 is divided based on above equivalency, and name the new partiion as P1 and repeat this untill pi == pi+1
- now the sets in pi are the final states of minimised - DFA
- Now fill the corresponding transititon table and OUTPUT the DFA

VIDEO LINK FOR EXECUTION : [Video](https://iiitaphyd-my.sharepoint.com/:v:/g/personal/narain_sreehith_students_iiit_ac_in/EQgF-sPB_I5Psgt0hiqU_DIBdeNh2Wboou6Mhjn0oUMcDw?e=WtaAlI)
