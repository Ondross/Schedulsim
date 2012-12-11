import operator

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
        if len(processes_running) < processors:
            return True
        return False

    def get_information(self, dispatcher):
        pass

class FirstInFirstOut(Policy):
    """First In First Out scheduling policy."""

    def __init__(self):
        super(FirstInFirstOut, self).__init__()

    def reorderQueue(self, queue, processes_running):
        """Reorders a queue of processes based on the FIFO policy."""
        pass

    def get_information(self, dispatcher):
        pass

class RoundRobin(Policy):
    """Round robin scheduling policy."""

    def __init__(self, quantum = 1):
        super(RoundRobin, self).__init__()
        self.quantum = quantum

    def shouldAdvance(self, queue, processes_running, processors):
        if len(processes_running) < processors:
            return True
        for i in range(0,processors):
            if (processes_running[i].execution_time >= self.quantum):
                return True
        return False

    def get_information(self, dispatcher):
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
        return True

    def get_information(dispatcher):
        pass

class DecayUsage(Policy):
    """Decay Usage scheduling policy."""

    def __init__(self, quantum = 3):
        super(DecayUsage, self).__init__()
        self.quantum = quantum

    def setPriority(self, runQueue, waitQueues, processes_running):
        for process in runQueue:
            process.priority = process.base_priority - process.usage
        for process in processes_running:
            process.priority = process.base_priority - process.usage
        for queue in waitQueues:
            for process in queue:
                process.priority = process.base_priority - process.usage

    def shouldAdvance(self, queue, processes_running, processors):
        if len(processes_running) < processors:
            return True
        if len(queue) > 0:
            for process in processes_running:
                if process.execution_time > self.quantum:
                    return True
                else:
                    return False

    def reorderQueue(self, runQueue, process_running):
        runQueue.sort(key = operator.attrgetter('priority'))

    def calculate_usage(self, processes_running, waitQueues):
        for process in processes_running:
            if process.usage < process.base_priority:
                process.usage += 1.0
        for queue in waitQueues:
            for process in queue:
                process.usage = process.usage * 5/8


    def updateInformation(self, dispatcher):
        self.calculate_usage(dispatcher.processes_running, dispatcher.waitQueues)
        self.setPriority(dispatcher.runQueue, dispatcher.waitQueues, dispatcher.processes_running)