
from Tkinter import *
from dispatcher import *
from models import *
import Tkinter as tk       

class Controller:
    def __init__(self, root):
        # Dispatcher initialization
        self.dispatcher = Dispatcher(FirstInFirstOut())
        self.runQueueViews = []
        self.diskQueueViews = []
        self.imputQueueViews = []
        self.processorViews = []
        self.policySettingControls = []

        root.resizable(width=False, height=False)
        root.title('Schedulsim')
        root.geometry("%dx%d+0+0" % (w, h))
        self.view = tk.Canvas(root, width=w, height=h)
        self.view.pack(side='top', fill='both', expand='yes')
        self.view.create_image(-5, -5, image=bg, anchor='nw')
        self.view.configure(highlightthickness=0)
        
        # Scheduling Policy
        self.policyString = StringVar(self.view)
        self.policyString.set("First In First Out") # initial value
        option = OptionMenu(self.view, self.policyString, "First In First Out", "Shortest Job First", "Round Robin", "Decay Usage", "Weigthed Round Robin", "Proportional Decay Usage", command=self.policyChanged)
        option.place(x=10, y=35)

        # Add process
        self.view.create_text(70, 120, text='ADD A PROCESS')

        self.processToAddString = StringVar(self.view)
        self.processToAddString.set("Firefox") # initial value
        option = OptionMenu(self.view, self.processToAddString, "Firefox", "Disk Defrag", "IM Client", "Photoshop", "Video game")
        option.place(x=10, y=140)
        addProcessButton = Button(self.view, text="Add Process", command=self.addProcess)
        addProcessButton.place(x=13, y=170)

        # Playback controls
        stepButton = Button(self.view, text="STEP", command=self.step)
        stepButton.place(x=13, y=200)

        # Processors
        self.view.create_text(270, 120, text='RUNNING', font='Arial')

        # Multithreading?
        self.multithreadingOn = IntVar()
        multithreadCheckButton = Checkbutton(self.view, text="Multithreading", variable=self.multithreadingOn, command=self.multithreadingCheckChanged)
        multithreadCheckButton.place(x=470, y=110)

        # Processors
        
        # Queues
        self.view.create_text(82, 260, text='DISK WAITING QUEUE')
        self.view.create_text(330, 260, text='USER INPUT WAITING QUEUE')
        self.view.create_text(500, 260, text='RUN QUEUE')

        self.redrawQueueBg()

    def redrawQueueBg(self):
        self.view.create_rectangle(212, 565, 7, 277, fill="white")
        self.view.create_rectangle(435, 565, 240, 277, fill="white")
        self.view.create_rectangle(672, 565, 467, 277, fill="white")

    def step(self):
        self.dispatcher.step()
        self.dispatcher.printQueues()

        self.prepareRunQueueViews()
        self.prepareDiskQueueViews()

        self.redrawQueueBg()

        self.drawQueues()

        self.prepareProcessorViews()

        self.drawProcessorViews()

    def prepareProcessorViews(self):
        # Delete views from screen
        for view in self.processorViews:
            view.place_forget()
            view.delete()
        del self.processorViews[:]
        # Generate views
        for process in self.dispatcher.processes_running:
            processView = RunningProcess(root, width=200, height=90)
            processView.setProcess(process)
            self.processorViews.append(processView)

    def drawProcessorViews(self):
        for i in range(0, len(self.processorViews)):
            view = self.processorViews[i]
            view.place(x=236 + (i*231), y=137)

    def prepareRunQueueViews(self):
        # Delete views from screen
        for view in self.runQueueViews:
            view.place_forget()
            view.delete()
        del self.runQueueViews[:]
        # Generate views
        for process in reversed(self.dispatcher.runQueue):
            processView = QueuedProcess(root, width=200, height=41)
            processView.setProcess(process)
            self.runQueueViews.append(processView)

    def prepareDiskQueueViews(self):
        # Delete views from screen
        for view in self.diskQueueViews:
            view.place_forget()
            view.delete()
        del self.diskQueueViews[:]
        # Generate views
        for process in reversed(self.dispatcher.diskQueue):
            processView = QueuedProcess(root, width=200, height=41)
            processView.setProcess(process)
            self.diskQueueViews.append(processView)

    def policyChanged(self, event):
        for view in self.policySettingControls:
            view.place_forget()
        del self.policySettingControls[:]

        policy = self.policyString.get()
        print policy
        #"Decay Usage", "Weigthed Round Robin", "Proportional Decay Usage"
        if policy == "First In First Out":
            self.dispatcher.policy = FirstInFirstOut()
            return

        if policy == "Round Robin":
            # Setup controls
            label = Label(self.view, text="Quantum")
            label.place(x = 200, y = 38)
            self.policySettingControls.append(label)

            textBox = Entry(self.view, textvariable=quantum, width=3)
            textBox.place(x = 270, y = 36)
            textBox.bind('<Return>', self.policyChanged)
            self.dispatcher.policy = RoundRobin(int(quantum.get()))
            return
    
    def addProcess(self):
        print "Process to add is: ", self.processToAddString.get()
        
        name = str(self.processToAddString.get())
        length = -1
        # TODO: get some data
        process = Process(10.0, 0,1,0, length, name)
        self.dispatcher.runQueue.insert(0, process)

        self.prepareRunQueueViews()
        self.drawRunQueue()

    def drawQueues(self):
        self.drawRunQueue()
        self.drawDiskQueue()
        self.drawImputQueue()

    def drawRunQueue(self):
        for i in range(0, len(self.runQueueViews)):
            view = self.runQueueViews[i]
            view.place(x=470 , y=280+ (i*40))

    def drawDiskQueue(self):
        for i in range(0, len(self.diskQueueViews)):
            view = self.diskQueueViews[i]
            view.place(x=10 , y=280+ (i*40))

    def drawImputQueue(self):
        for i in range(0, len(self.imputQueueViews)):
            view = self.imputQueueViews[i]
            view.place(x=270 , y=280+ (i*40))

    def multithreadingCheckChanged(self):
        if self.multithreadingOn.get():
            print "Multithreading activated"
            self.dispatcher.processors = 2
        else:
            print "Multithreading deactivated"
            self.dispatcher.processors = 1
        # TODO: make changes to dipatcher

class QueuedProcess(tk.Canvas):
    """View for processes inside a queue."""
    def __init__(self, parent, **options ):
        tk.Canvas.__init__( self, parent, **options )
        self.configure(highlightthickness=0)
        self.pack(side='top', fill='both', expand='yes')
        self.create_image(0, 0, image=bg1, anchor='nw')

    def setProcess(self, p):
        self.p = p
        self.create_text(14, 12, text=p.name, anchor='nw')

class RunningProcess(tk.Canvas):
    """View for processes inside a processor."""
    def __init__(self, parent, **options ):
        tk.Canvas.__init__( self, parent, **options )
        self.configure(highlightthickness=0)
        self.pack(side='top', fill='both', expand='yes')
        self.create_image(0, 0, image=runningProcessBg, anchor='nw')

    def setProcess(self, p):
        self.p = p
        self.create_text(56, 20, text=p.name)
        
class QueueWidget(tk.Frame):
   def __init__( self, parent, **options ):
      tk.Frame.__init__( self, parent, **options )

      self._list = tk.Canvas(self)
      self._scrollbar = tk.Scrollbar( self )

      self._list.pack( side=tk.LEFT )
      self._scrollbar.pack( side=tk.LEFT )

if __name__ == '__main__':
    root = tk.Tk()
    #root.withdraw()
    bg1 = PhotoImage(file="waitingProcessQueue.gif")
    runningProcessBg = PhotoImage(file="runningProcess.gif")
    bg = PhotoImage(file="windowbg.gif")
    quantum = StringVar()
    quantum.set("10")
    w = bg.width()
    h = bg.height()
    app = Controller(root)
    root.mainloop()