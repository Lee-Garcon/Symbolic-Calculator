'''Code from stackoverflow: https://stackoverflow.com/questions/17393176/python-3-method-docstring-inheritance-without-breaking-decorators-or-violating'''

from inspect import getmembers, isfunction

def inherit_docstrings(cls):
	for name, func in getmembers(cls, isfunction):
		if func.__doc__: continue
		for parent in cls.__mro__[1:]:
			if hasattr(parent, name):
				func.__doc__ = getattr(parent, name).__doc__
	return cls
