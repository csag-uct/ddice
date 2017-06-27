from abc import ABCMeta, abstractmethod

from copy import copy

from dice.array import Dimension
from dice.array import Array
from dice.array import numpyArray


class Variable():
	"""
	A variable encapsulates an array with named dimensions and attributes
	"""

	def __init__(self, dimensions, dtype, name=None, attributes={}, dataset=None, data=None, storage=numpyArray):
		"""
		Create a new variable instance.  The dimensions parameter must be a tuple consisting of either
		instances of Dimension or 2-tuples of the form (name, size) or (name, size, fixed)

		>>> V = Variable((('x', 5),('y',3)), float, 'V')
		>>> print(V)
		<Variable: V [<Dimension: x (5) >, <Dimension: y (3) >]>
		>>> V.shape
		(5, 3)
		>>> V[:] = 42.0
		>>> V[2,1]
		[[ 42.]]
		>>> V.units = 'kg/m2/s'
		"""

		self._dimensions = []
		self._dtype = dtype
		self.name = name
		self.dataset = dataset

		# dimensions argument should be a tuple of either Dimension instances, or 2-tuples
		# in the form (name, size)
		for d in dimensions:			

			if type(d) == tuple:
				self._dimensions.append(Dimension(*d))

			elif type(d) == Dimension:
				self._dimensions.append(d)

			else:
				raise TypeError('{} is not a 2-tuple (name, size) or a Dimension instance'.format(d))

		if data:
			self._data = data
		else:
			self._data = storage(self.shape, dtype)

		self._attributes = {}

		if type(attributes) == dict:
			self._attributes = attributes
		else:
			return TypeError('attributes must be a dictionary')

	def __repr__(self):
		if self.name:
			return "<{}: {} {}>".format(self.__class__.__name__, self.name, repr(self._dimensions))
		else:
			return "<{}: {}>".format(self.__class__.__name__, repr(self._dimensions))


	def asjson(self, data=False):
		return {'dimensions':[], 'dtype':repr(self.dtype), 'attributes':self.attributes.copy()}


	@property
	def shape(self):
		return tuple([d.size for d in self._dimensions])

	@property
	def dtype(self):
		return self._dtype

	@property
	def dimensions(self):
		return tuple(self._dimensions)

	@property
	def attributes(self):
		return self._attributes

	def __setitem__(self, slices, values):
		self._data[slices] = values

	def __getitem__(self, slices):
		return self._data[slices]

