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
		self.processes_running = []
		self.processors = 2
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
		for process_running in self.processes_running:
			print(process_running.name, "(", process_running.steps_remaining, ")(", process_running.priority, ") ", sep="", end=", ")
		print()

	def runCode(self):
		pass

	def step(self):
		"""Steps one unit of time."""

		#Add Processes
		#self.processFromInput()

		# Update resources used

		# Advance Queue?
		for i in range(0, self.processors):
			if self.policy.shouldAdvance(self.runQueue, self.processes_running, self.processors):
				if i < len(self.processes_running):
					self.processes_running[i].execution_time = 0
					self.runQueue.append(self.processes_running[i])
					self.processes_running.pop(self.processes_running.index(self.processes_running[i]))

		self.policy.reorderQueue(self.runQueue, self.processes_running)

		for i in range(0, self.processors):
			if (self.policy.shouldAdvance(self.runQueue, self.processes_running, self.processors)):
				if (len(self.runQueue) != 0):
					self.processes_running.insert(i, self.runQueue.pop())

		# Update queues
		self.policy.reorderQueue(self.runQueue, self.processes_running)

		#self.printQueues()

		# Determine if the process has to wait
		for process_running in self.processes_running:
			if (random.random() < process_running.disk_probability): #maybe we "randomly" need disk
				process_running.disk_time_remaining = random.randint(1, 10)
				self.diskQueue.insert(0, process_running)
				if len(self.runQueue) > 0 and len(self.processes_running) < self.processors:
					self.processes_running.insert(0, self.runQueue.pop())
				else:
					self.processes_running.remove(process_running)

			
		# Run one step of code
		for process_running in self.processes_running:
			process_running.execution_time += 1
			process_running.steps_remaining -= 1
			if process_running.steps_remaining == 0:
				# Process finished
				self.processes_running.remove(process_running)
				if (len(self.runQueue) != 0 and len(self.processes_running) < self.processors):
					self.processes_running.insert(0, self.runQueue.pop())
				

		self.runCode()

		self.policy.get_information(self)

		#Deal with Disk Queue
		if len(self.diskQueue) > 0:
			if self.diskQueue[-1].disk_time_remaining == 0:
				self.runQueue.append(self.diskQueue.pop())
		if len(self.diskQueue) > 0:
			self.diskQueue[-1].disk_time_remaining -= 1

