package engine;
import java.util.List;
import java.util.ArrayList;
import java.io.*;
import java.util.Random;

public class Tools{
	static Random random = new Random();

	// Опустити символ в нижній регістр
	public static char toLower(char c){
		if (c >= 'a' && c <= 'z') return c;
		return (char)((int)c + 32);
	}

	// Підняти символ в верхній регістр
	public static char toUpper(char c){
		if (c >= 'A' && c <= 'Z') return c;
		return (char)((int)c - 32);
	}

	/** Замінити символ в рядку
	* @param input_string Рядок
	* @param i Індекс, який потрібно замінити
	* @param с Символ, на який потрібно замінити
	* @return Рядок з заміненим символом
	*/
	public static String setCharAt(String input_string, int i, char c){
		StringBuilder result = new StringBuilder(input_string);
		result.setCharAt(i, c);
		return result.toString();
	}

	/** Очистити екран консолі */
	public static void clearScreen() {
		try { new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor(); }
		catch (Exception ex) { System.out.println(ex.toString()); }
	}

	/** Випадковість події
	*	@param percentage Відсоток вдачі
	*	@return true, якщо подія відбулася, false, якщо ні
	*/
	public static boolean tryRandom(int percentage){
		if (random.nextInt(100) < percentage) return true;
		else return false;
	}

	/** Отримати випадкове число в інтервалі [from, to]
	*	@param from початок інтервалу
	*	@param to кінець інтервалу
	*	@return Випадкове число в інтервалі
	*/
	public static int randomInt(int from, int to){
		return random.nextInt(to-from) + from;
	}

	/** Отримати випадкове ім'я з файлу
	*	@param file файл з іменами
	*	@return Випадкове ім'я
	*/
	public static String getRandomName(File file){
		String name = "Undefined";
		try{
			RandomAccessFile workfile = new RandomAccessFile(file, "r");
			workfile.seek(Math.abs(random.nextLong()) % workfile.length());	// переходимо на випадкову позицію в файлі
			workfile.readLine();				// зчитуємо поточний рядок до кінця (зчитає неповністю)
			name = workfile.readLine();			// зчитуємо повністю наступний рядок

			workfile.close();
		}
		catch (Exception ex) { System.out.println(ex.toString()); }
		return name;
	}
}