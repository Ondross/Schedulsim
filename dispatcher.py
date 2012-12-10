from __future__ import print_function
import random

from models import *

class Dispatcher(object):
	"""Dispatcher object takes care of keeping the wait
	and run queues updated."""
	def __init__(self, policy):
		super(Dispatcher, self).__init__()
		self.policy = policy
		self.runQueue = []
		self.timerQueue = []
		self.diskQueue = []
		self.process_running = None
		self.waitQueues = [self.timerQueue, self.diskQueue]

	def processFromInput(self):
		print("Press ENTER to step or type 'add' to add a process.")
		if (raw_input() == "add"):
			print("Name?")
			name = raw_input()
			print("Length?")
			length = int(raw_input())
			self.runQueue.insert(0, Process(10.0, 1, length, name))

	def printQueues(self):
		print("    RUN: ", end="")
		for process in self.runQueue:
			print(process.name, "(", process.steps_remaining, ")(", process.priority, ") ", sep="", end=", ")
		print()
		print("   WAIT: ", end="")
		for process in self.diskQueue:
			print(process.name, "(", process.steps_remaining, ")(", process.disk_time_remaining, ")", sep="", end=", ")
		print()
		print("RUNNING: ", end="")
		if (self.process_running):
			print(self.process_running.name, "(", self.process_running.steps_remaining, ")(", self.process_running.priority, ") ", sep="",)
		print()

	def step(self):
		"""Steps one unit of time."""

		#Add Processes
		self.processFromInput()

		# Update resources used

		# Advance Queue?
		if (self.policy.shouldAdvance(self.runQueue, self.process_running)):
			if (self.process_running):
				self.process_running.execution_time = 0
				self.runQueue.insert(0, self.process_running)
				self.process_running = None

		self.policy.reorderQueue(self.runQueue, self.process_running)

		if (self.policy.shouldAdvance(self.runQueue, self.process_running)):
			if (len(self.runQueue) != 0):
				self.process_running = self.runQueue.pop()

		# Update queues
		self.policy.reorderQueue(self.runQueue, self.process_running)

		self.printQueues()

		if self.process_running:
			if (random.random() < self.process_running.disk_probability): #maybe we "randomly" need disk
				self.diskQueue.insert(0, self.process_running)
				self.diskQueue[0].disk_time_remaining = random.randint(1, 10) #It has to wait on some "random" stuff
				#sorted as FIFO
				if len(self.runQueue) > 0:
					self.process_running = self.runQueue.pop()
					self.resourceInUse = True
				else:
					self.process_running = None

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

		self.policy.get_information(self)

		#Deal with Disk Queue
		if len(self.diskQueue) > 0:
			if self.diskQueue[-1].disk_time_remaining == 0:
				self.runQueue.append(self.diskQueue.pop())
		if len(self.diskQueue) > 0:
			self.diskQueue[-1].disk_time_remaining -= 1

main = Dispatcher(DecayUsage())

while (True):
	main.step()
