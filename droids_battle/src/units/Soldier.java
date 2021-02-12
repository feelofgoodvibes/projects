package units;
import engine.Tools;

public class Soldier extends Droid{
	public Soldier(int x, int y, char icon, String name){
		super(x, y, icon, name);
		this.health = 100;
		this.damage = 30;
		this.accuracy = 75;
		this.type = "SOLDIER";
	}

	@Override
	public void attack(Droid enemy){
		// 20% атакувати ще раз
		super.attack(enemy);
		if (Tools.tryRandom(20)) {
			super.attack(enemy);
		}
	}
}