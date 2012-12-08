import operator

# Models

class Process(object):
    """Represents a process."""
    def __init__(self, priority, goal, steps_remaining, name):
        self.priority = priority
        self.goal = goal
        self.steps_remaining = steps_remaining
        self.name = name
        self.execution_time = 0
        self.resourceInUse = None


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
        if (process_running.steps_remaining == 0):
            return True
        return False

class FirstInFirstOut(Policy):
    """First In First Out scheduling policy."""

    def __init__(self):
        super(FirstInFirstOut, self).__init__()

    def reorderQueue(self, queue, running):
        """Reorders a queue of processes based on the FIFO policy."""
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

class ShortestRemainingTime(Policy):
    """Shortest Remaining Time scheduling policy."""

    def __init__(self):
        super(ShortestRemainingTime, self).__init__()

    def reorderQueue(self, runQueue, process_running):
        """Reorders a queue of processes based on which processes have the least
        time remaining."""
        # We have to add the current process back in the queue
        if (process_running != None):
            runQueue.append(process_running)

        runQueue.sort(key = operator.attrgetter('steps_remaining'))

        if (len(runQueue) != 0):
            process_running = runQueue.pop()

    def shouldAdvance(self, queue, process_running):
        return True
