import operator

# Models

class Process(object):
    """Represents a process."""
    def __init__(self, priority, goal, steps_remaining, name):
        self.base_priority = priority
        self.priority = priority
        self.goal = goal
        self.steps_remaining = steps_remaining
        self.name = name
        self.execution_time = 0
        self.resourceInUse = None
        self.wait_time = 0

        #Behavior
        self.disk_probability = .10

        #metrics used by some policies
        self.usage = 0.0


    def resourceRequired(self, t):
        """Determines what resource would be needed for time t based on the 
        resource probabilities."""
        pass

# Resources
class Resource(object):
    """Abstract class representing a resource."""
    def __init__(self, name):
        super(Resource, self).__init__()
        self.name = name
        self.inUse = False
        self.waitQueue = None

    def isInUse(self):
        return self.inUse

    def waitingProcess(self):
        """Returns a process that has been waiting for the resource to become 
        available."""
        pass

class Disk(Resource):
    """Represents the I/O resource."""
    def __init__(self, name):
        super(Disk, self).__init__(name)

class Network(Resource):
    """Represents the network resource."""
    def __init__(self, name):
        super(Network, self).__init__(name)


# Scheduling polices
class Policy(object):
    """Abstract class representing a scheduling policy."""
    def __init__(self):
        super(Policy, self).__init__()

    def reorderQueue(self, running, process_running):
        """Reorders a queue of processes depending on the policy. Default
        implementation doesn't order the queue."""
        pass

    def shouldAdvance(self, queue, process_running):
        """Checks if a processor should kick out a process and
        advance the queue. Default implementation only advances when the process
        running finishes."""
        if (process_running == None):
            return True
        if (process_running.steps_remaining == 0):   #Isn't this case handled in dispatcher.step?
            return True
        return False

    def get_information(dispatcher):
        pass

class FirstInFirstOut(Policy):
    """First In First Out scheduling policy."""

    def __init__(self):
        super(FirstInFirstOut, self).__init__()

    def reorderQueue(self, queue, running):
        """Reorders a queue of processes based on the FIFO policy."""
        pass

    def get_information(dispatcher):
        pass

class RoundRobin(Policy):
    """Round robin scheduling policy."""

    def __init__(self, quantum = 1):
        super(RoundRobin, self).__init__()
        self.quantum = quantum

    def shouldAdvance(self, queue, process_running):
        if (process_running == None):
            return True
        if (process_running.execution_time >= self.quantum):
            return True
        return False

    def get_information(dispatcher):
        pass

class ShortestRemainingTime(Policy):
    """Shortest Remaining Time scheduling policy."""

    def __init__(self):
        super(ShortestRemainingTime, self).__init__()

    def reorderQueue(self, runQueue, process_running):
        """Reorders a queue of processes based on which processes have the least
        time remaining."""
        # We have to add the current process back in the queue
        #if (process_running != None):
         #   runQueue.append(process_running)  This is done in dispatcher.step()

        runQueue.sort(key = operator.attrgetter('steps_remaining'), reverse = True)

        #if (len(runQueue) != 0):
         #   process_running = runQueue.pop()     This is done in dispatcher.step()

    def shouldAdvance(self, queue, process_running):
        return True

    def get_information(dispatcher):
        pass

class DecayUsage(Policy):
    """Decay Usage scheduling policy."""

    def __init__(self, quantum = 3):
        super(DecayUsage, self).__init__()
        self.quantum = quantum

    def setPriority(self, runQueue, process_running):
        for process in runQueue:
            process.priority = process.base_priority - process.usage
        if process_running:
            process_running.priority = process_running.base_priority - process_running.usage

    def shouldAdvance(self, queue, process_running):
        if process_running == None:
            return True
        if len(queue) > 0:
            if process_running.execution_time > self.quantum:
                return True
            else:
                return False

    def reorderQueue(self, runQueue, process_running):
        runQueue.sort(key = operator.attrgetter('priority'))

    def calculate_usage(self, process_running, waitQueues):
        if process_running != None:
            if process_running.usage < process_running.base_priority:
                process_running.usage += 1
            for queue in waitQueues:
                for process in queue:
                    process.usage *= 5/8


    def get_information(self, dispatcher):
        self.calculate_usage(dispatcher.process_running, dispatcher.waitQueues)
        self.setPriority(dispatcher.runQueue, dispatcher.process_running)