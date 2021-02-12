package map;

/** Клас, який описує точку
* @param x Координата Х
* @param y Координата Y
*/
public class Point{
	public int x;
	public int y;

	public Point(int x, int y){
		this.x = x;
		this.y = y;
	}

	public Point(Point p2){
		this.x = p2.x;
		this.y = p2.y;
	}

	public String toString(){ return String.format("(%d, %d)", this.x, this.y); }
	public boolean equals(Point p){
		if (this.x == p.x & this.y == p.y) return true;
		else return false;
	}
}