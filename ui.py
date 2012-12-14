
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

        self.processesCreated = 0

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
        multithreadCheckButton.toggle()
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
            view.destroy()
        self.view.create_rectangle(150, 30, 700, 80, fill="white", outline="white")
        del self.policySettingControls[:]

        policy = self.policyString.get()

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

        if policy == "Decay Usage":
            # Setup controls
            label = Label(self.view, text="Quantum")
            label.place(x = 200, y = 38)
            self.policySettingControls.append(label)

            textBox = Entry(self.view, textvariable=quantum, width=3)
            textBox.place(x = 270, y = 36)
            textBox.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox)

            label1 = Label(self.view, text="Usage Increase")
            label1.place(x = 320, y = 38)
            self.policySettingControls.append(label1)

            textBox1 = Entry(self.view, textvariable=usageIncrease, width=3)
            textBox1.place(x = 420, y = 36)
            textBox1.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox1)

            label2 = Label(self.view, text="Usage Decrease")
            label2.place(x = 480, y = 38)
            self.policySettingControls.append(label2)

            textBox2 = Entry(self.view, textvariable=usageDecrease, width=5)
            textBox2.place(x = 590, y = 36)
            textBox2.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox2)

            self.dispatcher.policy = DecayUsage(int(quantum.get()), float(usageIncrease.get()), float(usageDecrease.get()))
            return

        if policy == "Weigthed Round Robin":
            # Setup controls
            label = Label(self.view, text="Minimum Quantum")
            label.place(x = 230, y = 38)
            self.policySettingControls.append(label)

            textBox = Entry(self.view, textvariable=quantum, width=3)
            textBox.place(x = 360, y = 36)
            textBox.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox)

            label1 = Label(self.view, text="Round Length")
            label1.place(x = 420, y = 38)
            self.policySettingControls.append(label1)

            textBox1 = Entry(self.view, textvariable=roundLength, width=3)
            textBox1.place(x = 520, y = 36)
            textBox1.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox1)

            self.dispatcher.policy = DecayUsage(int(quantum.get()), int(roundLength.get()))
            return

        if policy == "Proportional Decay Usage":
            # Setup controls
            label = Label(self.view, text="Min. Quantum")
            label.place(x = 235, y = 38)
            self.policySettingControls.append(label)

            textBox = Entry(self.view, textvariable=quantum, width=3)
            textBox.place(x = 335, y = 36)
            textBox.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox)

            label1 = Label(self.view, text="Round Length")
            label1.place(x = 380, y = 38)
            self.policySettingControls.append(label1)

            textBox1 = Entry(self.view, textvariable=roundLength, width=3)
            textBox1.place(x = 480, y = 36)
            textBox1.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox1)

            label1 = Label(self.view, text="+")
            label1.place(x = 530, y = 38)
            self.policySettingControls.append(label1)

            textBox1 = Entry(self.view, textvariable=usageIncrease, width=3)
            textBox1.place(x = 550, y = 36)
            textBox1.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox1)

            label2 = Label(self.view, text="-")
            label2.place(x = 600, y = 38)
            self.policySettingControls.append(label2)

            textBox2 = Entry(self.view, textvariable=usageDecrease, width=5)
            textBox2.place(x = 615, y = 36)
            textBox2.bind('<Return>', self.policyChanged)
            self.policySettingControls.append(textBox2)

            self.dispatcher.policy = DecayUsage(int(quantum.get()), int(roundLength.get()))
            return
    
    def addProcess(self):
        print "Process to add is: ", self.processToAddString.get()
        
        name = str(self.processToAddString.get())
        length = -1

        # (self, pid, priority, goal, niceness, steps_remaining, name):
        self.processesCreated = self.processesCreated + 1
        process = Process(self.processesCreated, 10.0, 1, 0, length, name)
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
            self.dispatcher.activateMultitasking()
        else:
            print "Multithreading deactivated"
            self.dispatcher.deactivateMultitasking()

class QueuedProcess(tk.Canvas):
    """View for processes inside a queue."""
    def __init__(self, parent, **options ):
        tk.Canvas.__init__( self, parent, **options )
        self.configure(highlightthickness=0)
        self.pack(side='top', fill='both', expand='yes')
        self.create_image(0, 0, image=bg1, anchor='nw')

    def setProcess(self, p):
        self.p = p
        self.create_text(14, 12, text=p.name + ' (' + str(p.pid) + ')', anchor='nw')

class RunningProcess(tk.Canvas):
    """View for processes inside a processor."""
    def __init__(self, parent, **options ):
        tk.Canvas.__init__( self, parent, **options )
        self.configure(highlightthickness=0)
        self.pack(side='top', fill='both', expand='yes')
        self.create_image(0, 0, image=runningProcessBg, anchor='nw')

    def setProcess(self, p):
        self.p = p
        self.create_text(56, 20, text=p.name + ' (' + str(p.pid) + ')', anchor='nw')
        
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
    usageIncrease = StringVar()
    usageIncrease.set("5")
    usageDecrease = StringVar()
    usageDecrease.set("0.625")

    roundLength = StringVar()
    roundLength.set("12")
    w = bg.width()
    h = bg.height()
    app = Controller(root)
    root.mainloop()