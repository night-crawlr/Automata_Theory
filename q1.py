import json
import sys

operators = {
    '+': 0,
    '.': 1,
    '*': 2
}
eplsilon = '$'
stateCounter = 0


class nfa():
    def __init__(this):
        this.states = []
        this.letters = []
        this.transition_function = []
        this.start_states = []
        this.final_states = []

    def TransformToSingleCharacterNFA(this, ch):
        start = getNewState()
        final = getNewState()
        this.states = [start, final]
        this.letters = [ch]
        this.transition_function = [[start, ch, final]]
        this.start_states = [start]
        this.final_states = [final]

    def TransformToKleenStar(this):
        start = getNewState()
        this.states.append(start)

        this.letters.append(eplsilon)
        this.letters = list(set(this.letters))

        for prevStart in this.start_states:
            for prevFinal in this.final_states:
                this.transition_function.append(
                    [prevFinal, eplsilon, prevStart])
            this.transition_function.append([start, eplsilon, prevStart])

        this.start_states = [start]
        this.final_states.append(start)

    def unionWith(this, nfa2):
        start = getNewState()

        this.states = this.states + nfa2.states
        this.states.append(start)

        this.letters = this.letters + nfa2.letters
        this.letters.append(eplsilon)
        this.letters = list(set(this.letters))

        this.transition_function = this.transition_function + nfa2.transition_function
        this.transition_function.append(
            [start, eplsilon, this.start_states[0]])
        this.transition_function.append(
            [start, eplsilon, nfa2.start_states[0]])

        this.start_states = [start]
        this.final_states = this.final_states + nfa2.final_states

    def concatWith(this, nfa2):
        this.states = this.states + nfa2.states

        this.letters = this.letters + nfa2.letters
        this.letters.append(eplsilon)
        this.letters = list(set(this.letters))

        this.transition_function = this.transition_function + nfa2.transition_function
        for prevFinal in this.final_states:
            for prevStart in nfa2.start_states:
                this.transition_function.append(
                    [prevFinal, eplsilon, prevStart])

        this.start_states = this.start_states
        this.final_states = nfa2.final_states


def input():
    if(len(sys.argv) != 3):
        print("Error : Usage python3 q2.py inpupt.json output.json")
        quit()

    try:
        with open(sys.argv[1]) as f:
            regex = json.load(f)
    except:
        print("Error in file handling Check if file exists or not")
    return regex['regex']


def output(nfa):
    try:
        with open(sys.argv[2], 'w') as f:
            json.dump(nfa, f, indent=4)
    except:
        print("Error in file handling ! Check if file exists or not")


def getNewState():
    global stateCounter
    stateCounter += 1
    return 'Q' + str(stateCounter)


def convert_concatenate(regex):
    # print(regex)
    if(regex == ""):
        output({
            'states': ["Q0", "Q1"],
            'letters': [""],
            'transition_matrix': [["Q0", "", "Q1"]],
            "start_states": ["Q0"],
            "final_states": ["Q1"]
        })
        quit()
    if(len(regex) == 1):
        return regex

    dotArray = []
    for i in range(len(regex) - 1):
        boolArray = []
        boolArray.append(regex[i].isalnum() and regex[i+1] == '(')
        boolArray.append(regex[i].isalnum() and regex[i+1].isalnum())
        boolArray.append(regex[i] == ')' and regex[i+1].isalnum())
        boolArray.append(regex[i] == '*' and regex[i+1] == '(')
        boolArray.append(regex[i] == '*' and regex[i+1].isalnum())
        if True in boolArray:
            dotArray.append(i)
    regexWithDot = []
    for i in range(len(dotArray)):
        if not i:
            regexWithDot.append(regex[:dotArray[i]+1])
            continue
        regexWithDot.append('.')
        regexWithDot.append(regex[dotArray[i-1] + 1:dotArray[i]+1])
    regexWithDot.append('.')
    regexWithDot.append(regex[dotArray[-1] + 1:])
    # print(regexWithDot)
    regexWithDot = ''.join(regexWithDot)
    # print(regexWithDot)
    return regexWithDot


def postfixOf(regex):
    global operators

    postfix = []
    stack = []

    for i, ch in enumerate(regex):
        if ch in operators:

            # No operator in stack
            if not len(stack):
                stack.append(ch)
                continue

            # operator in stack checks for valid precedence order
            if stack[-1] == '(' or stack[-1] == ')':
                stack.append(ch)
                continue

            while(1):
                if((not len(stack)) or (stack[-1] not in operators) or (operators[ch] > operators[stack[-1]])):
                    stack.append(ch)
                    break
                postfix.append(stack.pop())
        elif ch in ['(', ')']:
            if ch == '(':
                stack.append(ch)
                continue

            while(1):
                if(stack[-1] == '('):
                    stack.pop()
                    break
                postfix.append(stack.pop())
        else:
            postfix.append(ch)

    while len(stack):
        postfix.append(stack.pop())
    return postfix


def regex_to_nfa(regex):
    postfix = postfixOf(regex)
    stack = []
    for i, ch in enumerate(postfix):
        if ch not in operators:
            nfaForch = nfa()
            nfaForch.TransformToSingleCharacterNFA(ch)
            stack.append(nfaForch)
            continue

        if ch == '*':
            nfaForStar = stack.pop()
            nfaForStar.TransformToKleenStar()
            stack.append(nfaForStar)
        elif ch == '+':
            nfaForUnionRight = stack.pop()
            nfaForUnionLeft = stack.pop()
            nfaForUnionLeft.unionWith(nfaForUnionRight)
            stack.append(nfaForUnionLeft)
        elif ch == '.':
            nfaForConcatRight = stack.pop()
            nfaForConcatLeft = stack.pop()
            nfaForConcatLeft.concatWith(nfaForConcatRight)
            stack.append(nfaForConcatLeft)
    return stack.pop()


if __name__ == "__main__":

    regex = input()
    regex = convert_concatenate(regex)
    nfa = regex_to_nfa(regex)
    output(nfa.__dict__)
