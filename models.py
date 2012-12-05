#!/usr/bin/python
# Models

class Process(object):
    """Represents a process."""
    def __init__(self, estimatedRuntime, priority, goal):
        self.estimatedRuntime = estimatedRuntime
        self.priority = priority
        self.goal = goal
        self.resourceInUse = None

    def ressourceRequired(self, t):
        """Determines what ressource would be needed for 
        time t based on the ressource probabilities."""
        pass

# Resources
class Resource(object):
    """Abstract class representing a ressource."""
    def __init__(self, name):
        super(Ressource, self).__init__()
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

class Network(object):
    """Represents the network resource."""
    def __init__(self, name):
        super(Disk, self).__init__(name)


# Scheduling polices
class Policy(object):
    """Abstract class representing a scheduling policy."""
    def __init__(self):
        super(Policy, self).__init__()

    def reorderQueue():
        """Reoders a queue of processes depending on the 
        policy"""
        raise NotImplementedError("Should implement queue reordering on a policy level.")

class FirstInFirstOut(Policy):
    """First in first out scheduling policy."""
    def __init__(self, arg):
        super(FirstInFirstOut, self).__init__()
        self.arg = arg

    def reorderQueue():
        """Reoders a queue of processes based on the FIFO policy."""
        pass
