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
		self.idleQueue = []
		self.diskQueue = []
		self.processes_running = []
		self.processors = 2
		self.waitQueues = [self.idleQueue, self.diskQueue]
		self.finishedProcesses = []
		self.rounds = 0
		self.pid = 0

		self.running = True

	def activateMultitasking(self):
		self.processors = 2

	def deactivateMultitasking(self):
		self.processors = 1
		if len(self.processes_running) > 1:
			self.runQueue.insert(0, self.processes_running.pop())

	def processFromInput(self):
		print("Press ENTER to step or type 'add' to add a process.")
		if (raw_input() == "add"):
			print("Name?")
			name = raw_input()
			print("Length?")
			length = int(raw_input())
			print("Niceness?")
			niceness = int(raw_input())
			self.runQueue.insert(0, Process(self.pid, 10.0, 1, niceness, length, name))
			self.pid += 1

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
			print(process_running.name, "(", process_running.steps_remaining, ")(", process_running.allowed_time, ") ", sep="", end=", ")
		print()


	def isProcessorFree(self):
		return len(self.processes_running) < self.processors

	def step(self):
		"""Steps one unit of time."""

		#Add Processes
		#self.processFromInput()

		# Advance Queue?
		self.policy.shouldAdvance(self.runQueue, self.processes_running, self.processors)

		# Update queues
		self.policy.reorderQueue(self.runQueue, self.processes_running)

		#self.printQueues()

		toRemove = []
		# Determine if a process has to wait
		for process in self.processes_running:                         #check each process
			if process.needsDisk():                                      #if we "randomly" need disk
				process.diskWait(self.diskQueue)                       #put it in the wait queue
				toRemove.append((process, self.processes_running.index(process)))   #mark it for removal

		for process in toRemove:
			if len(self.runQueue) > 0:
				self.processes_running[process[1]] = self.runQueue.pop() 
			else:
				self.processes_running.remove(process[0])
			
		# Run one step of code
		for process_running in self.processes_running:
			process_running.execute()
			if process_running.isDone():                          #If process is done
				self.finishedProcesses.append(process_running)    #add to finished processes
				self.processes_running.remove(process_running)    #remove from processor
				if (len(self.runQueue) != 0 and len(self.processes_running) < self.processors):
					self.processes_running.insert(0, self.runQueue.pop())

		self.policy.updateInformation(self)
		self.policy.updateRuntimes(self)
		self.rounds += 1   #Each round represents 10 microseconds

		#Deal with Disk Queue
		if len(self.diskQueue) > 0:
			if self.diskQueue[-1].disk_time_remaining == 0:
				self.runQueue.append(self.diskQueue.pop())
		if len(self.diskQueue) > 0:
			self.diskQueue[-1].disk_time_remaining -= 1

main = Dispatcher(ProportionalDecayUsage())#WeightedRoundRobin())#FirstInFirstOut())

