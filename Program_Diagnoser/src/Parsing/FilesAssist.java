package Parsing;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;

import static java.nio.file.StandardCopyOption.*;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.Set;

import Experimenter.ExperimentInstance;
import Planner.Test;
import Planner.Tests_Pool;

public class FilesAssist {
	//paths
	final private static Path tagged_path = 	 new File("C:/Users/amir/workspace/Program_Diagnoser/tagged").toPath();
	final private static Path traces_path = 	 new File("C:/Users/amir/workspace/Program_Diagnoser/traces").toPath();
	final private static Path base_traces_path = new File("C:/Users/amir/workspace/Program_Diagnoser/traces/base").toPath();
	final private static Path temp_path = 		 new File("C:/Users/amir/workspace/Program_Diagnoser/temp").toPath();
	public static Path instances_path ;// = 	 new File("C:/GitHub/agent/experimentsPacks3/planner").toPath();
	public static String outPath ;//= 	 new File("./results/records/").toPath().toString();
	final private static Path log_source_path = FileSystems.getDefault().getPath("src/Implant");
	
	//files
	final private static File has_bugs_file = 		new File("C:/Users/amir/workspace/Program_Diagnoser/src/Implant/has_bugs.txt");
	final private static File failed_tests_file = 	new File("C:/Users/amir/workspace/Program_Diagnoser/src/Implant/failed_tests.txt");
	final private static File conversion_table = 	new File("C:/GitHub/agent/experiments2BugsTimes3/planner/conv_comp_table2.csv"); 
	final private static File experiment_records = 	new File("C:/Users/amir/workspace/Program_Diagnoser/experiment_records.csv");
	
	//other
	private static Path source_path = FileSystems.getDefault().getPath("");
	private static File[] trace_files = null;
	private static File[] base_trace_files = null;
	private static File[] benchmark_files = null;
	
	/***********************************************
	 * Tagged classes path getter.
	 * @return the path for saving tagged classes.
	 ***********************************************/
	public static Path get_tagged_path(){
		return tagged_path;
	}
	
	/****************************************
	 * WB Instances path getter.
	 * @return the path to the WB instances.
	 ****************************************/
	public static Path get_instances_path(){
		return instances_path;
	}
	
	
	/************************
	 * Has-bugs-file getter.
	 ************************/
	public static File get_has_bugs_file(){
		return has_bugs_file;
	}
	
	
	/****************************
	 * Failed-tests-file getter.
	 ****************************/
	public static File get_failed_tests_file(){
		return failed_tests_file;
	}
	
	
	/************************
	 * temp path getter.
	 ************************/
	public static Path get_temp_path(){
		return temp_path;
	}
	
	
	/**********************************************
	 * Source path getter.
	 * @return the path for saving tagged classes.
	 **********************************************/
	public static Path get_source_path(){
		return source_path;
	}
	
	
	/*******************************************************
	 * Source path setter. 
	 * @param path - Path of the source files to be tagged.
	 *******************************************************/
	public static void set_source_path(Path path){
		source_path = path;
	}
	
	
	/********************************************
	 * Creates a backup copy of the given files.
	 * Stores them in the temp filder.
	 * @param files - Files to be backuped.
	 * @throws IOException
	 ********************************************/
	public static void backup_files(File[] files) throws IOException{
		//make sure temp dir exists
		if (! Files.exists(temp_path))
			Files.createDirectory(temp_path);
		
		String temp_name;
		for(int i=0; i < files.length; i++){
			temp_name = files[i].getName();
			Files.copy(files[i].toPath(), temp_path.resolve(temp_name),REPLACE_EXISTING);
		}
	}
	
	
	/************************************************
	 * Restores the given backuped files.
	 * Deletes the backup copies after restoration!!
	 * @param files - Files to be restored.
	 * @throws IOException
	 ************************************************/
	public static void restore_files(File[] files) throws IOException{
		Path backup_source;
		String temp_name;
		
		for(int i=0; i < files.length; i++){
			temp_name = files[i].getName();
			backup_source = temp_path.resolve(temp_name);
			Files.move(backup_source, files[i].toPath(),REPLACE_EXISTING);
		}
	}
	
	
	/*******************************************************
	 * Creates the tagged classes directory.
	 * @throws IOException when directory can't be created.
	 *******************************************************/
	public static void create_tagged_dir() throws IOException{
		if (! Files.exists(tagged_path))
			Files.createDirectory(tagged_path);

	}
	
	
	/****************************************************
	 * Implants Logger and Bug-Switcher files.
	 * @throws IOException when logger can't be created.
	 ****************************************************/
	public static void plant_directory() throws IOException{
		//get fix on Log directory
		Path log_dest_path = source_path.resolve("Implant");
		
		//create the Log directory when needed
		if (! Files.exists(log_dest_path))
			Files.createDirectory(log_dest_path);
		
		//copy the Logger.java and bug_switcher files
		Files.copy(log_source_path.resolve("Logger.java"), 			log_dest_path.resolve("Logger.java"),REPLACE_EXISTING);
		Files.copy(log_source_path.resolve("has_bugs.txt"), 		log_dest_path.resolve("has_bugs.txt"),REPLACE_EXISTING);
		Files.copy(log_source_path.resolve("failed_tests.txt"), 	log_dest_path.resolve("failed_tests.txt"),REPLACE_EXISTING);
		Files.copy(log_source_path.resolve("Bug_Switcher.java"), 	log_dest_path.resolve("Bug_Switcher.java"),REPLACE_EXISTING);
		Files.copy(log_source_path.resolve("TestsListener.java"), 	log_dest_path.resolve("TestsListener.java"),REPLACE_EXISTING);
		Files.copy(log_source_path.resolve("TestsRunner.java"), 	log_dest_path.resolve("TestsRunner.java"),REPLACE_EXISTING);
		
		System.out.println("Files were planted at: " + log_dest_path);
	}
	
	
	/*********************************************************
	 * Gets all the Java files in the source path.
	 * @return Array of the .java files found.
	 * @throws IOException when error occurs while streaming.
	 *********************************************************/
	public static File[] get_all_java_files() throws IOException{		
		return get_files_from(source_path, ".java", true);  //use drill down mode
	}
	
	
	/*********************************************************
	 * Gets all the (regular) trace files in the source path.
	 * @return Array of the trace(.txt) files found.
	 * @throws IOException when error occurs while streaming.
	 *********************************************************/
	public static File[] get_trace_files() throws IOException{		
		if (trace_files == null)
			trace_files = get_files_from(traces_path, ".txt", false);
		
		return trace_files;
	}
	
	
	/*********************************************************
	 * Gets all the benchmark files in the source path.
	 * @return Array of the instances(.txt) files found.
	 * @throws IOException when error occurs while streaming.
	 *********************************************************/
	public static File[] get_all_benchmark_files() throws IOException{		
		if (benchmark_files == null)
			benchmark_files = get_files_from(instances_path, ".txt", false);
		
		return benchmark_files;
	}
	
	
	/*********************************************************
	 * Gets all the *base* trace files in the source path.
	 * @return Array of the trace(.txt) files found.
	 * @throws IOException when error occurs while streaming.
	 *********************************************************/
	public static File[] get_base_trace_files() throws IOException{		
		if (base_trace_files == null)
			base_trace_files = get_files_from(base_traces_path, ".txt", false);
		
		return base_trace_files; 
	}
	
	
	/**********************************
	 * Traces path getter.
	 * @return the path of the traces.
	 **********************************/
	public static Path get_traces_path(){
		return traces_path;
	}
	
	
	/***************************************
	 * Base traces path getter.
	 * @return the path of the base traces.
	 ***************************************/
	public static Path get_base_traces_path(){
		return base_traces_path;
	}
	
	
	/********************************************************************
	 * Conversion table file getter.
	 * @return the CSV file of the components-to-index conversion table.
	 ********************************************************************/
	public static File get_conv_table_file(){
		return conversion_table;
	}
	
	
	/*****************************************************************
	 * Experiment records file getter.
	 * @return the CSV file of the records-keeping of the experiment.
	 * @throws IOException 
	 *****************************************************************/
	public static File get_experiment_records_file() throws IOException{
		return experiment_records;
	}
	
	
	/*************************************************************************
	 * Gets all files found in the given directory of the specified type.
	 * @param path - Path to aquire files.
	 * @param ending - type of files to aquire.
	 * @param drill_down - Whether or not to drill down to sub-directories.
	 * @return All files found in the given directory of the specified type.
	 * @throws IOException when files can't be aquired.
	 *************************************************************************/
	public static File[] get_files_from(Path path, String ending, boolean drill_down) throws IOException{
		//get ready
		DirectoryStream<Path> stream = Files.newDirectoryStream(path);
		LinkedList<File> list = new LinkedList<File>();
		File temp_file = null;
		
		//process
		for (Path file: stream){
			temp_file = new File(file.toUri());
			if (file.toString().endsWith(ending)){
				list.add(temp_file);
			}//end if (java file)
			
			//handle drill down mode
			else if (drill_down && temp_file.isDirectory()){
				File[] other_files = get_files_from(file, ending, drill_down);
				
				for(int i=0; i < other_files.length; i++)
					list.add(other_files[i]);
			}
		}//end for (files)
		
		//convert list to array
		File[] files = new File[list.size()];
		Iterator<File> iterator = list.iterator();
		int i = 0;
		while(iterator.hasNext()){
			files[i] = iterator.next();
			i++;
		}//end while
		
		stream.close();
		return files;
	}
	
	
	/***********************************************
	 * Loads failed tests list (Workbench mode).
	 * @param pool - Tests Pool.
	 * @param ei - Experiment Instance.
	 * @return an array of true outcomes knowledge.
	 ***********************************************/
	public static int[] load_failed_tests_knowledge(Tests_Pool pool, ExperimentInstance ei){
		//initialize
		int[] result = new int[pool.size()];
		for(int i=0; i < result.length; i++)
			result[i] = 0; //passed
		
		//process
		Set<String> failed_set = ei.get_failed_tests();
		Test current_test;
		for(int i=0; i < pool.size(); i++){
			current_test = pool.get_test(i);
			if (failed_set.contains(current_test.get_name()))
				result[i] = 1;  //failed
		}//end for
		
		//wrap
		return result;
	}
	
	
	/************************************************
	 * Loads failed tests list (Free mode).
	 * @param pool - Tests Pool.
	 * @return an array of true outcomes knowledge.
	 * @throws FileNotFoundException 
	 ************************************************/
	public static int[] load_failed_tests_knowledge(Tests_Pool pool) throws FileNotFoundException{
		//get ready
		File file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/src/Implant/failed_tests.txt");
		int[] result = new int[pool.size()];
		HashSet<String> failed = new HashSet<String>();
		Scanner scanner = null;
		
		//initialize result
		for(int i=0; i < result.length; i++)
			result[i] = 0; //passed
		
		//load file
		scanner = new Scanner(new BufferedReader(new FileReader(file)));

		
		while(scanner.hasNextLine())
			failed.add(scanner.nextLine());
		
		//generate data structure
		Test current_test;
		for(int i=0; i < pool.size(); i++){
			current_test = pool.get_test(i);
			if (failed.contains(current_test.get_name()))
				result[i] = 1;  //failed
		}//end for
		
		//wrap
		scanner.close();
		return result;
	}
	
	
	/////////////////////////////FOR DEBUG////////////////////////////////////////
	public static void main(String[] args) throws IOException{
		File file = new File("C:/tom/eclipse/workspace/Program_Diagnoser/result_matrix.csv");
		File[] files = {file};
		
//		backup_files(files);
		restore_files(files);
	}
}
