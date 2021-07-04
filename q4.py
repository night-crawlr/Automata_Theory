import json
import sys

if(len(sys.argv) != 3):
    print("Error : Usage python3 q4.py inpupt.json output.json")
    quit()


def reachble(dfa):
    startState = dfa['start_states'][0]
    checked = [0 for i in range(len(dfa['states']))]
    que = [startState]
    for el in que:
        for i, real in enumerate(dfa['states']):
            if(real == el):
                checked[i] = 1
    while(1):
        if(len(que) == 0):
            break

        for i, el in enumerate(que):
            que.pop(i)
            for transition_n in dfa['transition_function']:
                if(transition_n[0] == el):
                    dest = transition_n[2]
                    for i, real in enumerate(dfa['states']):
                        if(real == dest):
                            if(checked[i] == 0):
                                checked[i] = 1
                                que.append(real)
    statesChecked = []
    for i, v in enumerate(checked):
        if(v == 1):
            statesChecked.append(dfa['states'][i])
    return statesChecked


def input_convert(dfa):
    converted_dfa = {
        "states": [],
        "letters": [],
        "transition_function": [],
        "start_states": [],
        "final_states": []
    }
    dfa['states'] = reachble(dfa)
    # print(reachble(dfa))
    for state in dfa['states']:
        converted_dfa['states'].append([state])
    converted_dfa['letters'] = dfa['letters'].copy()
    for transition_n in dfa['transition_function']:
        state = transition_n[0]
        alphs = transition_n[1]
        dest = transition_n[2]
        if state not in dfa['states']:
            continue
        converted_dfa['transition_function'].append([[state], alphs, [dest]])
    converted_dfa['start_states'].append([dfa['start_states'][0]])
    for final_state in dfa['final_states']:
        if final_state not in dfa['states']:
            continue
        converted_dfa['final_states'].append([final_state])
    if(converted_dfa['final_states'] == []):
        print("Error in DFA final State is not mentioned or reachable from start state")
        quit()
    return converted_dfa


try:
    with open(sys.argv[1]) as f:
        dfa = json.load(f)
except:
    print("Error in file handling Check if file exists or not")

# NOTE each state is a array of strings
dfa = input_convert(dfa)
states = dfa['states']  # array of arrays of strings each nested array is state
alphabets = dfa['letters']  # array of strngs
# array of arrays each array contain three elemtns 1st is state, alphabet, final state
transitionFunction = dfa['transition_function']
startStates = dfa['start_states']  # array of states
finalStates = dfa['final_states']  # array of states


def conversion(arrayOfStates):
    # input will be the array of state note each state is an array of single string
    # print(arrayOfStates)
    toBeReturned = []
    for i in arrayOfStates:
        toBeReturned.append(i[0])
    return toBeReturned


def transition(state, alphabet):
    global transitionFunction
    for i in range(len(transitionFunction)):
        source = transitionFunction[i][0][0]
        alpha = transitionFunction[i][1]
        dest = transitionFunction[i][2][0]
        if((source == state) and (alphabet == alpha)):
            return dest


def setOf(state, p):
    for i in range(len(p)):
        for j in p[i]:
            if(j == state):
                return i


def isSameState(state1, state2, p):
    global alphabets
    for i in range(len(alphabets)):
        if((setOf(transition(state1, alphabets[i]), p) != setOf(transition(state2, alphabets[i]), p))):
            return 0
    return 1


def partition(p):
    p1 = []
    for i in range(len(p)):
        part = p[i]
        check_array = [0 for i in range(len(part))]
        dividedSetsForithPart = []
        for j in range(len(part)):
            if(check_array[j]):
                continue
            statesSimilarToj = []
            for k in range(j, len(part)):
                if(check_array[k]):
                    continue
                if(isSameState(part[j], part[k], p)):
                    check_array[k] = 1
                    statesSimilarToj.append(part[k])
            dividedSetsForithPart.append(statesSimilarToj)
        for l in dividedSetsForithPart:
            p1.append(l)

    return p1


def isSame(partitonedP, intinalP):
    # nested sorting and comparing both arrays
    temp1 = []
    for i in partionedP:
        temp1.append(sorted(i))
    temp1 = sorted(temp1)
    temp2 = []
    for i in intialP:
        temp2.append(sorted(i))
    temp2 = sorted(temp2)

    return (temp1 == temp2)


def findOneIndestState(single_state, p):
    for part in p:
        for state in part:
            if(state == single_state):
                return part.copy()


def prepare(p):
    final_dfa = {
        "states": [],
        "letters": [],
        "transition_function": [],
        "start_states": [],
        "final_states": []
    }
    for part in p:
        final_dfa['states'].append(part)
    final_dfa['letters'] = alphabets
    for state in final_dfa['states']:
        oneState = state[0]
        for alphs in alphabets:
            transitonForThisState = []
            oneIndestState = transition(oneState, alphs)
            finalState = findOneIndestState(oneIndestState, p)
            transitonForThisState.append(state)
            transitonForThisState.append(alphs)
            transitonForThisState.append(finalState)
            final_dfa['transition_function'].append(transitonForThisState)
    final_dfa['start_states'].append(findOneIndestState(startStates[0][0], p))
    for f in finalStates:
        finalState = findOneIndestState(f[0], p)
        flag = 0
        for final_state in final_dfa['final_states']:
            if(sorted(final_state) == sorted(finalState)):
                flag = 1
        if(flag == 0):
            final_dfa['final_states'].append(finalState)
    return final_dfa


# Preparing p0 (intialP) for p0 refer to https://www.geeksforgeeks.org/minimization-of-dfa/ step-1
intialP = []
intialP.append(list(conversion(finalStates)))
intialP.append(list(set(conversion(states)) - set(conversion(finalStates))))

# partioan untill you get the same partition
#i = 0
while(1):
    partionedP = partition(intialP)
    # print(intialP)
    # print(partionedP)

    if(isSame(partionedP, intialP)):
        minimised_dfa = prepare(intialP)
        try:
            with open(sys.argv[2], 'w') as f:
                json.dump(minimised_dfa, f, indent=4)
        except:
            print("Error in file handling ! Check if file exists or not")

        # print(intialP)
        # print(partionedP)
        break
    intialP = partionedP.copy()
