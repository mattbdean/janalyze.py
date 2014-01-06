// default package for simplicity's sake

public abstract class SimpleAbsClass {
	/** Single line documentation */
	private int x;
	/**
	 * Multi-line documentation
	 */
	private int y;
	
	public SimpleAbsClass(int x, int y) {
		// Comment for the sake of having one
		this.x = x;
		this.y = y;
	}

	public int add() {
		return add(x, y);
	}

	public abstract int add(int x, int y);
}
