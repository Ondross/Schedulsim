#!/usr/bin/python
# Models

class Process(object):
	"""Represents a process."""
	def __init__(self, estimatedRuntime, priority, goal):
		self.estimatedRuntime = estimatedRuntime
		self.priority = priority
		self.goal = goal
		self.resourceInUse = None

# Resources
class Ressource(object):
	"""Abstract class representing a ressource."""
	def __init__(self, name):
		super(Ressource, self).__init__()
		self.name = name
		self.inUse = False

	def isInUse():
		return self.inUse

class Disk(Ressource):
	"""Represents the I/O ressource."""
	def __init__(self, name):
		super(Disk, self).__init__(name)

class Network(object):
	"""Represents the network ressource."""
	def __init__(self, name):
		super(Disk, self).__init__(name)


# Scheduling polices
class Policy(object):
	"""Abstract class representing a scheduling policy."""
	def __init__(self):
		super(Policy, self).__init__()

	def reorderQueue():
		"""Reoders a queue of processes depending on the 
		policy"""
        raise NotImplementedError("Should implement queue reordering on a policy level.")

class FirstInFirstOut(Policy):
	"""First in first out scheduling policy."""
	def __init__(self, arg):
		super(FirstInFirstOut, self).__init__()
		self.arg = arg
