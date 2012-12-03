package models;
import java.util.Queue;

public class Scheduler {
	Queue<Process> runQueue;
	Queue<Process> waitQueue;
	Policy policy;
	boolean playing;
	
	public void addProcess(Process process) {
		
	}
	
	public void step() {
		
	}

	public void play() {
		playing = true;
		
		while(playing) {
			step();
		}
	}
	
	public void stop() {
		playing = false;
	}
}
