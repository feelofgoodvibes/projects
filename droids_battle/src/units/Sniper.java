package units;
import java.util.List;
import engine.Tools;

public class Sniper extends Droid{
	public Sniper(int x, int y, char icon, String name){
		super(x, y, icon, name);
		this.health = 30;
		this.damage = 50;
		this.accuracy = 95;
		this.type = "SNIPER";
	}

	@Override
	public boolean progressPath(List<String> map){
		// 20% ще раз пройти по шляху
		boolean pathResult = super.progressPath(map);
		if (Tools.tryRandom(20)) {
			pathResult = super.progressPath(map);
		}

		return pathResult;
	}
}