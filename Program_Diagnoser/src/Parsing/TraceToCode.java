package Parsing;
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
	private Scanner scanner;
	private int indexer;
	
	/***************
	 * Constructor.
	 ***************/
	public TraceToCode(){
		conversion_table = new HashMap<String,Integer>();
		indexer = 0;
	}
	
	
	/******************************************************************
	 * Conversion table size getter.
	 * @return No. of all components elicitated from the trace files.
	 ******************************************************************/
	public int get_comps_num(){
		return conversion_table.size();
	}
	
	
	/**************************************
	 * Raffles a single component.
	 * @return single component, randomly.
	 **************************************/
	public Entry<String, Integer> raffle_component(){
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
		//declare vars
		String comp = "";
		
		//process
		for(int i = 0; i < files.length; i++){
			//construct scanner
			scanner = new Scanner(new BufferedReader(new FileReader(files[i])));
		    scanner.useDelimiter("");
	    
		    //scan file
		    while(scanner.hasNext()){
		    	comp = scanner.nextLine();
		    	if (!conversion_table.containsKey(comp)){
		    		conversion_table.put(comp, indexer);
		    		indexer++;
		    	}
		    }//end while
		}//end for (files)	  
	    
	    TDP_Run.set_comps_num(conversion_table.size());
	}
	
	
	/*******************************
	 * Prints the conversion table. 
	 *******************************/
	public void printConvTable(){
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
		//initialize file
		File file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/conv_comp_table.csv");
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
	
	
	/**********************************************
	 * Converts methods-set into code.
	 * @param set - Set of methods' names.
	 * @return String[] representation of the set.
	 **********************************************/	
	public int[] setToArray(Set<String> set){
		//declare vars
		int[] result = null;
		
        //convert
        Object[] temp = set.toArray();
        result = new int[temp.length];
        
        for(int i = 0; i < temp.length; i++){
        	try{
        	result[i] = conversion_table.get((String)temp[i]);
        	}catch(Exception e){
        		System.out.println(conversion_table.toString() + temp.toString()); //for debug
        	}
        }//end for
        
        result = OrderAssist.quickSort(result);
		return result;	
	}
	
	
	/************************************************
	 * Converts trace file into code.
	 * The result is automatically ordered!
	 * @param file_name - Trace file name.
	 * @return String[] representation of the trace.
	 * @throws FileNotFoundException
	 ************************************************/
	public int[] fileToArray(File file) throws FileNotFoundException{
		//declare vars
		int[] result = null;
		HashSet<String> map = new HashSet<String>();
		
		 //construct scanner
		scanner = new Scanner(new BufferedReader(new FileReader(file)));
        scanner.useDelimiter("");

        //start scanning lines
        while (scanner.hasNextLine()) {
        	map.add(scanner.nextLine());
        }//end while (stream from file)
        scanner.close();
		
        //convert
        Object[] temp = map.toArray();
        result = new int[temp.length];
        
        for(int i = 0; i < temp.length; i++){
        	try{
        	result[i] = conversion_table.get((String)temp[i]);
        	}catch(Exception e){
        		System.out.println(conversion_table.toString() + temp.toString()); //for debug
        	}
        }//end for
        
        result = OrderAssist.quickSort(result);
		return result;
	}
	
	
	/**************************************************************
	 * Converts a batch of (sorted!) traces into code.
	 * @param file_names - Names of traces files.
	 * @return Hash table of tests and their activated components.
	 * @throws FileNotFoundException
	 **************************************************************/
	public HashMap<Integer,int[]> filesToArrays(File[] files) throws FileNotFoundException{
		//declare vars
		HashMap<Integer,int[]> map = new HashMap<Integer,int[]>();
		
		//process files
		for(int i = 0; i < files.length; i++){
			map.put(i, fileToArray(files[i]));
		}//end for (files)
		
		return map;
	}
	
	
	/*************************************************************************
	 * Converts tests traces into code and stores it in the given tests pool.
	 * The traces are internally sorted!
	 * @param pool - Tests pool.
	 * @param file_names - Tests traces files.
	 * @throws IOException 
	 **************************************************************************/
	public void add_traces_to_pool(Tests_Pool pool) throws IOException{
		//declare vars
		int[] current_test;
		
		//fill conversion table
		File[] traces_files = FilesAssist.get_trace_files();
		File[] base_traces_files = FilesAssist.get_base_trace_files();
		extractComps(traces_files);
		extractComps(base_traces_files);
		
		//process base traces
		HashMap<Integer,int[]> tests = filesToArrays(base_traces_files);
		for(int i = 0; i < tests.size(); i++){
			current_test = tests.get(i);
			pool.add_test(current_test, base_traces_files[i].getName().replace(".txt", ""));
		}//end for
	}
	
	
	/**************************************
	 * Loads a conversion table from file.
	 * @param file - CSV file.
	 * @throws FileNotFoundException 
	 **************************************/
	public void load_conversion_table(File file) throws FileNotFoundException{
		//initialize
		conversion_table.clear();
		
		Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
		String line;
		String[] line_parts;
		boolean first_line = true;
		while(scanner.hasNextLine()){
			line = scanner.nextLine();
			if(first_line){
				first_line = false;
				continue;
			}
			line_parts = line.split(",");
			conversion_table.put(line_parts[1].trim(),Integer.parseInt(line_parts[0]));
		}
		scanner.close();
	}
	
	
	/***************************************
	 * Stores a conversion table in a file.
	 ***************************************/
	public void store_conversion_table(File file) throws IOException{
		PrintWriter writer = new PrintWriter(new FileWriter(file, false));
		for(String key : conversion_table.keySet()){
			writer.println(conversion_table.get(key).intValue()+","+key);
		}
		writer.close();
	}
}
