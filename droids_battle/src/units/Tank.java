package units;
import engine.Tools;

public class Tank extends Droid{
	public Tank(int x, int y, char icon, String name){
		super(x, y, icon, name);
		this.health = 150;
		this.damage = 10;
		this.accuracy = 50;
		this.type = "TANK";
	}

	@Override
	public int recieveDamage(int damage){
		// 20% шансу поглинути ушкодженння
		if (Tools.tryRandom(80)) {
			return health;
		};

		return super.recieveDamage(damage);
	}
}