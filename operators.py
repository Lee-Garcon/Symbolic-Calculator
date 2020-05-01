#For my symbolic calculator, every operation is represented as a class. This makes it easier to simplify.

import math #might come in handy
from class_helper import inherit_docstrings #method docstring inheritence

class Expression:
	'''Base class'''

	def evaluate(self):
		'''Returns the value of the expression.'''
		return 0

	def simplify(self):
		'''Condenses the expression so that operations can be performed much more simply. Different from evaluate().'''
		return self

@inherit_docstrings
class UnaryOperation(Expression):
	'''Operations that only takes one input'''
	def __init__(self, a):
		return a

@inherit_docstrings
class BinaryOperation(Expression):
	'''Operations that take two inputs'''
	def __init__(self, a, b):
		self.a = a
		self.b = b

@inherit_docstrings
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

@inherit_docstrings
class Addition(BinaryOperation):
	'''Addition operation (a + b)'''
	def evaluate(self):
		return self.a.evaluate() + self.b.evaluate()

	def simplify(self):
		temp = Addition(self.a.simplify(), self.b.simplify())
		#zero-addition
		if isinstance(temp.a, Constant):
			if temp.a.value == 0:
				return temp.b
		if isinstance(temp.b, Constant):
			if temp.b.value == 0:
				return temp.a
		#constant evaluation
		if isinstance(temp.a, Constant) and isinstance(temp.b, Constant):
			return Constant(temp.a.value + temp.b.value)
		#Logrithm Product Rule
		if isinstance(temp.a, Logrithm) and isinstance(temp.b, Logrithm):
			if temp.a.b == temp.b.b:
				return Logrithm(Multiplication(temp.a.a, temp.b.a), temp.a.b).simplify()
		return temp

@inherit_docstrings
class Subtraction(Addition):
	'''Subtraction operation (a - b)'''
	def evaluate(self):
		return self.a.evaluate() - self.b.evaluate()

	def simplify(self):
		temp = Subtraction(self.a.simplify(), self.b.simplify())
		#zero-subtraction
		if isinstance(temp.a, Constant):
			if temp.a.value == 0:
				return Negation(temp.b).simplify()
		if isinstance(temp.b, Constant):
			if temp.b.value == 0:
				return temp.a
		#constant evaluation
		if isinstance(temp.a, Constant) and isinstance(temp.b, Constant):
			return Constant(temp.a - temp.b)
		#Logrithm Quotient Rule
		if isinstance(temp.a, Logrithm) and isinstance(temp.b, Logrithm):
			if temp.a.b == temp.b.b:
				return Logrithm(Division(temp.a.a, temp.b.a), temp.a.b).simplify()
		return temp

@inherit_docstrings
class Negation(UnaryOperation):
	'''Negation operation (-a)'''
	def evaluate(self):
		return -self.a

	def simplify(self):
		#negative of a negative is a positive
		if isinstance(self.a, Negation):
			return self.a.a.simplify()
		#negative of zero is zero
		if isinstance(self.a, Constant):
			if self.a.value == 0:
				return self.a
		return Negation(self.a.simplify())

@inherit_docstrings
class Multiplication(BinaryOperation):
	'''Multiplication operation (a * b)'''
	def evaluate(self):
		return self.a.evaluate() * self.b.evaluate()

	def simplify(self):
		temp = Multiplication(self.a.simplify(), self.b.simplify())
		#Multiplication constant values
		if isinstance(temp.a, Constant) and isinstance(temp.b, Constant):
			return Constant(temp.a.value * temp.b.value)
		if isinstance(temp.a, Constant):
			if temp.a == 0:
				return Constant(0)
			if temp.a == 1:
				return temp.b
		if isinstance(temp.b, Constant):
			if temp.b == 0:
				return Constant(0)
			if temp.b == 1:
				return temp.a
		#Negatives
		if isinstance(temp.a, Negation) and isinstance(temp.b, Negation):
			return Multiplication(temp.a.a, temp.b.a)
		if isinstance(temp.a, Negation) and not isinstance(temp.b, Negation):
			return Negation(Multiplication(temp.a.a, temp.b))
		if not isinstance(temp.a, Negation) and isinstance(temp.b, Negation):
			return Negation(Multiplication(temp.a, temp.b.a))
		#Division
		if isinstance(temp.a, Division) and isinstance(temp.b, Division):
			return Division(Multiplication(temp.a.a, temp.b.a).simplify(), Multiplication(temp.a.b, temp.b.b).simplify()).simplify()
		if isinstance(temp.a, Division) and not isinstance(temp.b, Division):
			return Division(Multiplication(temp.a.a, temp.b).simplify(), temp.a.b).simplify()
		if not isinstance(temp.a, Division) and isinstance(temp.b, Division):
			return Division(Multiplication(temp.a, temp.b.a).simplify(), temp.b.b).simplify()
		#Logarithm Power Rule
		if isinstance(temp.a, Logarithm):
			return Logarithm(Power(temp.a.a, temp.b), temp.a.b).simplify()
		if isinstance(temp.b, Logarithm):
			return Logarithm(Power(temp.b.a, temp.a), temp.b.b).simplify()
		return temp

@inherit_docstrings
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
		temp = Division(self.a.simplify(), self.b.simplify())
		#Division constant values
		if isinstance(temp.a, Constant):
			if temp.a.value == 0:
				return Constant(0)
		if isinstance(temp.b, Constant):
			if temp.b.value == 0:
				return NotANumber()
			if temp.b.value == 1:
				return temp.a
		return temp

@inherit_docstrings
class Power(BinaryOperation):
	'''Power operator (a^b)'''
	def evaluate(self):
		return self.a.evaluate() ** self.b.evaluate()

	def simplify(self):
		temp = Power(self.a.simplify(), self.b.simplify())
		#Power constant values
		if isinstance(temp.a, Constant) and isinstance(temp.b, Constant):
			if temp.a.value == temp.b.value == 0:
				return NotANumber()
		if isinstance(temp.a, Constant):
			if temp.a.value == 0:
				return Constant(0)
			if temp.a.value == 1:
				return Constant(1)
		if isinstance(temp.b, Constant):
			if temp.b.value == 0:
				return Constant(1)
			if temp.b.value == 1:
				return temp.a
		return temp

@inherit_docstrings
class Root(Power):
	'''Root operator (b√a)'''
	def evaluate(self):
		return self.a.evaluate() ** (1/self.b.evaluate())

	def simplify(self):
		temp = Root(self.a.simplify(), self.b.simplify())
		#Root constants value
		if isinstance(temp.a, Constant) and isinstance(temp.b, Constant):
			if temp.a.value == temp.b.value == 0:
				return NotANumber()
		if isinstance(temp.a, Constant):
			if temp.a.value == 0:
				return Constant(0)
			if temp.a.value == 1:
				return Constant(1)
		if isinstance(temp.b, Constant):
			if temp.b.value == 0:
				return Constant(1)
			if temp.b.value == 1:
				return temp.a
		return temp

@inherit_docstrings
class Logrithm(BinaryOperation):
	'''Logrithm operator (log base b of a)'''
	def evaluate(self):
		return math.log(self.a.evaluate(), self.b.evaluate())

	def simplify(self):
		temp = Logrithm(self.a.simplify(), self.b.simplify())
		#Logrithm constants variable
		if isinstance(temp.a, Constant), isinstance(temp.b, Constant):
			if temp.a.value == temp.b.value:
				return Constant(1)
		if isinstance(temp.a, Constant):
			if temp.a.value == 1:
				return Constant(0)
			if temp.a.value <= 0:
				return NotANumber()
		if isinstance(temp.b, Constant):
			if temp.b.value <= 1:
				return NotANumber()
		return temp

@inherit_docstrings
class Variable(Expression):
	'''Variable representation. Cannot evaluate without inserting a value.'''
	def __init__(self):
		self.value = None

	def set_value(self, value):
		'''Set the value of the variable. Enables the use of evaluate().'''
		self.value = value

	def evaluate(self):
		if self.value != None:
			return self.value
		else:
			raise TypeError()

	def simplify(self):
		return self

@inherit_docstrings
class Constant(Expression):
	'''Constant representation. Represents a static number.'''
	def __init__(self, n):
		self.value = n

	def evaluate(self):
		return self.value

	def simplify(self):
		return self
