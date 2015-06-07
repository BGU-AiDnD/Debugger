package Implant;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Scanner;

public class Bug_Switcher {
	private static boolean file_loaded = false;
	private static HashMap<String,String> has_bugs = new HashMap<String,String>();
	private static File file = new File("c:/TOM/eclipse/workspace/Program_Diagnoser/src/Implant/has_bugs.txt");
	
	
	/**********************
	 * Load the list file.
	 **********************/
	private static void load_file(){
		String comp = "";
		
        //construct scanner
		Scanner scanner = null;
		try {
			scanner = new Scanner(new BufferedReader(new FileReader(file)));
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
        scanner.useDelimiter("");
        while (scanner.hasNextLine()) {
        	comp = new String();
        	comp = scanner.nextLine();
        	has_bugs.put(comp, null);
        }
        
        //wrap
        scanner.close();
        file_loaded = true;
	}
	
	
	/**********************************************************************************
	 * Cheks whether the given component is listed as having a bug.
	 * @param comp - Component name;
	 * @return True - if given component is listed as having a bug. False - otherwise.
	 ***********************************************************************************/
	public static boolean has_bug(String comp){
		//make sure file was loaded
		if (file_loaded == false)
			load_file();
		
		boolean result = has_bugs.containsKey(comp);
		if (result == true)
			return true;
		else return false;
	}
}
