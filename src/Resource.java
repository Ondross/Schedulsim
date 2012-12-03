
public class Resource {
	String name;
	boolean activated;
	
	Resource (String _name) {
		if(_name.length() == 0) {
			_name = "Resource";
		}
		activated = true;
		name = _name;
	}
	
	public void activate() {
		activated = true;
	}
	
	public void deactivate() {
		activated = false;
	}
}
