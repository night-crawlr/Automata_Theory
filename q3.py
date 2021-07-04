import sys
import json
import random

if(len(sys.argv) != 3):
    print("Error : Usage python3 q2.py inpupt.json output.json")
    quit()

REGEX = "regex"
STATES = "states"
LETTERS = "letters"
TRANSITIONFUNCTION = "transition_function"
STARTSTATES = "start_states"
FINALSTATES = "final_states"
EPSILON = "$"
START = "_START_" + "20191"
FINAL = "_FINAL_" + "01116"


def input():
    try:
        with open(sys.argv[1]) as f:
            dfa = json.load(f)
    except:
        print("Error in file handling Check if file exists or not")
    return dfa


def output(regex):
    try:
        with open(sys.argv[2], 'w') as f:
            json.dump({REGEX: regex}, f, indent=4)
    except:
        print("Error in file handling Check if file exists or not")


class GNFA():
    def __init__(this, dfa):
        this.states = dfa[STATES]
        this.letters = dfa[LETTERS]
        this.transition_function = dfa[TRANSITIONFUNCTION]
        this.start_states = dfa[STARTSTATES]
        this.final_states = dfa[FINALSTATES]
        this.convertToGNFA()

    def convertToGNFA(this):

        this.states.append(START)
        this.states.append(FINAL)

        this.letters.append(EPSILON)

        this.transition_function.append(
            [START, EPSILON, this.start_states[0]])
        for finalState in this.final_states:
            this.transition_function.append([finalState, EPSILON, FINAL])
        for transition in this.transition_function:
            s = transition[0]
            f = transition[2]
            alphas = []
            for search in this.transition_function:
                if search[0] == s and search[2] == f:
                    alphas.append(search[1])
            transition[1] = this.addList(alphas)

        this.start_states = [START]
        this.final_states = [FINAL]

    def beautify(this, regex):
        handsome_regex = []
        division_indexes = [-3]
        replaced_letters = []
        for i in range(len(regex) - 3):
            if(regex[i] == "(" and regex[i+1] in this.letters and regex[i+2] == ")"):
                division_indexes.append(i)
                replaced_letters.append(regex[i+1])
        for i in range(len(division_indexes)):
            if(i == len(division_indexes) - 1):
                handsome_regex.append(regex[division_indexes[i] + 3:])
                break
            handsome_regex.append(
                regex[division_indexes[i] + 3: division_indexes[i+1]])
            handsome_regex.append(replaced_letters[i])

        return ''.join(handsome_regex)

    def addList(this, R):
        if R == []:
            return ""
        if len(R) == 1:
            if(R[0][0] == "("):
                return R[0]
            return "(" + R[0] + ")"
        return "(" + '+'.join(R) + ")"

    def prepareRegex(this):
        if len(this.states) == 2:
            R = []
            for transtition in this.transition_function:
                if(transtition[0] == START and transtition[2] == FINAL):
                    R.append(transtition[1])
            return this.addList(R)

        # Selecting rip states
        ripState = ""
        for state in this.states:
            if state != START and state != FINAL:
                ripState = state
                break
        #print("Decided to remove " + ripState)
        transitionsToBeRemoved = []
        # Preparing R2 ie self transitions from rip to rip and  noting then in transitionsToBeRemoved so that we can remove in future
        R2 = []
        # print()
        for transtition in this.transition_function:
            if transtition[0] == ripState and transtition[2] == ripState:
                R2.append(transtition[1])
                transitionsToBeRemoved.append((transtition, "R2"))
                #print("\t"+str(transtition), end=" R2 \n")
        R2 = this.addList(R2)
        R2 = "(" + R2 + "*)" if (R2 != "") else "(" + EPSILON + ")"
        #print("\nR2 : " + R2)
        # Changing transition for all transitions assuming that rip doesn't exist
        for qi in this.states:
            # print()
            #print("\tSelecting ith state " + str(qi))
            if qi == ripState or qi == FINAL:
                continue

            # Preparing R1 ie transition from qi to qrip and storing the transitions to remove in future after removing rip
            R1 = []
            for transtition in this.transition_function:
                if transtition[0] == qi and transtition[2] == ripState:
                    R1.append(transtition[1])
                    transitionsToBeRemoved.append((transtition, "R1"))
                    #print(str("\t\t") + str(transtition), end=" R1 \n")
            R1 = this.addList(R1)
            #print("\n\tR1 : " + R1)
            for qj in this.states:
                # print()
                #print("\t\tSelecting jth state " + str(qj))
                if qj == START or qj == ripState:
                    continue

                # Preparing R3 ie transition from qrip to qj and storing the transitions to remove in future after removing rip
                R3 = []
                for transtition in this.transition_function:
                    if transtition[0] == ripState and transtition[2] == qj:
                        R3.append(transtition[1])
                        transitionsToBeRemoved.append((transtition, "R3"))
                        #print("\t\t\t" + str(transtition), end=" R3 \n")
                R3 = this.addList(R3)
                #print("\n\t\tR3 : " + R3)
                # Preparing R4 ie transitions from qi to qj and storing the transitons by adding each of them
                # print()
                R4 = []
                WECANREMOVEHERE = []
                for transtition in this.transition_function:
                    if transtition[0] == qi and transtition[2] == qj:
                        R4.append(transtition[1])
                        WECANREMOVEHERE.append((transtition, "R4"))
                        #print("\t\t\t" + str(transtition), end=" R4 \n")
                for transtition in WECANREMOVEHERE:
                    this.transition_function.remove(transtition[0])

                R4 = this.addList(R4)
                #print("\n\t\tR4 : " + R4)
                R = ""
                # R = "((" + R1 + R2 + R3 + ")+" + R4 + \
                #    ")" if not (R1 == "" or R3 == "") else R4
                if R1 == "" or R3 == "":
                    if R4 == "":
                        R = ""
                    else:
                        R = R4
                else:
                    R = "(" + R1 + R2 + R3 + ")"
                    if R4 != "":
                        R += "+" + R4
                        R = "(" + R + ")"
                #print("\n\t\tR : " + R)
                if(R != ""):
                    this.transition_function.append([qi, R, qj])

        # Succuesfully updated all transitions now we need to do is removing the rip state and the unneccesary transitions
        this.states.remove(ripState)
        [this.transition_function.remove(
            transtition[0]) for transtition in transitionsToBeRemoved if transtition[0] in this.transition_function]
        return this.prepareRegex()


dfa = input()
gnfa = GNFA(dfa)
regular_expression = gnfa.prepareRegex()
regular_expression = gnfa.beautify(regular_expression)
output(regular_expression)
