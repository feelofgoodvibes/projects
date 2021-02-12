package units;
import java.util.List;
import java.util.ArrayList;
import engine.Tools;

import map.*;

public class Droid{
	protected String name;
	protected Point position;

	protected int health;
	protected int damage;
	protected String type;

	protected int accuracy;
	protected char icon;

	protected Droid target;
	protected List<Point> path;

	public Droid(int x, int y, char icon, String name){
		this.position = new Point(x, y);
		this.health = 100;
		this.damage = 20;

		this.name = name;
		this.accuracy = 80;
		this.icon = icon;

		this.target = null;
		this.path = null;
		this.type = "SOLDIER";
	}

	public Point getPos() { return this.position; }
	public char getIcon() { return icon; }
	public String getName() { return name; }
	public List<Point> getPath() { return path; }
	public Droid getTarget() { return target; }
	public int getAccuracy() { return accuracy; }
	public int getHealth() { return health; }

	public void setPath(List<Point> newPath) { path = newPath; }
	public void setTarget(Droid enemy) { target = enemy; }
	public void setHealth(int hp) { health = hp; }
	public void setPos(Point pos) { position.x = pos.x; position.y = pos.y; }
	public void setName(String newname) { name = newname; }
	public void setIcon(char newicon) { icon = newicon; }

	public void configState(boolean state, List<String> map){
		if (state == true) 	icon = Tools.toUpper(icon);
		else       			icon = Tools.toLower(icon);
		map.set(position.y, Tools.setCharAt(map.get(position.y), position.x, icon));
	}

	public int recieveDamage(int damage){
		health -= damage;
		if (health <= 0) {
			target = null;
			health = 0;
		}
		return health;
	}

	public void attack(Droid enemy){
		if (Tools.tryRandom(getAccuracy())){
			int attackDamage = Tools.randomInt(damage - 10, damage + 10);
			enemy.recieveDamage((attackDamage >= 0) ? attackDamage : 0);
		}
	}

	public boolean isAlive(){
		if (this.health > 0) return true;
		else return false;
	}

	/** Просуватися по шляху
	* @param map Масив карти
	* @return true, якщо просування здійснене, false, якщо ні
	*/
	public boolean progressPath(List<String> map){
		if ((path == null) || (moveTo(path.get(0), map) == false)) return false;
		path.remove(0);
		if ((path.size()) == 0) path = null;
		return true;
	}

	/** Переміститися на точку
	* @param point Точка, на яку переміщуємось
	* @param map Масив карти
	* @return true, якщо переміщення здійснене, false, якщо ні
	*/
	public boolean moveTo(Point point, List<String> map){
		if (map.get(point.y).charAt(point.x) == ' ' || map.get(point.y).charAt(point.x) == '.'){
			map.set(position.y, Tools.setCharAt(map.get(position.y), position.x, ' '));
			position.x = point.x;
			position.y = point.y;
			map.set(point.y, Tools.setCharAt(map.get(point.y), point.x, icon));
			return true;
		}
		else return false;
	}

	/** Чи дроїд може вистрелити в іншого (чи між ними можна провести лінію)
	* @param enemy Дроїд, в якого стріляємо
	* @param map Масив карти
	* @return true, якщо можна вистрелити, false, якщо ні
	*/
	public boolean canShoot(Droid enemy, List<String> map){
		if (MapUtils.getLine(position, enemy.position, map) == null) return false;
		else return true;
	}

	public String toString(){
		String result = String.format("%7s %10s [%2d,%3d]   Health: %3d   Icon: %c", type, name, position.x, position.y, health, icon);
		if (target != null) result += "   Target: " + target.getName();
		return result;
	}
}
