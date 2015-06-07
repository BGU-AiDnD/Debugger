package Implant;

import java.awt.Toolkit;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

import org.junit.Test;
import org.junit.runner.Description;
import org.junit.runner.Request;
import org.junit.runner.notification.Failure;

import Implant.Logger;

public class TestsRunner {
	public static String now_running = "";
	private static File fail_list_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/src/Implant/failed_tests.txt");
	private static File tests_dir = new File("c:/tom/eclipse/workspace/Appache Tests/src");
	private static boolean failures_file_cleared = false;
	
	@Test
	public void testToast() throws Exception{
		Logger.log("TestsRunner.testToast");
		boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.testToast");
		if (_bug_switch)
			throw new Exception("toast");
	}
	
	
	/******************************************
	 * Now running setter.
	 * @param test_full_name - test full name.
	 ******************************************/
	public static void set_now_running(String test_full_name){
		now_running = test_full_name;
	}
	
	
	/*********************************
	 * Failed tests list file setter.
	 * @param file - File.
	 *********************************/
	public static void set_fail_list_file(File file){
		fail_list_file = file;
	}
	
	
	/***************************
	 * Tests path setter.
	 * @param path - Dir path.
	 * @throws IOException 
	 ***************************/
	public static void set_tests_path(File dir) throws IOException{
		tests_dir = dir;
		System.out.println("Tests source path was set to: " + dir.toPath().toRealPath());
	}
	
	
	/*********************************************
	 * Gets all the Testing classes.
	 * @param source - Root path.
	 * @param prefix - Prefix.
	 * @return All the relevant Testing classes.
	 * @throws IOException
	 * @throws ClassNotFoundException
	 *********************************************/
	private static LinkedList<Class<?>> get_classes(Path source, String prefix) throws IOException, ClassNotFoundException{
		//initialize
		LinkedList<Class<?>> list = new LinkedList<Class<?>>();
		String temp_prefix;
		
		//process
		DirectoryStream<Path> stream = Files.newDirectoryStream(source);
		File temp_file = null;
		
		//process
		String file_name;
		for (Path path: stream){	
			temp_file = path.toFile();
			file_name = temp_file.getName();
			
			//drill down
			if (temp_file.isDirectory()){
				if (!prefix.equals(""))
					temp_prefix = prefix + '.';
				else temp_prefix = "";
				
				list.addAll(get_classes(path, temp_prefix + file_name));
			}//end if (drill down)
			
			else{
				if (file_name.endsWith(".java")){
					file_name = file_name.replace(".java", "");
					
					if (file_name.endsWith("Test") && !file_name.contains("Abstract"))
						list.add(Class.forName(prefix + '.' + file_name));	
				}//end if
			}//end super if
		}//end for (files)
		
		//wrap
		return list;
	}
	
	
	/*********************************************
	 * Gets all the Testing classes.
	 * @return All the relevant Testing classes.
	 * @throws IOException
	 * @throws ClassNotFoundException
	 *********************************************/
	private static LinkedList<Class<?>> get_classes() throws ClassNotFoundException, IOException{
		return get_classes(tests_dir.toPath(), "");
	}
	
	
	/**********************************
	 * Tests runner.
	 * Using JUnit code.
	 * @throws IOException 
	 * @throws ClassNotFoundException 
	 **********************************/
    public static void run_all_tests() throws ClassNotFoundException, IOException{
    	//print classes to be processed
    	print_classes();
    	
    	//initialize JUnit core
    	org.junit.runner.JUnitCore junit = new org.junit.runner.JUnitCore();
    	TestsListener listener  = new TestsListener();
    	junit.addListener(listener); //enabling logging capability
    	
    	//get classes
    	LinkedList<Class<?>> classes = get_classes();
    	
    	//cast to array
    	Class<?>[] class_array = new Class<?>[classes.size()];
    	Iterator<Class<?>> iterator = classes.iterator();
    	int i = 0;
    	while(iterator.hasNext()){
    		class_array[i] = iterator.next();
    		i++;
    	}
    		
    	//run tests
    	org.junit.runner.Result result = junit.run(class_array);
    	List<Failure> failed = result.getFailures(); //aquire failed tests
    	
    	//wrap
    	dump_to_disk(failed);
    }
    
    
    /*************************************************
     * Dumps the failing tests knowledge to the disk.
     * @param failed - List of failed tests.
     * @throws IOException 
     *************************************************/
    private static void dump_to_disk(List<Failure> failed) throws IOException{
    	//clear the file
    	if (failures_file_cleared == false){
        	PrintWriter writer = new PrintWriter(new FileWriter(fail_list_file, false));
        	writer.print("");
        	writer.close();
        	
        	failures_file_cleared = true;
    	}

    	
    	//write to file
    	PrintWriter writer = new PrintWriter(new FileWriter(fail_list_file, true));
    	String class_name = "";
    	String method_name = "";
    	
    	Description current_desc;
    	Iterator<Failure> iterator = failed.iterator();
    	while(iterator.hasNext()){
    		current_desc = iterator.next().getDescription();
    		method_name = current_desc.getMethodName();
    		class_name = current_desc.getClassName();
    		
    		//avoid missclassified classes
    		if (class_name.contains("initializationError") || method_name.contains("initializationError"))
    			continue;
    		
    		writer.println(class_name + '.' + method_name);
    	}//end while
    	
    	writer.close();
    }
    
    
    /*****************************************************************
     * Runs the tests that exists at remote location (other project).
     * Holds until all tests are done.
     * @throws IOException
     * @throws InterruptedException
     *****************************************************************/
    synchronized public static void run_from_remote(String args) throws IOException, InterruptedException{
    	//parse args
    	args = parse_args(args);
    	
    	set_tests_path(new File("C:/TOM/eclipse/workspace/Appache Tests/bin"));
    	
    	//declare Build-files
    	File file1 = new File("C:/TOM/eclipse/workspace/Appache Tests/bin");
    	File file2 = new File("C:/TOM/eclipse/plugins/org.hamcrest.core_1.3.0.v201303031735.jar");
    	File file3 = new File("C:/TOM/eclipse/plugins/org.junit_4.11.0.v201303080030/junit.jar");
    	
    	String filesString = "" + '"' + file1.toPath().toRealPath() + ';' + file2.toPath().toRealPath() + ';' + file3.toPath().toRealPath() + '"';
    	
    	Process proc = Runtime.getRuntime().exec("java -classpath " + filesString + " Implant.TestsRunner" + args, null, new File("C:/"));
		InputStream stream = proc.getInputStream();
		BufferedReader buffer = new BufferedReader(new InputStreamReader(stream));
		String last_output = buffer.readLine();
		
		while(last_output == null || !last_output.equals("RFC finished")){
			if (last_output != null)
				System.out.println(last_output);
			
			last_output = buffer.readLine();    		
		}//end while
		
		//wrap
		stream.close();
		System.out.println("RFC finished");
    }
    
    
    /*****************************************************************
     * Runs the tests that exists at remote location (other project).
     * Holds until all tests are done.
     * @throws IOException
     * @throws InterruptedException
     *****************************************************************/
    synchronized public static void run_from_remote() throws IOException, InterruptedException{
    	run_from_remote("");
    }
    
    
    /********************************************************
     * Parses the args string to class name and method name.
     * @param args - args string.
     * @return parsed args.
     ********************************************************/
    synchronized public static String parse_args(String args){
    	//handle base case
    	if (args.equals(""))
    		return "";
    	
    	//initialize
    	String new_args = "";
    	String class_name = "";
    	String method_name = "";
    	boolean deep_log = false;
    	
    	//check if deep logging is requested
    	String[] args_tag = args.split(",");
    	if (args_tag.length > 1){
    		if (args_tag[1].equals("true"))
        		deep_log = true;
    		
    		args = args_tag[0];
    	}

    	
    	//parse class and method names
    	String[] tokens = args.split("\\.");
    	for(int i=0; i < tokens.length - 1; i++)
    		class_name += (tokens[i] + '.');
    	
    	class_name = class_name.substring(0, class_name.length() - 1);
    	method_name = tokens[tokens.length - 1];
    	
    	//process
    	new_args = ' ' + class_name + '#' + method_name;
    	if (deep_log)
    		new_args += '#' + "deep";
    	else new_args += '#' + "normal";
    	
    	//wrap
    	return new_args;
    }
    
    
    /**********************************************************
     * Runs a single test method.
     * @param full_class_name - Full class name.
     * @param method_name - Methd name.
     * @throws ClassNotFoundException when class isn't found.
     * @throws IOException when log file can't be aquired.
     **********************************************************/
    public static void run_single_test(String full_class_name, String method_name, String log_mode) throws ClassNotFoundException, IOException{
    	//handle deep logging mode
    	if (log_mode.equals("deep"))
    		Logger.set_deep_log(); //springy switch!
    	
    	//initialize JUnit core
    	org.junit.runner.JUnitCore junit = new org.junit.runner.JUnitCore();
    	TestsListener listener  = new TestsListener();
    	junit.addListener(listener); //enabling logging capability
    	
    	//fix on class
    	Class<?> clazz = null;
		clazz = Class.forName(full_class_name);
    	
    	//run
    	Request request = Request.method(clazz, method_name);
    	org.junit.runner.Result result = junit.run(request);
    	List<Failure> failed = result.getFailures(); //aquire failed tests
    	
    	//wrap
    	dump_to_disk(failed);
    }
    
    
    /**********************************************************************
     * Prints all the classes in the (already) specified source directory.
     * @throws ClassNotFoundException
     * @throws IOException
     **********************************************************************/
    public static void print_classes() throws ClassNotFoundException, IOException{
    	LinkedList<Class<?>> classes = get_classes();
    	
    	Iterator<Class<?>> iterator = classes.iterator();
    	while(iterator.hasNext())
    		System.out.println(iterator.next());	
    }
    
    
    public static boolean check_test_meets_bug() throws FileNotFoundException{
    	//support reggular Junit run
    	if (now_running.equals(""))
    		return true;
    	
    	//initialize
    	boolean result = false;
    	File file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces/base/" + now_running + ".txt");
    	
    	//process
    	Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
    	String comp;
    	while(scanner.hasNextLine()){
    		comp = scanner.nextLine();
    		if (Bug_Switcher.has_bug(comp)){
    			result = true;
    			break;
    		}
    	}
    	
    	//wrap
    	scanner.close();
    	return result;
    }
    
    
    
    /**********************************************************************************************
     **************************************** MAIN  ***********************************************
     **********************************************************************************************/
    synchronized public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException{
    	//beep!
    	Toolkit.getDefaultToolkit().beep();
    	
    	//parse args
    	String[] params = null;
    	if(args.length >= 1 && args[0].contains("#"))
    		params = args[0].split("#");
    	
        //run tests
        System.out.println("Run tests...");
        if (params != null)
        	run_single_test(params[0], params[1], params[2]);
        
        else run_all_tests();
        
        //wrap
        System.out.println("RFC finished");
        System.exit(0);
    }
}
