#For my symbolic calculator, every operation is represented as a class. This makes it easier to simplify.

import math #might come in handy

class Expression:
	'''Base class'''

	def evaluate(self):
		return 0

	def simplify(self):
		return self

class UnaryOperation(Expression):
	'''Operations that only takes one input'''
	def __init__(self, a):
		return a

class BinaryOperation(Expression):
	'''Operations that take two inputs'''
	def __init__(self, a, b):
		self.a = a
		self.b = b

class TrinaryOperation(Expression):
	'''Operations that take three inputs'''
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

class NotANumber(Expression):
	'''NaN representation'''
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs

class Addition(BinaryOperation):
	'''Addition operation (a + b)'''
	def evaluate(self):
		return self.a.evaluate() + self.b.evaluate()

	def simplify(self):
		#zero-addition
		if self.a.evaluate() == self.b.evaluate() == 0:
			return Constant(0)
		if self.a.evaluate() == 0:
			return self.b.simplify()
		if self.b.evaluate() == 0:
			return self.a.simplify()
		#constant evaluation
		if isinstance(self.a, Constant) and isinstance(self.b, Constant):
			return Constant(self.evaluate())
		return self

class Subtraction(Addition):
	'''Subtraction operation (a - b)'''
	def evaluate(self):
		return self.a.evaluate() - self.b.evaluate()

	def simplify(self):
		#zero-subtraction
		if self.a.evaluate() == self.b.evaluate() == 0:
			return Constant(0)
		if self.a.evaluate() == 0:
			return Negation(self.b.simplify())
		if self.b.evaluate() == 0:
			return self.a.simplify()
		#constant evaluation
		if isinstance(self.a, Constant) and isinstance(self.b, Constant):
			return Constant(self.evaluate())
		return self

class Negation(UnaryOperation):
	'''Negation operation (-a)'''
	def evaluate(self):
		return -self.a

	def simplify(self):
		if isinstance(self.a, Negation): #Negative of a Negative is a positive
			return self.a.a.simplify()
		return Negation(self.a.simplify())

class Multiplication(BinaryOperation):
	'''Multiplication operation (a * b)'''
	def evaluate(self):
		return self.a.evaluate() * self.b.evaluate()

	def simplify(self):
		#Multiplication constant values
		if self.a.evaluate() == 0 or self.b.evaluate() == 0:
			return Constant(0)
		if self.a.evaluate() == self.b.evaluate() == 1:
			return Constant(1)
		if self.a.evaluate() == 1:
			return self.b.simplify()
		if self.b.evaluate() == 1:
			return self.a.simplify()
		#Negatives
		if isinstance(self.a, Negation) and isinstance(self.b, Negation):
			return Multiplication(self.a.n, self.b.n).simplify()
		if isinstance(self.a, Negation) and not isinstance(self.b, Negation):
			return Negation(Multiplication(self.a.n, self.b)).simplify()
		if not isinstance(self.a, Negation) and isinstance(self.b, Negation):
			return Negation(Multiplication(self.a, self.b.n).simplify())
		#Division
		if isinstance(self.a, Division) and isinstance(self.b, Division):
			return Division(Multiplication(self.a.a, self.b.a).simplify(), Multiplication(self.a.b, self.b.b).simplify()).simplify()
		if isinstance(self.a, Division) and not isinstance(self.b, Division):
			return Division(Multiplication(self.a.a, self.b), self.a.b)
		if (not isinstance(self.a, Division)) and isinstance(self.b, Division):
			return Division(Multiplication(self.a, self.b.a), self.b.b)

		return self

class Division(Multiplication):
	'''Division operator (a/b)'''
	def evaluate(self):
		denom = self.b.evaluate()
		if denom != 0:
			return self.a.evaluate() / denom
		else:
			return NotANumber(self)

	def simplify(self):
		#TODO: Add division simplification rules
		pass

class Power(BinaryOperation):
	'''Power operator (a^b)'''
	def evaluate(self):
		return self.a.evaluate() ** self.b.evaluate()

	def simplify(self):
		#TODO: Add power simplification rules
		pass

class Root(Power):
	'''Root operator (b√a)'''
	def evaluate(self):
		return self.a.evaluate() ** (1/self.b.evaluate())

	def simplify(self):
		#TODO: Add root simplification rules
		pass

class Logrithm(BinaryOperation):
	'''Logrithm operator (log base b of a)'''
	def evaluate(self):
		return math.log(self.a.evaluate(), self.b.evaluate())

	def simplify(self):
		#TODO: Add logrithm simplification rules
		pass

class Variable(Expression):
	'''Variable representation. Cannot evaluate without inserting a value.'''
	def __init__(self):
		self.value = None

	def set_value(self, value):
		self.value = value

	def evaluate(self):
		if self.value != None:
			return self.value
		else:
			raise TypeError()

	def simplify(self):
		return self

class Constant(Expression):
	'''Constant representation. Represents a static number.'''
	def __init__(self, n):
		self.value = n

	def evaluate(self):
		return self.value

	def simplify(self):
		return self
