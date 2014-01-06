// default package for simplicity's sake

public class SimpleClass extends SimpleAbsClass {
	/**
	 * Some documentation on this field
	 */
	private String myString;
	
	public SimpleClass(int x, int y) {
		super(x, y);
	}

	@Override
	public int add(int x, int y) {
		return x + y;
	}
	

	public static void main(String[] args) {
		// Instantiate a new SimpleClass
		SimpleClass sc = new SimpleClass(5, 12);
		/* Print the result */
		System.out.println(sc.add());
		/* Some strange */ /* comment combo */
	}
}
