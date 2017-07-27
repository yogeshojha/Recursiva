#--------------<Built-in Functions>--------------

add					= lambda x,y:x+y
subtract			= lambda x,y:x-y
multiply			= lambda x,y:x*y
divide				= lambda x,y:x/y
minusOne			= lambda x:x-1
square				= lambda x:x**2
rangeInclusive		= lambda x:[i for i in range(1,x+1)]
rangeExclusive		= lambda x:[i for i in range(1,x)]
compare				= lambda x,y:x==y
lesserThan			= lambda x,y:x<y
greaterThan			= lambda x,y:x>y
printer				= lambda x:print(x)

dictionary={
	'¬':{'func':minusOne,'args':1},
	'+':{'func':add,'args':2},
	'-':{'func':subtract,'args':2},
	'*':{'func':multiply,'args':2},
	'/':{'func':divide,'args':2},
	'R':{'func':rangeInclusive,'args':1},
	'r':{'func':rangeExclusive,'args':1},
	'S':{'func':square,'args':1},
	'<':{'func':lesserThan,'args':2},
	'>':{'func':greaterThan,'args':2},
	'=':{'func':compare,'args':2},
	'P':{'func':printer,'args':1}
}

#--------------<Built-in Functions/>-------------

def atomicInterpret(func,arguments):
	if len(arguments)==1:return dictionary[func]['func'](arguments[0])
	if len(arguments)==2:return dictionary[func]['func'](arguments[1],arguments[0])

def isIntLiteral(x):
	return x in[str(i) for i in range(10)]
 
def tokenizer(statement):
	tokens,i,j=[],0,0
	while i<len(statement):
		token=statement[i]
		if isIntLiteral(token):
			j=1
			while i+j<len(statement)and isIntLiteral(statement[i+j]):
				token+=statement[i+j];j+=1
			i+=j;tokens+=[int(token)]
		else:
			if token==' 'or token=='	':
				i+=1
			else:
				i+=1
				tokens+=[token]
	return tokens

def evaluate(expression):
	operatorStack=[]
	operandStack=[]
	for token in tokenizer(expression):
		if token in dictionary.keys():
			operatorStack.append(token)
		else:
			operandStack.append(token)
		if operatorStack and len(operandStack)>=dictionary[operatorStack[-1]]['args']:
			operands=[]
			argsLeft = dictionary[operatorStack[-1]]['args']
			while argsLeft:
				operands.append(operandStack.pop())
				argsLeft-=1
			operandStack.append(atomicInterpret(operatorStack.pop(),operands))
	while operatorStack:
		operator=operatorStack.pop()
		try:
			operand=operandStack.pop()
			operandStack.append(atomicInterpret(operator,operand))
		except:
			print("Too Few Operands")
			raise Exception
	result = operandStack.pop()
	if operandStack:
		print("Too many operands")
		raise Exception
	return result

def function_interpret(function_string,arguments):
	alphas=[i for i in function_string if 'a'<=i<='z']
	start_alpha=min(alphas)
	compiled = function_string
	for i,x in enumerate(arguments):
		compiled = compiled.replace(chr(ord(start_alpha)+i),x)
	return interpret(compiled) 
	
def interpret(statement):
	try:
		if '@' in statement:
			function_string = statement.split('@')[0]
			arguments_string = statement.split('@')[1]
			arguments = arguments_string.split()
			return function_interpret(function_string,arguments)
		if ':' in statement:
			condition=statement[:statement.find(':')]
			statements=statement[statement.find(':')+1:]
			statements_inverted=statements[::-1]
			if_statement=statements_inverted[statements_inverted.find('!')+1:][::-1]
			else_statement=statements_inverted[:statements_inverted.find('!')][::-1]
			if interpret(condition):return interpret(if_statement)
			if (else_statement):return interpret(else_statement)
			else:return None
		else:
			return evaluate(statement)
	except:
		raise Exception
