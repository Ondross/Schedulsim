#!/usr/bin/python
# Models

class Process(object):
    """Represents a process."""
    def __init__(self, estimatedRuntime, priority, goal, steps, name):
        self.estimatedRuntime = estimatedRuntime
        self.priority = priority
        self.goal = goal
        self.steps_remaining = steps
        self.name = name
        self.execution_time = 0
        self.resourceInUse = None


    def resourceRequired(self, t):
        """Determines what resource would be needed for 
        time t based on the resource probabilities."""
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
        """Returns a process that has been waiting for
        the resource to become available."""
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

    def reorderQueue(self):
        """Reorders a queue of processes depending on the 
        policy"""
        raise NotImplementedError("Should implement queue reordering on a policy level.")

class FirstInFirstOut(Policy):
    """First in first out scheduling policy."""
    def __init__(self):
        super(FirstInFirstOut, self).__init__()

    def reorderQueue(self):
        """Reorders a queue of processes based on the FIFO policy."""
        pass

    def shouldAdvance(self, queue, process_running):
        """Checks if a processor should kick out a process and
        advance the queue"""
        if (process_running == None):
            return True
        if (process_running.execution_time > 5):
            return True
        else:
            return False