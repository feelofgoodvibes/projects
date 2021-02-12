package main;

import java.io.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;

import units.Droid;
import engine.*;
import map.*;

public class Main{
	public static void main(String[] args) {
		Scanner inputReader = new Scanner(System.in);
		String inputBuffer;

		System.out.print("Enter path to map file: ");
		String mapName = inputReader.nextLine();
		List<String> battlemap = MapUtils.readMap(mapName);
		List<Droid> droids = new ArrayList<>();
		int teamsAmount = 0;
		double frameTime;

		Tools.clearScreen();
		MapUtils.printMap(battlemap, null, 0);
		System.out.print("\nEnter filename to read bots from (enter \"map\" to scan from map, or leave empty to create bots manually): ");
		inputBuffer = inputReader.nextLine();

		// Ручне введення
		if (inputBuffer.equals("")){
			Droid temp = MapUtils.createDroid();
			while (temp != null) {
				while (battlemap.get(temp.getPos().y).charAt(temp.getPos().x) != ' ') {
					System.out.println("Wrong coordinates!");
					temp = MapUtils.createDroid();
					continue;
				}
				battlemap.set(temp.getPos().y, Tools.setCharAt(battlemap.get(temp.getPos().y), temp.getPos().x, temp.getIcon()));
				MapUtils.addDroid(droids, temp);
				teamsAmount = MapUtils.countTeams(droids);
				Tools.clearScreen();
				MapUtils.printMap(battlemap, droids, teamsAmount);

				temp = MapUtils.createDroid();
			}
		}
		
		// Сканування карти
		else if (inputBuffer.equals("map")){
			droids = MapUtils.scanMap(battlemap);
		}

		// Зчитування з файлу
		else {
			if (!MapUtils.readDroids(inputBuffer, battlemap, droids)){
				System.out.println("Wrong filename or structure!");
				return;
			}
		}
		
		teamsAmount = MapUtils.countTeams(droids);
		Tools.clearScreen();
		MapUtils.printMap(battlemap, droids, teamsAmount);
		System.out.println("Press Enter to start . . . ");
		inputReader.nextLine();

		while (true){
			frameTime = 0.3;
			double start = System.nanoTime();
			if (Engine.gameLoop(battlemap, droids, teamsAmount)) frameTime += 2;
			Tools.clearScreen();
			MapUtils.printMap(battlemap, droids, teamsAmount);
			while (((System.nanoTime() - start) / 1000000000) < frameTime) { continue; };
		}
	}
}