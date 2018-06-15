#This program follows the steps below.
#(1) formula was read
#(2) tokenize it
#(3) convert its notation into Reverse Polish Notation
#(4) calculate converted formula
#(5) print answer

index = 0
def getIndex():
    return index

def setIndex(number):
    return index+number


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
    nums = ''
    numflag = 0
    while index < len(line):
        if line[index].isdigit() or line[index] == '.':
            numflag = 1
            numlist.append(line[index]) #for two or more digit number and decimals
        elif line[index] == '+' or '-' or '*' or '/' or '(' or ')':
            if numflag ==1:
                nums = ''.join(numlist)
                numlist = [] #initialize
                tokens.append(nums) #push number
                numflag = 0 #initialize
                num = '' #initialize
            tokens.append(line[index]) #push operand
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        #if last token is a number
        if index ==len(line)-1 and line[index].isdigit():
            nums = ''.join(numlist)
            tokens.append(nums)
        index += 1
    return tokens


def test(line, expectedAnswer):
    actualAnswer = 0
    tokens = tokenize(line)
    tokens = ReversePolishNotation(tokens)
    if abs(float(evaluate(tokens)) - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, evaluate(tokens))


def runTest():
    print "==== Test started! ===="
    test("1", 1)
    test("1+2", 3)
    test("1.5+2", 3.5)
    test("10.5+25", 35.5)
    test("1.5+2.5", 4.0)
    test("2-1", 1)
    test("1-2", -1)
    test("2.5-1", 1.5)
    test("1.5-2.0", -0.5)
    test("1*2", 2)
    test("1.5*2", 3.0)
    test("2*1.5", 3.0)
    test("0.5*2.5", 1.25)
    test("2/1", 2)
    test("1/2", 0.5)
    test("2.5/1.25", 2)
    test("1.25/2.5", 0.5)
    test("(1.5+2)*2.4", 8.4)
    test("2.4*(1.5+2)", 8.4)
    test("(1.5+2.5)/(0.5*4)", 2.0)
    test("((1.5+2.5)/(0.5*4))*(33-22)", 22.0)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input() #(1) formula was read
    line = line.replace(' ', '') #delete spaces
    tokens = tokenize(line)  #(2) tokenize it
    tokens = ReversePolishNotation(tokens) #(3) convert its notation into Reverse Polish Notation
    answer = evaluate(tokens) #(4) calculate converted formula
    print "answer = %f\n" % answer #(5) print answer
    
