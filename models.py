import random
from policies import *

# Models
class Process(object):
    """Represents a process."""
    def __init__(self, pid, priority, goal, niceness, steps_remaining, name):
        self.pid = pid
        self.base_priority = priority
        self.priority = priority
        self.goal = goal
        self.steps_remaining = steps_remaining
        self.name = name
        self.execution_time = 0
        self.resourceInUse = None
        self.wait_time = 0
        self.allowed_time = 0

        #Behavior
        self.disk_probability = .05

        #metrics used by some policies
        self.usage = 0.0

        weights = [1024, 512, 256, 128, 64, 32, 16]
        if niceness > 6:
            self.niceness = 6
        self.weight = float(weights[niceness])

        #analytics information
        self.totalTimeInRunQueue = 0
        self.timesRun = 0    #this and the above determine avg time in run queue
        self.timeSinceStart = 0

    def execute(self):
        self.execution_time += 1
        self.steps_remaining -= 1

    def isDone(self):
        return self.steps_remaining == 0

    def needsDisk(self):
        return random.random() < self.disk_probability

    def diskWait(self, diskQueue):
        self.disk_time_remaining = random.randint(1, 5)
        diskQueue.insert(0, self)


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