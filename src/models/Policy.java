package models;
import java.util.Queue;

public abstract class Policy {
	String name;
	
	public abstract void updateQueue(Queue<Process> queue);
}
