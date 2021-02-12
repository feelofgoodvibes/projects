package engine;
import units.Droid;
import map.*;
import java.util.*;
import java.util.Scanner;

public class Engine{
	static Scanner input_reader = new Scanner(System.in);

	/** Оновити інформацію про дроїда
	* @param map Масив карти
	* @param droids Масив дроїдів
	* @param teamsAmount Кількість команд
	* @return true, якщо є події (перестрілки)
	*/
	public static boolean gameLoop(List<String> map, List<Droid> droids, int teamsAmount){
		boolean events = false;
		Map<Droid, Droid> conflicts = MapUtils.getConflicts(droids, map);

		for (Droid droid : droids){
			if (!droid.isAlive()) { continue; }
			boolean localevent = droidUpdate(droid, map, conflicts);
			if (!events) events = localevent;
		}

		return events;
	}

	/** Оновити інформацію про дроїда
	* @param currentDroid Дроїд
	* @param map Масив карти
	* @param conflicts Конфлікти між дроїдами
	* @return true, якщо є події (перестрілки)
	*/
	public static boolean droidUpdate(Droid currentDroid, List<String> map, Map<Droid, Droid> conflicts){
		boolean events = false;
		
		// Якщо нема шляху руху - генеруємо
		if (currentDroid.getPath() == null){
			Point pathTo = MapUtils.getRandomPoint(map);
			List<Point> newPath = MapUtils.getPath(currentDroid.getPos(), pathTo, map);
			currentDroid.setPath(newPath);
		}

		// Якщо немає противника
		if (currentDroid.getTarget() == null){
			// Якщо є у кого вистрелити - робимо його противником
			if (conflicts.get(currentDroid) != null && conflicts.get(currentDroid).isAlive()){
				currentDroid.setTarget(conflicts.get(currentDroid));
				currentDroid.configState(true, map);	// Переводимо дроїда в фазу бою
				List<Point> line = MapUtils.getLine(currentDroid.getPos(), currentDroid.getTarget().getPos(), map);
				// System.out.println("line: " + line);
				if (line != null && line.size() > 1) MapUtils.drawLine(line, map, 3);	// Лінія між дроїдом і противником
			}

			// Якщо немає противника і немає в кого стріляти - продовжуємо рух по маршруту
			else {
				// Якщо рух по маршруту перешкоджено - генеруємо новий
				if (!currentDroid.progressPath(map)){
					currentDroid.setPath(MapUtils.getPath(currentDroid.getPos(), MapUtils.getRandomPoint(map), map));
				}
			}
		}

		// Якщо є противник
		else {
			// Стріляємо, якщо противник живий
			if (currentDroid.getTarget().isAlive()){
				currentDroid.attack(currentDroid.getTarget());
				events = true;
			}
			// Якщо супротивник мертвий (в т.ч. після пострілу)
			if (!currentDroid.getTarget().isAlive()){
				try {
					MapUtils.clearLine(MapUtils.getLine(currentDroid.getPos(), currentDroid.getTarget().getPos(), map), map);	// Стирання лінії
					MapUtils.clearLine(MapUtils.getLine(currentDroid.getTarget().getPos(), currentDroid.getPos() ,map), map);	// Стирання лінії
				} catch (Exception e) {}
				MapUtils.clearPoint(currentDroid.getTarget().getPos(), map);
				currentDroid.configState(false, map);		// Переведення дроїда в небойовий режим
				currentDroid.setTarget(null);
			}
		}

		return events;
	}
}