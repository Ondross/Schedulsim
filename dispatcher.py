from __future__ import print_function

from models import *

class Dispatcher(object):
	"""Dispatcher object takes care of keeping the wait
	and run queues updated."""
	def __init__(self, policy):
		super(Dispatcher, self).__init__()
		self.policy = policy
		self.runQueue = []
		self.timerQueue = []
		self.process_running = None

	def processFromImput(self):
		print("Insert a Process?")
		if (raw_input() == "yes"):
			print("What is it called?")
			name = raw_input()
			self.runQueue.insert(0, Process(1, 1, 1, 5, name))

	def printQueues(self):
		print("Run Queue: ", end="")
		for process in self.runQueue:
			print(process.name, end=", ")
		print()
		print("Wait Queue: ", end=", ")
		for process in self.timerQueue:
			print(process.name, end=", ")
		print()
		if (self.process_running):
			print(self.process_running.name, end=" is running")
		print("\n")

	def step(self):
		"""Steps one unit of time."""

		#Add Processes
		self.processFromImput()

		# Update queues
		self.policy.reorderQueue()

		# Update resources used

		# Run one step of code
		if (self.process_running):
			self.process_running.execution_time += 1
			self.process_running.steps_remaining -= 1
			if self.process_running.steps_remaining == 0:
				# Process finished
				if (len(self.runQueue) != 0):
					self.process_running = self.runQueue.pop()
				else: # No more processes to run
					self.process_running = None

		# Advance Queue?
		if (self.policy.shouldAdvance(self.runQueue, self.process_running) == True):
			if (self.process_running):
				self.process_running.execution_time = 0
				self.runQueue.insert(0, self.process_running)
			if (len(self.runQueue) != 0):
				self.process_running = self.runQueue.pop()

		self.printQueues()

main = Dispatcher(FirstInFirstOut())

while (True):
	main.step()
