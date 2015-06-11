package Parsing;
import Implant.*;

import Implant.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;

import Experimenter.TDP_Run;
import Infrastrcture.OrderAssist;
import Planner.Tests_Pool;


public class TraceToCode {
	//declare global vars
	private HashMap<String,Integer> conversion_table;
	
	/***************
	 * Constructor.
	 ***************/
	public TraceToCode(){
		conversion_table = new HashMap<String,Integer>();
	}
	
	
	/********
	 * Loads a conversion table from file.
	 * @param file - CSV file.
	 * @throws FileNotFoundException 
	 */
	public void load_conversion_table(File file) throws FileNotFoundException{
Logger.log("TraceToCode.load_conversion_table");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.load_conversion_table");
if (_bug_switch)
	return;

		//initialize
		conversion_table.clear();
		
		Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
		String line;
		String[] line_parts;
		boolean first_line=true;
		while(scanner.hasNextLine()){
			line = scanner.nextLine();
			if(first_line){
				first_line=false;
				continue;
			}
			line_parts = line.split(",");
			conversion_table.put(line_parts[1].trim(),Integer.parseInt(line_parts[0]));
		}
		scanner.close();
	}
	
	/**
	 * Stores a conversion table in a file
	 */
	public void store_conversion_table(File file) throws IOException{
Logger.log("TraceToCode.store_conversion_table");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.store_conversion_table");
if (_bug_switch)
	return;

		PrintWriter writer = new PrintWriter(new FileWriter(file, false));
		for(String key : conversion_table.keySet()){
			writer.println(conversion_table.get(key).intValue()+","+key);
		}
		writer.close();
	}
	
	
	/******************************************************************
	 * Conversion table size getter.
	 * @return No. of all components elicitated from the trace files.
	 ******************************************************************/
	public int get_comps_num(){
Logger.log("TraceToCode.get_comps_num");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.get_comps_num");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return conversion_table.size();
	}
	
	
	/**************************************
	 * Raffles a single component.
	 * @return single component, randomly.
	 **************************************/
	public Entry<String, Integer> raffle_component(){
Logger.log("TraceToCode.raffle_component");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.raffle_component");
if (_bug_switch)
	return null;

		//initialize
		Entry<String, Integer> result = null;
		
		//process
		Set<Entry<String, Integer>> comps_list = conversion_table.entrySet();
		Iterator<Entry<String, Integer>> iterator = comps_list.iterator();
		int comp = (int)(Math.random() * comps_list.size());
		int i = 0;
		
		while(i <= comp){
			result = iterator.next();
			i++;
		}
		
		//wrap
		return result;
	}
	
	
	/****************************************************
	 * Extracts components out of traces and codes them.
	 * @param file_names - Tests traces files.
	 * @throws FileNotFoundException
	 ****************************************************/
	private void extractComps(File[] files) throws FileNotFoundException{
Logger.log("TraceToCode.extractComps");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.extractComps");
if (_bug_switch)
	return;

		Scanner scanner;
		for(int i = 0; i < files.length; i++){
			//construct scanner
			scanner = new Scanner(new BufferedReader(new FileReader(files[i])));
		    scanner.useDelimiter("");
	    
		    //scan file
		    while(scanner.hasNext())
		    	conversion_table.put(scanner.nextLine(), null);
		}//end for (files)
		
	    //give index
	    int i = 0;
	    Entry<String,Integer> entry;
	    Iterator<Entry<String,Integer>> iterator = conversion_table.entrySet().iterator();
	    
	    while(iterator.hasNext()){
	    	entry = iterator.next();
	    	entry.setValue(i);
	    	i++;
	    }//end while
	    
	    TDP_Run.set_comps_num(conversion_table.size());
	}
	
	
	/*******************************
	 * Prints the conversion table. 
	 *******************************/
	public void printConvTable(){
Logger.log("TraceToCode.printConvTable");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.printConvTable");
if (_bug_switch)
	return;

		Iterator<Entry<String,Integer>> iterator = conversion_table.entrySet().iterator();
		Entry<String,Integer> entry;
		
	    System.out.println("Components Table:");
		while(iterator.hasNext()){
	    	entry = iterator.next();
	    	System.out.println(entry.getValue() + ":\t" + entry.getKey());
	    }//end while
		
		System.out.println("");
	}
	
	
	/***************************************************
	 * Saves the comonents conversion table to disk.
	 * @throws IOException when file can't be obtained.
	 ***************************************************/
	public void saveConvTable() throws IOException{
Logger.log("TraceToCode.saveConvTable");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.saveConvTable");
if (_bug_switch)
	return;

		//initialize file
		File file = new File(TestsRunner.WORKSPACE_PATH+"/conv_comp_table.csv");
		if (!file.exists())
			file.createNewFile();
		
		PrintWriter writer = new PrintWriter(new FileWriter(file, false));
		writer.print("");
		writer.close();
		writer = new PrintWriter(new FileWriter(file, true));
		
		Iterator<Entry<String,Integer>> iterator = conversion_table.entrySet().iterator();
		Entry<String,Integer> entry;
		
	    writer.println("Components Table:");
		while(iterator.hasNext()){
	    	entry = iterator.next();
	    	writer.println(entry.getValue() + ",\t" + entry.getKey());
	    }//end while
		
		//wrap
		writer.close();
		System.out.println("Components conversion table was saved to: " + file.toPath());	
	}
	
	
	/************************************************
	 * Converts trace file into code.
	 * @param file_name - Trace file name.
	 * @return String[] representation of the trace.
	 * @throws FileNotFoundException
	 ************************************************/
	public int[] fileToArray(File file) throws FileNotFoundException{
Logger.log("TraceToCode.fileToArray");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.fileToArray");
if (_bug_switch)
	return null;

		//declare vars
		int[] result = null;
		HashSet<String> map = new HashSet<String>();
		
		 //construct scanner
		Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
        scanner.useDelimiter("");

        //start scanning lines
        String line;
        while (scanner.hasNextLine()) {
        	line = scanner.nextLine();
        	System.out.println(line);
        	map.add(line );
        }//end while (stream from file)
        scanner.close();
		
        //convert
        Object[] temp = map.toArray();
        result = new int[temp.length];
        
        String component_name;
        int new_index;
        for(int i = 0; i < temp.length; i++){
        	component_name = (String)temp[i];
        	if(conversion_table.containsKey(component_name)==false){
        		new_index = conversion_table.size();
        		conversion_table.put(component_name, new_index);
        		TDP_Run.set_comps_num(conversion_table.size());				
        	}
        		
        	result[i] = conversion_table.get(component_name);
        }//end for
        
        result = OrderAssist.quickSort(result);
		return result;
	}
	
	
	/**************************************************************
	 * Converts a batch of traces into code.
	 * @param file_names - Names of traces files.
	 * @return Hash table of tests and their activated components.
	 * @throws FileNotFoundException
	 **************************************************************/
	public HashMap<Integer,int[]> filesToArrays(File[] files) throws FileNotFoundException{
Logger.log("TraceToCode.filesToArrays");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.filesToArrays");
if (_bug_switch)
	return null;

		//declare vars
		HashMap<Integer,int[]> map = new HashMap<Integer,int[]>();
		
		//fill conversion table
		if ((conversion_table == null)||(conversion_table.size()==0))
			extractComps(files);
		
		//process files
		for(int i = 0; i < files.length; i++){
			map.put(i, fileToArray(files[i]));
		}//end for (files)
		
		return map;
	}
	
	
	/*************************************************************************
	 * Converts tests traces into code and stores it in the given tests pool.
	 * @param pool - Tests pool.
	 * @param file_names - Tests traces files.
	 * @throws FileNotFoundException
	 **************************************************************************/
	public void addFilesToPool(Tests_Pool pool, File[] files) throws FileNotFoundException{
Logger.log("TraceToCode.addFilesToPool");
boolean _bug_switch = Bug_Switcher.has_bug("TraceToCode.addFilesToPool");
if (_bug_switch)
	return;

		//declare vars
		int[] current_test;
		
		//process
		HashMap<Integer,int[]> tests = filesToArrays(files);
		for(int i = 0; i < tests.size(); i++){
			current_test = tests.get(i);
			pool.add_test(current_test, files[i].getName().replace(".txt", ""));
		}//end for
	}
}
