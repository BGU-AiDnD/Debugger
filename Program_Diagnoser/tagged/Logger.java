package Implant;
import Implant.*;


import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Iterator;


public class Logger {
	//declare global vars
	public static HashSet<String> cache = new HashSet<String>();
	public static File trace_dir = new File(TestsRunner.WORKSPACE_PATH+"/traces");
	
	/*******************************************
	 * Adds the given method's name to the log.
	 * @param method_name - Method name.
	 *******************************************/
	public static void log(String method_name){
Logger.log("Logger.log");
boolean _bug_switch = Bug_Switcher.has_bug("Logger.log");
if (_bug_switch)
	return;

		cache.add(method_name);
	}
	
	
	/************************
	 * Refreshes the logger.
	 ************************/
	public static void refresh(){
Logger.log("Logger.refresh");
boolean _bug_switch = Bug_Switcher.has_bug("Logger.refresh");
if (_bug_switch)
	return;

		cache = new HashSet<String>();
	}
	
	
	/********************************
	 * Dumps the log to disk.
	 * @param file_name - File name.
	 ********************************/
	public static void commit(String file_name){
Logger.log("Logger.commit");
boolean _bug_switch = Bug_Switcher.has_bug("Logger.commit");
if (_bug_switch)
	return;

		//don't generate empty traces!! (Staccato can't handle them)
		if (cache.size() == 0)
			return;
		
		//declare vars
		File trace_file = new File(TestsRunner.WORKSPACE_PATH+"/traces", file_name);
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
}
