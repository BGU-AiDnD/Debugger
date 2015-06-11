package Experimenter;
import Implant.*;




import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

import Parsing.Utils;
import Planner.Test;
import Planner.Tests_Pool;

public class ExperimentInstance {
	
	private Set<String> bugs;
	private Set<String> initial_tests;
	private Set<String> failed_tests;
	private Tests_Pool pool;
	
	public ExperimentInstance(Set<String> bugs, 
			Set<String> initial_tests, 
			Set<String> failed_tests, 
			Tests_Pool pool	){
		this.bugs = bugs;
		this.initial_tests=initial_tests;
		this.failed_tests=failed_tests;
		this.pool = pool;
	}
	
	public Tests_Pool get_pool(){
Logger.log("ExperimentInstance.get_pool");
boolean _bug_switch = Bug_Switcher.has_bug("ExperimentInstance.get_pool");
if (_bug_switch)
	return null;

		return pool;
	}
	public Set<String> get_failed_tests(){
Logger.log("ExperimentInstance.get_failed_tests");
boolean _bug_switch = Bug_Switcher.has_bug("ExperimentInstance.get_failed_tests");
if (_bug_switch)
	return null;

		return failed_tests;
	}
	public Set<String> get_initial_tests() {
Logger.log("ExperimentInstance.get_initial_tests");
boolean _bug_switch = Bug_Switcher.has_bug("ExperimentInstance.get_initial_tests");
if (_bug_switch)
	return null;

		return initial_tests;
	}	
	
	
	/**
	 * Output to file
	 * 
	 * @param instance_file
	 * @throws IOException 
	 */
	public void write_to_file(File instance_file) throws IOException{
Logger.log("ExperimentInstance.write_to_file");
boolean _bug_switch = Bug_Switcher.has_bug("ExperimentInstance.write_to_file");
if (_bug_switch)
	return;

		PrintWriter writer = new PrintWriter(new FileWriter(instance_file, false));

		// Bugs
		writer.println("[Bugs]");
		for(String bug: bugs)
			writer.println(bug);
		
		// Initial tests
		writer.println("[InitialTests]");
		for(String test : initial_tests)
			writer.println(test);
		
		// Print test details
		writer.println("[TestDetails]");
		Test test;
		int[] comps;
		for(int i=0;i<pool.size();i++){
			test = pool.get_test(i);
			
			writer.print(test.get_name()+";");
			comps = test.get_base_comps();
			if(comps==null)
				writer.print("null");
			else
				writer.print(Arrays.toString(comps));

			writer.print(";");
			writer.print(Utils.intArrayToString(test.get_part_comps()));
			writer.print(";");
			if(failed_tests.contains(test))
				writer.println(1);
			else 
				writer.println(0);			
		}
		writer.close();
	}
	
	/**
	 * Read from file
	 * 
	 * @param instance_file
	 * @param coder_file
	 * @throws IOException 
	 */
	public static ExperimentInstance read_from_file(File file) throws IOException{
Logger.log("ExperimentInstance.read_from_file");
boolean _bug_switch = Bug_Switcher.has_bug("ExperimentInstance.read_from_file");
if (_bug_switch)
	return null;

		Set<String> new_bugs = new HashSet<String>();
		Set<String> new_initial_tests = new HashSet<String>();
		Set<String> new_failed_tests = new HashSet<String>();
		Set<Test> tests = new HashSet<Test>();
		Test test;	
		Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
		String state = "start";
		String line;
		String test_name;
		String[] line_parts;
		int[] base_comps;
		int[] part_comps;
		
		// Fill bugs, initial tests and failed tests
		while(scanner.hasNextLine()){
			line = scanner.nextLine();
			
			switch(state){
			case "start":
				if(line.equals("[Bugs]")){
					state="bugs";
					continue;
				}			
				
			break;
			case "bugs":
				if(line.equals("[InitialTests]")){
					state="initial-tests";
					continue;
				}	
				new_bugs.add(line);			
				
			break;
			case "initial-tests":
				if(line.equals("[TestDetails]")){
					state="test-details";
					continue;
				}	
				new_initial_tests.add(line);
				
			break;
			case "test-details":
				line_parts = line.split(";");
				
				// Name and part_comps
				test_name = line_parts[0];
				part_comps = Utils.stringToIntArray(line_parts[1]);
				test = new Test(part_comps, test_name);
				
				// Base_comps
				if(line_parts[2].equals("null"))
					base_comps=null;
				else
					base_comps = Utils.stringToIntArray(line_parts[2]);
				test.set_base_comps(base_comps);
				
				// Outcome
				if(line_parts[3].equals("1"))
					new_failed_tests.add(test_name);
				
				tests.add(test);
			break;					
			}			
		}
		scanner.close();
				
		// Fill pool
		Tests_Pool pool = new Tests_Pool();
		for(Test test_to_add: tests)
			pool.add_test(test_to_add);	
		
		return new ExperimentInstance(new_bugs, new_initial_tests, new_failed_tests, pool);
	}
}
