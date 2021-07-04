import sys
import json
from itertools import combinations
if(len(sys.argv) != 3):
    print("Error : Usage python3 q2.py inpupt.json output.json")
    quit()


def input():
    try:
        with open(sys.argv[1]) as f:
            nfa = json.load(f)
    except:
        print("Error in file handling Check if file exists or not")
    return nfa


def output(dfa):
    try:
        with open(sys.argv[2], 'w') as f:
            json.dump(dfa, f, indent=4)
    except:
        print("Error in file handling ! Check if file exists or not")


def getStatesFromNFA(state, alpha, transition_funciton):
    finalStates = []
    for transition in transition_funciton:
        iniState = transition[0]
        alpha_t = transition[1]
        fiState = transition[2]
        if(iniState == state and alpha_t == alpha):
            finalStates.append(fiState)
    return finalStates


def nfa_to_dfa(nfa):
    states, letters, transition_function, start_states, final_states = nfa.values()
    states = sorted(states)
    # states of DFA
    dfa_states = []
    for r in range(len(states) + 1):
        for t in list(combinations(states, r)):
            dfa_states.append(list(t))

    # letters of DFA
    dfa_letters = letters

    # transition for DFA
    dfa_transition_function = []
    for state in dfa_states:
        if(state == []):
            for alpha in letters:
                dfa_transition_function.append([state, alpha, state])
            continue
        for alpha in letters:
            finalStates = []
            for s in state:
                finalForS = getStatesFromNFA(s, alpha, transition_function)
                finalStates = finalStates.copy() + finalForS.copy()
            finalStates = sorted(list(set(finalStates)))
            dfa_transition_function.append([state, alpha, finalStates])

    # start Staes for DFA
    dfa_start_states = [start_states]

    # final States for DFA
    dfa_final_states = []
    for finalState in final_states:
        for state in dfa_states:
            if finalState in state:
                if state not in dfa_final_states:
                    dfa_final_states.append(state)

    return ({
        'states': dfa_states,
        'letters': dfa_letters,
        'transition_function': dfa_transition_function,
        'start_states': dfa_start_states,
        'final_states': dfa_final_states
    })


nfa = {}
dfa = {}

nfa = input()
dfa = nfa_to_dfa(nfa)
output(dfa)
