package Implant;
import Implant.*;


import java.awt.Toolkit;
import java.io.BufferedReader;
import java.io.File;
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

import org.junit.Test;
import org.junit.runner.Description;
import org.junit.runner.Request;
import org.junit.runner.notification.Failure;

import Implant.Logger;


public class TestsRunner {
	//public static String WORKSPACE_PATH = "c:/tom/eclipse/workspace/Program_Diagnoser"
	public static String WORKSPACE_PATH = "C:/projects/Program_Diagnoser";

	//public static String APACHE_COMMONS_MATH_PATH = "/tom/workspace/diagnoser/Appache Tests";
	public static String APACHE_COMMONS_MATH_PATH = "/Users/user/workspace/diagnoser/Appache Tests";

	//private static String ECLIPSE_PATH = "C:/TOM/eclipse";	
	private static String ECLIPSE_PATH = "C:/Tools/eclipse";
	
	public static String APACHE_COMMONS_MATH_SRC = APACHE_COMMONS_MATH_PATH + "/src";
	public static String APACHE_COMMONS_MATH_BIN = APACHE_COMMONS_MATH_PATH + "/bin";
	public static String COMPONENT_INDEX_TABLE = WORKSPACE_PATH+"/conv_comp_table.csv";	
	public static String BENCHMARK_PATH = WORKSPACE_PATH+"/benchmark/";
		
	
	private static File tests_dir = new File(APACHE_COMMONS_MATH_SRC);
	public static Object lock = new Object();
	private static boolean failures_file_cleared = false;
	
	private static File FAILED_TEST_FILE;
	public static String IMPLANT_PATH;
	public static String HAS_BUGS_PATH;
	
	static{
		IMPLANT_PATH = Thread.currentThread().getContextClassLoader().getResource("Implant/").getPath();
		HAS_BUGS_PATH = IMPLANT_PATH + "/has_bugs.txt";		
		FAILED_TEST_FILE = new File(IMPLANT_PATH + "/failed_tests.txt");
	}
	
	@Test
	public void testToast() throws Exception{
Logger.log("TestsRunner.testToast");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.testToast");
if (_bug_switch)
	return;

		Logger.log("TestsRunner.testToast");
		boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.testToast");
		if (_bug_switch)
			throw new Exception("toast");
	}
	
	
	/*********************************
	 * Failed tests list file setter.
	 * @param file - File.
	 *********************************/
	public static void set_fail_list_file(File file){
Logger.log("TestsRunner.set_fail_list_file");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.set_fail_list_file");
if (_bug_switch)
	return;

		FAILED_TEST_FILE = file;
	}
	
	
	/***************************
	 * Tests path setter.
	 * @param path - Dir path.
	 * @throws IOException 
	 ***************************/
	public static void set_tests_path(File dir) throws IOException{
Logger.log("TestsRunner.set_tests_path");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.set_tests_path");
if (_bug_switch)
	return;

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
Logger.log("TestsRunner.get_classes");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.get_classes");
if (_bug_switch)
	return null;

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
Logger.log("TestsRunner.get_classes");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.get_classes");
if (_bug_switch)
	return null;

		return get_classes(tests_dir.toPath(), "");
	}
	
	
	/**********************************
	 * Tests runner.
	 * Using JUnit code.
	 * @throws IOException 
	 * @throws ClassNotFoundException 
	 **********************************/
    public static void run_all_tests() throws ClassNotFoundException, IOException{
Logger.log("TestsRunner.run_all_tests");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.run_all_tests");
if (_bug_switch)
	return;

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
Logger.log("TestsRunner.dump_to_disk");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.dump_to_disk");
if (_bug_switch)
	return;

    	//clear the file
    	if (failures_file_cleared == false){
        	PrintWriter writer = new PrintWriter(new FileWriter(FAILED_TEST_FILE, false));
        	writer.print("");
        	writer.close();
        	
        	failures_file_cleared = true;
    	}

    	
    	//write to file
    	PrintWriter writer = new PrintWriter(new FileWriter(FAILED_TEST_FILE, true));
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
Logger.log("TestsRunner.run_from_remote");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.run_from_remote");
if (_bug_switch)
	return;

    	//parse args
    	args = parse_args(args);
    	
    	set_tests_path(new File(APACHE_COMMONS_MATH_BIN));
    	
    	//declare Build-files
    	File file1 = new File(APACHE_COMMONS_MATH_BIN);
    	File file2 = new File(ECLIPSE_PATH+"/plugins/org.hamcrest.core_1.3.0.v201303031735.jar");
    	File file3 = new File(ECLIPSE_PATH+"/plugins/org.junit_4.11.0.v201303080030/junit.jar");
    	
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
Logger.log("TestsRunner.run_from_remote");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.run_from_remote");
if (_bug_switch)
	return;

    	run_from_remote("");
    }
    
    
    /********************************************************
     * Parses the args string to class name and method name.
     * @param args - args string.
     * @return parsed args.
     ********************************************************/
    synchronized public static String parse_args(String args){
Logger.log("TestsRunner.parse_args");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.parse_args");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

    	//handle base case
    	if (args.equals(""))
    		return "";
    	
    	//initialize
    	String new_args = "";
    	String class_name = "";
    	String method_name = "";
    	
    	//parse class and method names
    	String[] tokens = args.split("\\.");
    	for(int i=0; i < tokens.length - 1; i++)
    		class_name += (tokens[i] + '.');
    	
    	class_name = class_name.substring(0, class_name.length() - 1);
    	method_name = tokens[tokens.length - 1];
    	
    	//process
    	new_args = ' ' + class_name + '#' + method_name;
    	
    	//
    	return new_args;
    }
    
    
    /**********************************************************
     * Runs a single test method.
     * @param full_class_name - Full class name.
     * @param method_name - Methd name.
     * @throws ClassNotFoundException when class isn't found.
     * @throws IOException when log file can't be aquired.
     **********************************************************/
    public static void run_single_test(String full_class_name, String method_name) throws ClassNotFoundException, IOException{
Logger.log("TestsRunner.run_single_test");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.run_single_test");
if (_bug_switch)
	return;

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
Logger.log("TestsRunner.print_classes");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.print_classes");
if (_bug_switch)
	return;

    	LinkedList<Class<?>> classes = get_classes();
    	
    	Iterator<Class<?>> iterator = classes.iterator();
    	while(iterator.hasNext())
    		System.out.println(iterator.next());	
    }
    
    
    
    /**********************************************************************************************
     **************************************** MAIN  ***********************************************
     **********************************************************************************************/
    synchronized public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException{
Logger.log("TestsRunner.main");
boolean _bug_switch = Bug_Switcher.has_bug("TestsRunner.main");
if (_bug_switch)
	return;

    	//beep!
    	Toolkit.getDefaultToolkit().beep();
    	
    	//parse args
    	String[] params = null;
    	if(args.length >= 1 && args[0].contains("#"))
    		params = args[0].split("#");
    	
        //run tests
        System.out.println("Run tests...");
        if (params != null)
        	run_single_test(params[0], params[1]);
        
        else run_all_tests();
        
        //wrap
        System.out.println("RFC finished");
        System.exit(0);
    }
}
