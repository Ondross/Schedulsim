class Dispatcher(object):
	"""Dispatcher object takes care of keeping the wait
	and run queues updated."""
	def __init__(self, policy):
		super(Dispatcher, self).__init__()
		self.policy = policy
		self.runQueue = []

	def step(self):
		"""Steps one unit of time."""
		# Update queues
		# Update resources used
		pass
		