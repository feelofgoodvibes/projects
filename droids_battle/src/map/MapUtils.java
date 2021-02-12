package map;

import java.util.*;
import java.io.*;
import units.*;
import engine.Tools;
import java.util.Random;

public class MapUtils{
	static char WALL = '#';		// символ стіни
	static char BLANK = ' ';	// символ пустоти
	static char LINE = '.';		// символ лінії


	/** Зчитати карту з файлу
	* @param filename Ім'я файлу
	* @return Масив рядків, які являють собою карту
	*/
	public static List<String> readMap(String filename){
		String buffer;
		List<String> map = new ArrayList<>();

		try{
			BufferedReader fileReader = new BufferedReader(new FileReader(filename));
			while((buffer = fileReader.readLine()) != null) map.add(buffer);
			fileReader.close();
		} catch (Exception ex) { return null; }

		return map;
	}

	/** Зчитати інформацію про дроїдів з файлу
	* @param filename Ім'я файлу
	* @param map Масив карти
	* @param droids Масив дроїдів, в який заноситься інформація про нових з файлу
	* @return true, якщо вдалося зчитати
	*/
	public static boolean readDroids(String filename, List<String> map, List<Droid> droids){
		File file = new File("..\\..\\nicknames.txt");
		try{
			BufferedReader fileReader = new BufferedReader(new FileReader(filename));
			String buffer;
			while ((buffer = fileReader.readLine()) != null) {
				String[] splitted_string = buffer.split(", ");
				Droid currentDroid;
				System.out.println();
				if (splitted_string[1].equals("%random%")) { splitted_string[1] = Tools.getRandomName(file); }
				if (splitted_string[0].equals("0")) currentDroid = new Soldier(Integer.parseInt(splitted_string[2]), Integer.parseInt(splitted_string[3]), splitted_string[4].charAt(0), splitted_string[1]);
				else if (splitted_string[0].equals("1")) currentDroid = new Tank(Integer.parseInt(splitted_string[2]), Integer.parseInt(splitted_string[3]), splitted_string[4].charAt(0), splitted_string[1]);
				else if (splitted_string[0].equals("2")) currentDroid = new Sniper(Integer.parseInt(splitted_string[2]), Integer.parseInt(splitted_string[3]), splitted_string[4].charAt(0), splitted_string[1]);
				else { System.out.println("Wrong class!"); return false; }

				if (map.get(currentDroid.getPos().y).charAt(currentDroid.getPos().x) != ' ') return false;
				map.set(currentDroid.getPos().y, Tools.setCharAt(map.get(currentDroid.getPos().y), currentDroid.getPos().x, currentDroid.getIcon()));
				addDroid(droids, currentDroid);
				System.out.println('+');
			}
			fileReader.close();

		} catch (Exception ex) { System.out.println(ex.toString()); return false; }
		return true;
	}

	/** Вручну ввести дані про нового дроїда
	* @return Створений дроїд
	*/
	public static Droid createDroid(){
		Scanner inputReader = new Scanner(System.in);
		String buffer;

		System.out.print("Class [SOLDIER (0), TANK (1), SNIPER (2)]: ");
		String new_class = inputReader.nextLine();
		if (new_class.equals("")) return null;
		System.out.print("Name: ");
		String new_name = inputReader.nextLine();

		System.out.print("Position: ");
		buffer = inputReader.nextLine();
		int new_x = Integer.parseInt(buffer.split(" ")[0]);
		int new_y = Integer.parseInt(buffer.split(" ")[1]);

		System.out.print("Icon: ");
		buffer = inputReader.nextLine();
		char new_icon = buffer.charAt(0);

		Droid currentDroid;
		switch (new_class){
			case ("0") : { currentDroid = new Soldier(new_x, new_y, new_icon, new_name); break; } 
			case ("1") : { currentDroid = new Tank(new_x, new_y, new_icon, new_name); break; } 
			case ("2") : { currentDroid = new Sniper(new_x, new_y, new_icon, new_name); break; }
			default : currentDroid = new Soldier(new_x, new_y, new_icon, new_name);
		}

		return currentDroid;
	}

	/** Зчитати інформацію про дроїдів з карти
	* @param map Масив карти
	* @return Масив дроїдів на карті
	*/
	public static List<Droid> scanMap(List<String> map){
		List<Droid> result = new ArrayList<>();
		File file = new File("..\\..\\nicknames.txt");

		for (int y = 0; y < map.size(); y++){
			for (int x = 0; x < map.get(y).length(); x++){
				if ((map.get(y).charAt(x) != WALL) && (map.get(y).charAt(x) != BLANK)){
					addDroid(result, new Soldier(x, y, map.get(y).charAt(x), Tools.getRandomName(file)));
				}
			}
		}

		return result;
	}

	/** Порахувати кількість команд в масиві дрїдів
	* @param droids Масив дроїдів
	* @return Кількість команд
	*/
	public static int countTeams(List<Droid> droids){
		int amount = 0;
		HashSet<Character> checkedTeams = new HashSet<Character>();
		for (Droid droid : droids){
			if (!checkedTeams.contains(droid.getIcon())){
				amount += 1;
				checkedTeams.add(droid.getIcon());
			}
		}

		return amount;
	}

	/** Додати дроїда в масив дроїдів на вірне місце
	* @param droids Масив дроїдів
	* @param droid Дроїд, якого додаємо
	*/
	public static void addDroid(List<Droid> droids, Droid droid){
		char findChar = droid.getIcon();
		int createAt = -1;
		if (droids.size() <= 1) { droids.add(droid); return; }
		for (int i = droids.size() - 1; i >= 0; i--){
			if (droids.get(i).getIcon() == findChar){ createAt = i; break; }
		}

		if (createAt == -1) { droids.add(droid); }
		else { droids.add(createAt, droid); }
	}

	/** Друк карти на екран консолі
	* @param map Масив карти
	* @param droids Масив дроїдів
	* @param teams Кількість команд на карті
	*/
	public static void printMap(List<String> map, List<Droid> droids, int teams){
		if (droids == null){ printMapSimple(map); return; }
		int printInfoIndex = (map.size() - droids.size() - teams) / 2;	// З якого індексу починати друк дроїдів (середина карти)
		int currentDroid = 0;	// Процесс друку дроїдів
		char currentTeam = Tools.toLower(droids.get(0).getIcon());

		for (int y = 0; y < map.size(); y++){
			System.out.print(map.get(y));
			if (y >= printInfoIndex && currentDroid < droids.size()){
				if (Tools.toLower(droids.get(currentDroid).getIcon()) != currentTeam) {
					currentTeam = Tools.toLower(droids.get(currentDroid).getIcon());
					System.out.print("\n");
					continue;
				}
				System.out.println("   " + droids.get(currentDroid).toString());
				currentDroid += 1;
			}
			else System.out.print('\n');
		}

		while (currentDroid < droids.size()) {
			if (Tools.toLower(droids.get(currentDroid).getIcon()) != currentTeam) {
				currentTeam = Tools.toLower(droids.get(currentDroid).getIcon());
				System.out.print("\n");
				continue;
			}
			System.out.println(droids.get(currentDroid).toString());
			currentDroid += 1;
		}
	}

	/** Спрощений друк карти
	* @param map Масив карти
	*/
	public static void printMapSimple(List<String> map){ for (String y : map) System.out.println(y); }

	/** Зачищення точки на карті
	* @param point Точка, яку потрібно очистити
	* @param map Масив карти
	*/
	public static void clearPoint(Point point, List<String> map){
		map.set(point.y,  Tools.setCharAt(map.get(point.y), point.x, BLANK));
	}

	/** Отримати точки лінії між двома точками
	* @param from З якої точки
	* @param to До якої точки
	* @param map Масив карти
	* @return Масив точок
	*/
	public static List<Point> getLine(Point from, Point to, List<String> map){
		Point start = new Point(from);	// Лінія З
		Point end = new Point(to);		// Лінія ДО
		boolean reverse = false;		// Прапорець обрахунку координат в зворотньому порядку

		// Реверс обрахунку координат якщо точка "З" нижче точки "ДО"
		// За рахунок цього лінії [x, y] та [y, x] будуть одинаковими
		// (без реверсу вони за певних умов можуть бути різними через округлення координат)
		if (start.y < end.y){
			reverse = true;
			int temp = start.x;
			start.x = end.x; end.x = temp;
			temp = start.y;
			start.y = end.y; end.y = temp;
		}
		double x = start.x;		//	Тимчасові координати. 
		double y = start.y;		//	Являють собою точку, на якій зараз відбувається обрахунок точки лінії

		int steps = (Math.abs(end.x - start.x) + Math.abs(end.y - start.y));	// Кількість кроків в побудові лінії

		double dx = (double)(end.x - start.x) / (steps + 3);	// На скільки збільшується Х на кожному кроці
		double dy = (double)(end.y - start.y) / (steps + 3);	// На скільки збільшується Y на кожному кроці

		List<Point> result = new ArrayList<>();		// Масив точок лінії

		int i = 0;
		while (true){
			// Якщо точка не змінилась - не додаємо в масив
			if ((int)(x + dx) == x && (int)(y + dy) == y){
				x += dx;
				y += dy;
				i -= 1;
				continue;
			}

			x += dx;	// Зміна фактичного Х на різницю координати на кожному кроці
			y += dy;	// Зміна фактичного Y на різницю координати на кожному кроці

			// Якщо лінія йде через стіну - повертаємо NULL
			if (map.get((int)(y)).charAt((int)(x)) == WALL) return null;
			
			Point point = new Point((int)(x), (int)(y));
			if (point.x == end.x && point.y == end.y) break;	// Якщо досягли кінця - виходимо з циклу
			result.add(point);
			i += 1;
		}

		if (reverse == true) Collections.reverse(result);	// Відновлення початкового порядку координат точок, якщо на початку відбувся реверс
		return result;
	}

	/** Намалювати лінію на карті
	* @param points Точки лінії
	* @param map Масив карти
	* @param step Інтервал лінії
	*/
	public static void drawLine(List<Point> points, List<String> map, int step){
		for (int i = 0; i < points.size(); i += step){
			if (map.get(points.get(i).y).charAt(points.get(i).x) == BLANK){
				map.set(points.get(i).y, Tools.setCharAt(map.get(points.get(i).y), points.get(i).x, LINE));
			}
		}

		Point endOfLine = points.get(points.size()-1); 
		for (int i = points.size()-1; i > 0; i--){
			if (map.get(points.get(i).y).charAt(points.get(i).x) != '*'){
				endOfLine = points.get(i);
				break;
			}
		}
		map.set(endOfLine.y, Tools.setCharAt(map.get(endOfLine.y), endOfLine.x, '*'));
	}

	/** Очистити лінію з карті
	* @param points Точки лінії
	* @param map Масив карти
	*/
	public static void clearLine(List<Point> points, List<String> map){
		for (Point point : points){
			if (map.get(point.y).charAt(point.x) == LINE || map.get(point.y).charAt(point.x) == '*'){
				map.set(point.y, Tools.setCharAt(map.get(point.y), point.x, BLANK));
			}
		}
	}

	/** Отримати найкоротшоий шлях між двома точками
	* @param start З якої точки шлях
	* @param end До якої точки шлях
	* @param map Масив карти
	* @return Масив точок шляху
	*/
	public static List<Point> getPath(Point start, Point end, List<String> map){
		// Матриця відвіданих точок
		int matrixX = map.get(0).length();
		int matrixY = map.size();
		int[][] visited_matrix = new int[matrixY][matrixX];
		for (int y = 0; y < matrixY; y++){
			for (int x = 0; x < matrixX; x++){
				visited_matrix[y][x] = 0;
			}
		}

		Queue<Point> points_queue = new ArrayDeque<Point>();	// Черга точок, які потрібно відвідати
		Map<Point, Point> path = new HashMap<Point, Point>();	// Шляхи, якими ми рухались (потрібно для відтворення найкоротшого з них)
		List<Point> shortestPath = new ArrayList<>();			// Найкоротший шлях

		visited_matrix[start.y][start.x] = 1;
		points_queue.add(start);
		Point current_point;	// Точка, на якій ми перебуваємо зараз
		Point temp;				// Тимчасова змінна для обробки точок, в які ми рухаємось

		// Цикл, що виконується поки є неперевірені точки, або поки не досягнемо цілі
		while ((current_point = points_queue.poll()) != null){
			if (current_point.equals(end)) break;			// Якщо дійшли до цілі

			// Масив точок, які потрібно занести в чергу
			// потрібен для того, щоб заносити їх в випадковому порядку, тим самим роблячи шлях менш лінійноподібним
			List<Point> addToQueue = new ArrayList<Point>();	

			// Перевіряємо точки, сусідні до тої, на якій ми знаходимось зараз
			// Заносимо сусідню точку у чергу, якщо вона не є стіною, або якщо вона ще не відвідана  
			if (map.get(current_point.y).charAt(current_point.x + 1) != WALL && visited_matrix[current_point.y][current_point.x + 1] == 0){
				temp = new Point(current_point.x + 1, current_point.y);
				path.put(temp, current_point);
				addToQueue.add(temp);
				visited_matrix[current_point.y][current_point.x + 1] = 1;
			}
			if (map.get(current_point.y - 1).charAt(current_point.x) != WALL && visited_matrix[current_point.y - 1][current_point.x] == 0){
				temp = new Point(current_point.x, current_point.y - 1);
				path.put(temp, current_point);
				addToQueue.add(temp);
				visited_matrix[current_point.y - 1][current_point.x] = 1;
			}
			if (map.get(current_point.y).charAt(current_point.x - 1) != WALL && visited_matrix[current_point.y][current_point.x - 1] == 0){
				temp = new Point(current_point.x - 1, current_point.y);
				path.put(temp, current_point);
				addToQueue.add(temp);
				visited_matrix[current_point.y][current_point.x - 1] = 1;
			}
			if (map.get(current_point.y + 1).charAt(current_point.x) != WALL && visited_matrix[current_point.y + 1][current_point.x] == 0){
				temp = new Point(current_point.x, current_point.y + 1);
				path.put(temp, current_point);
				addToQueue.add(temp);
				visited_matrix[current_point.y + 1][current_point.x] = 1;
			}

			Collections.shuffle(addToQueue);				// Занесення у чергу у випадковому порядку невідвіданих сусідніх точок
			for (Point p : addToQueue) points_queue.add(p);	// За рахунок чого шлях не є лінійноподібним
		}

		// Відтворення зворотнього найкоротшого шляху
		while (current_point != null){
			shortestPath.add(0, current_point);
			current_point = path.get(current_point);	// Додаємо у масив найкоротшого шляху точки, з яких прийшли
		}

		shortestPath.remove(0);		// Видалення точки, в якій знаходимось зараз
		return shortestPath;
	}

	public static void drawPath(List<Point> path, List<String> map){
		for (Point p : path){
			map.set(p.y, Tools.setCharAt(map.get(p.y), p.x, 'x'));
		}
	}

	/** Отримати дроїдів, які між собою можуть перестрілюватись
	* @param droids Масив дроїдів
	* @param map Масив карти
	* @return Набір пар дроїдів, які між собою можуть перестрілюватись
	*/
	public static Map<Droid, Droid> getConflicts(List<Droid> droids, List<String> map){
		Map<Droid, Droid> conflicts = new HashMap<Droid, Droid>();

		for (int i1 = 0; i1 < droids.size(); i1++){
			if (!droids.get(i1).isAlive()) continue;
			for (int i2 = i1 + 1; i2 < droids.size(); i2++){
				if (!droids.get(i2).isAlive()) continue;
				if (droids.get(i1) != droids.get(i2) && droids.get(i1).canShoot(droids.get(i2), map) && Tools.toLower(droids.get(i1).getIcon()) != Tools.toLower(droids.get(i2).getIcon())){
					conflicts.put(droids.get(i1), droids.get(i2));
					conflicts.put(droids.get(i2), droids.get(i1));
				}
			}
		}

		return conflicts;
	}

	/** Отримати випадкову точку на карті
	* @param map Масив карти
	* @return Випадкова точка
	*/
	public static Point getRandomPoint(List<String> map){
		Random random = new Random();
		Point result = new Point(random.nextInt(map.get(0).length()), random.nextInt(map.size()));
		while ((map.get(result.y).charAt(result.x)) != BLANK){
			result = new Point(random.nextInt(map.get(0).length()), random.nextInt(map.size()));
		}

		return result;
	}
}