#Inigo Beitia and Andrew Heine
#Software Systems Project, Fall 2012
#Schedulsim: a scheduling algorithm simulator and assessor

#This branch, "Grapher" analyzes the results of the schedulers and graphs them
#The branch, "tkinter" lets a user add processes and view the policy in a GUI

#Dispatcher.py is the controller of the application. It dispatches processes between
#processors and queues, and calls them methods that keep the process information up to date

from __future__ import print_function
import random
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab


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
		print("Press ENTER to step or type 'results' to view statistics.")
		if (raw_input() == "results"):
			self.printResults()
#			print("Name?")
#			name = raw_input()
#			#print("Length?")
#			length = -1 #int(raw_input())
#			print("Niceness?")
#			niceness = int(raw_input())
#			print("Impatience?")
#			impatience = float(raw_input())
#			if name == "quit":
#				self.printResults()
#			self.runQueue.insert(0, Process(self.pid, 10.0, impatience, niceness, length, name))
#			self.pid += 1

	def printQueues(self):
		print("    RUN: ", end="")
		for process in self.runQueue:
			print(process.name, "(", process.timesRun, ") ", sep="", end=", ")
		print()
		print("   WAIT: ", end="")
		for process in self.diskQueue:
			print(process.name,"(", process.timesRun, ")", sep="", end=", ")
		print()
		print("RUNNING: ", end="")
		for process_running in self.processes_running:
			print(process_running.name, "(", process_running.timesRun, ") ", sep="", end=", ")
		print()


	def isProcessorFree(self):
		return len(self.processes_running) < self.processors

	def printResults(self):
		context_switches = 0.0
		average_wait = 0.0
		greedies = 0.1
	 	wait_greedy = 0.0
	 	throughput_greedy = 0.0
	 	nices = 0.1
	 	nicegreedy = 0.1
	 	niceimpatient = 0.1
	 	nice_run = 0.1
	 	nice_life = 0.1
	 	wait_greedy_nice = 0.0
	 	throughput_greedy_nice = 0.0

	 	means = 0.1
	 	meangreedy = 0.1
	 	meanimpatient = 0.1
	 	mean_run = 0.1
	 	mean_life = 0.1
	 	wait_greedy_mean = 0.0
	 	throughput_greedy_mean = 0.0

	 	impatients = 0.1
	 	wait_impatient = 0.0
	 	throughput_impatient = 0.0
	 	niceimpatient = 0.1
	 	wait_impatient_nice = 0.0
	 	throughput_impatient_nice = 0.0
	 	mean_impatient = 0.1
	 	wait_impatient_mean = 0.0
	 	throughput_impatient_mean = 0.0

	 	processes = []
	 	processes += self.processes_running + self.finishedProcesses + self.runQueue
	 	for queue in self.waitQueues:
	 		processes += queue

	 	for p in processes:
	 		print(p.name)

	 	for process in processes:
	 		context_switches += process.timesRun
	 		throughput = process.timeRun / process.timeSinceStart
	 		print (666, process.timeRun, process.timeSinceStart)
	 		try:
	 			wait_time = process.totalTimeInRunQueue / process.timesRun
	 		except:
	 			wait_time = 0
	 		average_wait += wait_time

	 		if process.goal == "greedy":
	 			greedies += 1
	 			wait_greedy += wait_time
	 			throughput_greedy += throughput
	 			if process.niceness > 3:
	 				nices += 1
	 				nicegreedy += 1
	 				nice_run += process.timeRun
	 				nice_life += process.timeSinceStart
	 				wait_greedy_nice += wait_time
	 				throughput_greedy_nice += throughput
	 			else:
	 				means += 1
	 				meangreedy += 1
	 				mean_run += process.timeRun
	 				mean_life += process.timeSinceStart
	 				wait_greedy_mean += wait_time
	 				throughput_greedy_mean += throughput

	 		else:
	 			impatients += 1
	 			wait_impatient += wait_time
	 			throughput_impatient += throughput
	 			if process.niceness > 3:
	 				nices += 1
	 				niceimpatient += 1
	 				nice_run += process.timeRun
	 				nice_life += process.timeSinceStart
	 				wait_impatient_nice += wait_time
	 				throughput_impatient_nice += throughput
	 			else:
	 				means += 1
	 				meanimpatient += 1
	 				mean_run += process.timeRun
	 				mean_life += process.timeSinceStart
	 				wait_impatient_mean += wait_time
	 				throughput_impatient_mean += throughput

		

	 	average_wait = average_wait / (means + nices)

	 	print("check")
	 	print (means + nices)
	 	print (impatients + greedies)
	 	print (len(processes))

	 	wait_impatient = wait_impatient / impatients
	 	wait_greedy = wait_greedy / greedies
	 	throughput_impatient = throughput_impatient / impatients
	 	thoughput_greedy = throughput_greedy / greedies

	 	wait_impatient_nice = wait_impatient_nice / niceimpatient
	 	wait_greedy_nice = wait_greedy_nice / nicegreedy
	 	throughput_impatient_nice = throughput_impatient_nice / niceimpatient
	 	throughput_greedy_nice = throughput_greedy_nice / nicegreedy

	 	wait_impatient_mean = wait_impatient_mean / meanimpatient
	 	wait_greedy_mean = wait_greedy_mean / meangreedy
	 	throughput_impatient_mean = throughput_impatient_mean / meanimpatient
	 	throughput_greedy_mean = throughput_greedy_mean / meangreedy

	 	print("Time Running: ", self.rounds * 10, " microseconds")

	 	print("Nice Processes: ", nices)
	 	print("Mean Processes: ", means)
	 	print("Impatient Processes: ", impatients)
	 	print("Greedy Processes: ", greedies)
	 	print("Mean/Nice running: ", mean_run/nice_run)
	 	print("Mean/Nice lifetime: ", mean_life/nice_life)
	 	print("Average Wait Time: ", average_wait, " us")
	 	print("Context Switches: ", context_switches)
	 	print("\n")
	 	print("Avg Wait Time, Impatient: ", wait_impatient, " us")
	 	print("Avg Wait Time, Greedy: ", wait_greedy, " us")
	 	print("Percent Time Running, Impatient: ", throughput_impatient * 100)
	 	print("Percent Time Running, Greedy: ", throughput_greedy * 100)
	 	print("\n")
	 	print("Avg Wait Time, Nice-Impatient: ", wait_impatient_nice, " us")
	 	print("Avg Wait Time, Nice-Greedy: ", wait_greedy_nice, " us")
	 	print("Percent Time Running, Nice-Impatient: ", throughput_impatient_nice * 100)
	 	print("Percent Time Running, Nice-Greedy: ", throughput_greedy_nice * 100)
	 	print("Avg Wait Time, Mean-Impatient: ", wait_impatient_mean, " us")
	 	print("Avg Wait Time, Mean-Greedy: ", wait_greedy_mean, " us")
	 	print("Percent Time Running, Mean-Impatient: ", throughput_impatient_mean * 100)
	 	print("Percent Time Running, Mean-Greedy: ", throughput_greedy_mean * 100)

	 	plt.figure(1)
	 	chart = plt.bar([0, 1, 2, 3],[wait_impatient_mean, wait_greedy_mean, wait_impatient_nice, wait_greedy_nice])

	 	plt.xlabel('Category')
	 	plt.ylabel('Average Wait Time (us)')
	 	plt.title("Average Waiting Time of Processes")
	 	plt.axis([0, 4, 0, 100])
	 	plt.grid(True)
	 	group_labels = ["mean/impatient", "mean/greedy", "nice/impatient", "nice,greedy"]
	 	plt.xticks([.5, 1.5, 2.5, 3.5], group_labels)

	 	pylab.ion()
	 	plt.show()

	 	plt.figure(2)
	 	chart = plt.bar([0, 1, 2, 3],[100 * throughput_impatient_mean, 100 * throughput_greedy_mean, 100* throughput_impatient_nice, 100 * throughput_greedy_nice])

	 	plt.xlabel('Category')
	 	plt.ylabel('Runtime/Lifetime')
	 	plt.title("Runtime/Lifetime Ratio")
	 	plt.axis([0, 4, 0, 100])
	 	plt.grid(True)
	 	group_labels = ["mean/impatient", "mean/greedy", "nice/impatient", "nice,greedy"]
	 	plt.xticks([.5, 1.5, 2.5, 3.5], group_labels)

	 	plt.show()


	def step(self):
		"""Steps one unit of time."""
		#Add Processes
		self.processFromInput()

		# Advance Queue?
		self.policy.shouldAdvance(self.runQueue, self.processes_running, self.processors)

		# Update queues
		self.policy.reorderQueue(self.runQueue, self.processes_running)

		self.printQueues()

		toRemove = []
		# Determine if a process has to wait for hard disk
		for process in self.processes_running:                         #check each process
			if process.needsDisk():                                      #if we "randomly" need disk
				process.diskWait(self.diskQueue)                       #put it in the wait queue
				toRemove.append((process, self.processes_running.index(process)))   #mark it for removal

		for process in toRemove:
			if len(self.runQueue) > 0:
				self.processes_running[process[1]] = self.runQueue.pop()
				self.processes_running[process[1]].timesRun += 1 
			else:
				self.processes_running.remove(process[0])

		toRemove = []

		# Determine if a process has to wait for user input
		for process in self.processes_running:                         #check each process
			if process.needsinput():                                      #if we "randomly" need disk
				process.inputWait(self.idleQueue)                       #put it in the wait queue
				toRemove.append((process, self.processes_running.index(process)))   #mark it for removal

		for process in toRemove:
			if len(self.runQueue) > 0:
				self.processes_running[process[1]] = self.runQueue.pop()
				self.processes_running[process[1]].timesRun += 1 
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
					self.processes_running[0].timesRun += 1

		self.policy.updateInformation(self)
		self.policy.updateRuntimes(self)
		self.rounds += 1   #Each round represents 10 microseconds

		#Deal with Disk Queue
		if len(self.diskQueue) > 0:
			if self.diskQueue[-1].disk_time_remaining == 0:
				self.runQueue.append(self.diskQueue.pop())
		if len(self.diskQueue) > 0:
			self.diskQueue[-1].disk_time_remaining -= 1

		#Deal with input Queue
		if len(self.idleQueue) > 0:
			if self.idleQueue[-1].idle_time_remaining <= 0:
				self.runQueue.append(self.idleQueue.pop())
		if len(self.idleQueue) > 0:
			for process in self.idleQueue:
				process.idle_time_remaining -= 1

main = Dispatcher(ProportionalDecayUsage())#WeightedRoundRobin())

#make eight dummy processes for testing (user input is disabled in this version)
#each falls into one of the four combinations of niceness/usage
main.runQueue.insert(0, Process(0, 10.0, .15, 0, -1, "meanimp"))
main.runQueue.insert(0, Process(1, 10.0, 0, 0, -1, "meangreed"))
main.runQueue.insert(0, Process(2, 10.0, .15, 6, -1, "niceimp"))
main.runQueue.insert(0, Process(3, 10.0, 0, 6, -1, "nicegreed"))
main.runQueue.insert(0, Process(4, 10.0, .15, 0, -1, "meanimp2"))
main.runQueue.insert(0, Process(5, 10.0, 0, 0, -1, "meangreed2"))
main.runQueue.insert(0, Process(6, 10.0, .15, 6, -1, "niceimp2"))
main.runQueue.insert(0, Process(7, 10.0, 0, 6, -1, "nicegreed2"))

main.pid = 8

while (True):
	main.step()