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
		self.processors = 1

	def processFromInput(self):
		print("Press ENTER to step or type 'add' to add a process.")
		if (raw_input() == "add"):
			print("Name?")
			name = raw_input()
			print("Length?")
			length = int(raw_input())
			self.runQueue.insert(0, Process(1, 1, length, name))

	def printQueues(self):
		print("    RUN: ", end="")
		for process in self.runQueue:
			print(process.name, "(", process.steps_remaining, ")", sep="", end=", ")
		print()
		print("   WAIT: ", end="")
		for process in self.diskQueue:
			print(process.name, "(", process.steps_remaining, ")(", process.disk_time_remaining, ")", sep="", end=", ")
		print()
		print("RUNNING: ", end="")
		for process_running in self.processes_running:
			print(process_running.name, "(", process_running.steps_remaining, ")", sep="",)
		print()

	def step(self):
		"""Steps one unit of time."""

		#Add Processes
		self.processFromInput()

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

		self.printQueues()

		for i in range(0, self.processors):
			if i < len(self.processes_running) and self.processes_running[i]:
				if (random.random() < self.processes_running[i].disk_probability): #maybe we "randomly" need disk
					self.diskQueue.insert(0, self.processes_running[i])
					self.diskQueue[0].disk_time_remaining = random.randint(1, 10) #It has to wait on some "random" stuff
					#sorted as FIFO
					if len(self.runQueue) > 0:
						self.processes_running.insert(0, self.runQueue.pop())
					else:
						self.processes_running.pop(i)

		# Run one step of code
		for i in range(0, self.processors):
			if i < len(self.processes_running):
				self.processes_running[i].execution_time += 1
				self.processes_running[i].steps_remaining -= 1
				if self.processes_running[i].steps_remaining == 0:
					# Process finished
					if (len(self.runQueue) != 0):
						self.processes_running.insert(0, self.runQueue.pop())
					else: # No more processes to run
						self.processes_running.pop(i)

		#Deal with Disk Queue
		if len(self.diskQueue) > 0:
			if self.diskQueue[-1].disk_time_remaining == 0:
				self.runQueue.append(self.diskQueue.pop())
		if len(self.diskQueue) > 0:
			self.diskQueue[-1].disk_time_remaining -= 1

main = Dispatcher(FirstInFirstOut())

while (True):
	main.step()
