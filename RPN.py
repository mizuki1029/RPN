#This program follows the steps below.
#(1) formula was read
#(2) tokenize it
#(3) convert its notation into Reverse Polish Notation
#(4) calculate converted formula
#(5) print answer

import csv

FILE_NAME = "result.csv"
 
#calculate RPN formula
def evaluate(tokens):
    operator = {
        '+': (lambda a, b : a + b),
        '-': (lambda a, b : a - b),
        '*': (lambda a, b : a * b),
        '/': (lambda a, b : float(a) / b)
    }
    stack = []
    for token in tokens:
        if token.isdigit() or '.' in token:
            stack.append(token)
            continue
        else:
            b = float(stack.pop())
            a = float(stack.pop())
            stack.append(operator[token](a, b))
    return stack[0]


#convert the notation(normal formula) into reverse polish notation
def ReversePolishNotation(tokens):
    fixedtokens = []
    stack = []
    for token in tokens:
        if token.isdigit() or '.' in token:
            fixedtokens.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            #until "(" appears, pop operands from stack
            while stack[-1] != '(':
                fixedtokens.append(stack.pop())
            stack.pop()
        else:
            #if the priority of token is less than or equal to the priority of operand in stack
            while len(stack)!=0 and checkPriority(token, stack[-1]):
                fixedtokens.append(stack.pop())
            stack.append(token)
    #pop all operands from stack and push it into fixedtokens
    while len(stack)!=0:
        fixedtokens.append(stack.pop())

    return fixedtokens


#if the priority of operand1 is less than or equal to the priority of operand2, then return true
def checkPriority(operand1, operand2):
    if operand1 in '*/' and operand2 in '*/':
        return True
    elif operand1 in '+-' and operand2 in '+-*/':
        return True
    else:
        return False


#tokenize the formula
def tokenize(line):
    tokens = []
    index = 0
    numlist = []
    numflag = 0
    while index < len(line):
        nums = ''
        if line[index].isdigit() or '.' in line[index]:
            numflag = 1
            numlist.append(line[index]) #for two or more digit number and decimals
        elif line[index] in '+-*/()': #operands and brackets
            if numflag ==1:
                nums = ''.join(numlist)
                numlist = [] #initialize
                tokens.append(nums) #push number
                numflag = 0 #initialize
            tokens.append(line[index]) #push operand
        else:
            print("Invalid character found: " + str(line[index]))
            exit(1)
        #if last token is a number
        if index ==len(line)-1 and line[index].isdigit():
            nums = ''.join(numlist)
            tokens.append(nums)
        index += 1
    return tokens

with open(FILE_NAME, "w", encoding="utf-8", errors=FILE_NAME + "create error") as f:
            writer = csv.writer(f)
            row = ["formula", "answer"]
            writer.writerow(row)

print("Please input formula and press the Enter key.")
print("You can confirm your inputs and the answers.")
print("If you input 'c', the results are deleted.")

while True:
    print("> ", end="")
    line = input() #(1) formula was read
    line = line.replace(' ', '') #delete spaces
    line = line.replace('=', '') #delete equals sign
    if line == "c":
        with open(FILE_NAME, "w", encoding="utf-8", errors=FILE_NAME + "create error") as f:
            writer = csv.writer(f)
            row = ["formula", "answer"]
            writer.writerow(row)
    else:
        tokens = tokenize(line)  #(2) tokenize it
        tokens = ReversePolishNotation(tokens) #(3) convert its notation into Reverse Polish Notation
        answer = evaluate(tokens) #(4) calculate converted formula
        print(answer) #(5) print answer
        with open(FILE_NAME, "a", encoding="utf-8", errors=FILE_NAME + "create error") as f:
            writer = csv.writer(f)
            row = [line, answer]
            writer.writerow(row)
    
