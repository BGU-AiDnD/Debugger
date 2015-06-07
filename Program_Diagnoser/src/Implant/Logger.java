package Implant;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;

public class Logger {
	//declare global vars
	public static File trace_dir = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces");
	private static final String deep_file = "deep_log.txt";
	
	private static boolean deep_log_flag  = false; //springy switch
	private static HashSet<String> cache = new HashSet<String>();
	private static LinkedList<String> deep_cache = new LinkedList<String>();
	
	
	/****************************************************************************
	 * Deep logging switch.
	 * Notice: deep log switch is a springy switch!
	 * Logger will return to normal logging after the first next commit command.
	 * @param flag - Boolen flag.
	 ****************************************************************************/
	public static void set_deep_log(){
		deep_log_flag = true;
		clear_deep_file();
	}
	
	/*******************************************
	 * Adds the given method's name to the log.
	 * @param method_name - Method name.
	 *******************************************/
	public static void log(String method_name){
		if (deep_log_flag)
			log_deep(method_name);
		
		else cache.add(method_name);
	}
	
	
	/************************
	 * Refreshes the logger.
	 ************************/
	public static void refresh(){
		cache.clear();
		deep_cache.clear();
	}
	
	
	/*******************************************
	 * Adds the given method's name to the log.
	 * Commits when log is too big.
	 *******************************************/
	private static void log_deep(String method_name){
		//avoid re-logging the same method in sequence (in loops for example)
		if(deep_cache.size() >= 1 && deep_cache.getLast().equals(method_name))
			return;
		
		deep_cache.add(method_name);
		
		//handle explosion of cache
		if (deep_cache.size() >= 100){
			commit_deep();
			deep_cache.clear();
		}
	}
	
	
	/***********************************
	 * Light commiter.
	 * Dumps the log to specified file.
	 * @param file_name - File name.
	 ***********************************/
	private static void commit_light(String file_name){	
		//don't generate empty traces!! (Staccato can't handle them)
		if (cache.size() == 0)
			return;
		
		//declare vars
		File trace_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces", file_name);
		String temp_method_name = "";
		Iterator<String> iterator = cache.iterator();
		
		//process
	    try{
	    //handle no file	
	    if(trace_file.exists()== false){
	    	trace_dir.mkdir();
	    	trace_file.createNewFile();
	    }
	    
    	//clear file
    	PrintWriter out = new PrintWriter(new FileWriter(trace_file, false));
	    out.print("");
	    out.close();
	    
	    //write
	    out = new PrintWriter(new FileWriter(trace_file, true));
	    while(iterator.hasNext()){
	    	temp_method_name = iterator.next();
	    	out.println(temp_method_name); 
	    }//end while 
	    
	    //wrap 
	    out.close();
	    }catch(IOException e){
			e.printStackTrace();
	    }	
	}
	
	
	/********************************
	 * Clears a trace file.
	 * @param file_name - File name.
	 ********************************/
	private static void clear_deep_file(){
		//declare vars
		File trace_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces", deep_file);
		
	    //handle no file
	    if(trace_file.exists()== false)
	    	trace_dir.mkdir();
	    
	    //clear file
	    PrintWriter out = null;
		try {
			out = new PrintWriter(new FileWriter(trace_file, false));
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		//wrap
	    out.print("");
	    out.close();
	}
	
	
	/***********************************
	 * Deep commiter.
	 * Dumps the log to specified file.
	 * @param file_name - File name.
	 ***********************************/
	private static void commit_deep(){
		//declare vars
		File trace_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces", deep_file);
		String temp_method_name = "";
		Iterator<String> iterator = deep_cache.iterator();
		
		//process
	    try{
	    //handle no file	
	    if(trace_file.exists()== false){
	    	trace_dir.mkdir();
	    	trace_file.createNewFile();
	    }
	    
	    //write
	    PrintWriter out = new PrintWriter(new FileWriter(trace_file, true));
	    while(iterator.hasNext()){
	    	temp_method_name = iterator.next();
	    	out.println(temp_method_name); 
	    }//end while 
	    
	    //wrap 
	    out.close();
	    }catch(IOException e){
			e.printStackTrace();
	    }		
	}
	
	
	/********************************
	 * Dumps the log to disk.
	 * @param file_name - File name.
	 ********************************/
	public static void commit(String file_name){
		if (deep_log_flag){
			commit_deep();
			deep_log_flag = false; //deep log switch is a springy switch!
		}
		
		else commit_light(file_name);
	}
}
