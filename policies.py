import operator
import matplotlib.pyplot as plt

# Scheduling polices
class Policy(object):
    """Abstract class representing a scheduling policy."""
    def __init__(self):
        super(Policy, self).__init__()

    def reorderQueue(self, running, processes_running):
        """Reorders a queue of processes depending on the policy. Default
        implementation doesn't order the queue."""
        pass

    def shouldAdvance(self, queue, processes_running, processors):
        """Checks if a processor should kick out a process and
        advance the queue. Default implementation only advances when the process
        running finishes."""
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again


    def updateInformation(self, dispatcher):
        pass

    def updateRuntimes(self, dispatcher):
        for process in dispatcher.runQueue:
            process.totalTimeInRunQueue += 10
            process.timeSinceStart += 10
        for queue in dispatcher.waitQueues:
            for process in queue:
                process.timeSinceStart += 10
        for process in dispatcher.processes_running:
            process.timeSinceStart += 10
            process.timeRun += 10

class FirstInFirstOut(Policy):
    """First In First Out scheduling policy."""

    def __init__(self):
        super(FirstInFirstOut, self).__init__()

    def reorderQueue(self, queue, processes_running):
        """Reorders a queue of processes based on the FIFO policy."""
        pass

    def updateInformation(self, dispatcher):
        pass

class RoundRobin(Policy):
    """Round robin scheduling policy."""

    def __init__(self, quantum = 50):
        super(RoundRobin, self).__init__()
        self.quantum = quantum

    def shouldAdvance(self, queue, processes_running, processors):
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again
            else:
                for i in range(len(processes_running)):
                    if processes_running[i].execution_time > self.quantum:
                        queue.insert(0, processes_running[i])
                        queue[0].execution_time = 0
                        processes_running[i] = queue.pop()
                        processes_running[i].timesRun += 1


    def updateInformation(self, dispatcher):
        pass

class ShortestRemainingTime(Policy):
    """Shortest Remaining Time scheduling policy."""

    def __init__(self):
        super(ShortestRemainingTime, self).__init__()

    def reorderQueue(self, runQueue, processes_running):
        """Reorders a queue of processes based on which processes have the least
        time remaining."""
        # We have to add the current process back in the queue
        #if (process_running != None):
         #   runQueue.append(process_running)  This is done in dispatcher.step()

        runQueue.sort(key = operator.attrgetter('steps_remaining'), reverse = True)

        #if (len(runQueue) != 0):
         #   process_running = runQueue.pop()     This is done in dispatcher.step()

    def shouldAdvance(self, queue, processes_running, processors):
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again
        if len(queue) > 0:    #if there is something to advance
            for i in range(len(processes_running)):
                if queue[-1].steps_remaining < processes_running[i].steps_remaining:
                    queue.insert(0, processes_running[i])
                    queue[0].execution_time = 0
                    processes_running[i] = queue.pop()
                    processes_running[i].timesRun += 1

    def updateInformation(self, dispatcher):
        pass

class DecayUsage(Policy):
    """Decay Usage scheduling policy."""

    def __init__(self, quantum = 3, usageIncrease = 1, usageDecrease = 5/8):
        super(DecayUsage, self).__init__()
        self.quantum = quantum
        self.usageIncrease = usageIncrease
        self.usageDecrease = usageDecrease

    def setPriority(self, runQueue, waitQueues, processes_running):
        for process in runQueue:
            process.priority = process.base_priority - process.usage
        for process in processes_running:
            process.priority = process.base_priority - process.usage
        for queue in waitQueues:
            for process in queue:
                process.priority = process.base_priority - process.usage

    def shouldAdvance(self, queue, processes_running, processors):
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again
            else:
                for i in range(len(processes_running)):
                    if processes_running[i].execution_time > self.quantum:
                        queue.insert(0, processes_running[i])
                        queue[0].execution_time = 0
                        processes_running[i] = queue.pop()
                        processes_running[i].timesRun += 1

    def reorderQueue(self, runQueue, process_running):
        runQueue.sort(key = operator.attrgetter('priority'))

    def calculate_usage(self, processes_running, waitQueues):
        for process in processes_running:
            if process.usage < process.base_priority:
                process.usage += self.usageIncrease
        for queue in waitQueues:
            for process in queue:
                process.usage = process.usage * self.usageDecrease


    def updateInformation(self, dispatcher):
        self.calculate_usage(dispatcher.processes_running, dispatcher.waitQueues)
        self.setPriority(dispatcher.runQueue, dispatcher.waitQueues, dispatcher.processes_running)


class WeightedRoundRobin(Policy):
    """Weighted Round Robin scheduling policy."""

    def __init__(self, minimumQuantum = 30.0, roundLength = 120.0):
        super(WeightedRoundRobin, self).__init__()
        self.minimumQuantum = minimumQuantum
        self.roundLength = roundLength

    def setRuntime(self, runQueue, processes_running, process):
        totalWeight = 0                                   #Divide up proportional share of CPU
        for process in runQueue:
            totalWeight += process.weight
        for process in processes_running:
            totalWeight += process.weight
        allowed_time = process.weight/totalWeight * self.roundLength
        if allowed_time < self.minimumQuantum:            #make sure runtime isn't crazy short
            allowed_time = self.minimumQuantum
        process.allowed_time = allowed_time        

    def shouldAdvance(self, queue, processes_running, processors):
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again
            else:
                for i in range(len(processes_running)):
                    if processes_running[i].execution_time >= processes_running[i].allowed_time:
                        queue.insert(0, processes_running[i])
                        queue[0].execution_time = 0
                        processes_running[i] = queue.pop()
                        processes_running[i].timesRun += 1
                        self.setRuntime(queue, processes_running, processes_running[i])
        return

    def reorderQueue(self, runQueue, process_running):
        pass

class ProportionalDecayUsage(Policy):
    """A unique scheduling algorithm that reorders the run queue based on usage, but choose time slices based on niceness"""

    def __init__(self, minimumQuantum = 30.0, roundLength = 120.0):
        super(ProportionalDecayUsage, self).__init__()
        self.minimumQuantum = minimumQuantum
        self.roundLength = roundLength
        self.usageIncrease = 1
        self.usageDecrease = 5/8

    def setPriority(self, runQueue, waitQueues, processes_running):
        for process in runQueue:
            process.priority = process.base_priority - process.usage
        for process in processes_running:
            process.priority = process.base_priority - process.usage
        for queue in waitQueues:
            for process in queue:
                process.priority = process.base_priority - process.usage

    def reorderQueue(self, runQueue, process_running):
        runQueue.sort(key = operator.attrgetter('priority'))

    def calculate_usage(self, processes_running, waitQueues):
        for process in processes_running:
            if process.usage < process.base_priority:
                process.usage += self.usageIncrease
        for queue in waitQueues:
            for process in queue:
                process.usage = process.usage * self.usageDecrease

    def setRuntime(self, runQueue, processes_running, process):
        totalWeight = 0.0                                  #Divide up proportional share of CPU
        for process in runQueue:
            totalWeight += process.weight
        for process in processes_running:
            totalWeight += process.weight
        allowed_time = process.weight/totalWeight * self.roundLength
        if allowed_time < self.minimumQuantum:            #make sure runtime isn't crazy short
              allowed_time = self.minimumQuantum
        process.allowed_time = allowed_time        

    def shouldAdvance(self, queue, processes_running, processors):
        if len(queue) > 0:    #if there is something to advance
            if len(processes_running) < processors:   #empty processor?
                processes_running.append(queue.pop())  #fill it up
                processes_running[-1].timesRun += 1
                self.shouldAdvance(queue,processes_running, processors)  #check again
            else:
                for i in range(len(processes_running)):
                    if processes_running[i].execution_time >= processes_running[i].allowed_time:
                        queue.insert(0, processes_running[i])
                        queue[0].execution_time = 0
                        processes_running[i] = queue.pop()
                        processes_running[i].timesRun += 1
                        self.setRuntime(queue, processes_running, processes_running[i])
        return

    def updateInformation(self, dispatcher):
        self.calculate_usage(dispatcher.processes_running, dispatcher.waitQueues)
        self.setPriority(dispatcher.runQueue, dispatcher.waitQueues, dispatcher.processes_running)
