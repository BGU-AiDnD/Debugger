package Experimenter;

import java.awt.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.Set;
import java.util.StringTokenizer;

import Parsing.Utils;
import Planner.Test;
import Planner.Tests_Pool;

public class ExperimentInstance {
	
	private String name;
	private Set<String> bugs;
	private Set<String> initial_tests;
	private Set<String> failed_tests;
	private Tests_Pool pool;
	public static double[] priors;
	
	/*********************************************
	 * Constructor.
	 * @param bugs - Bugs set.
	 * @param initial_tests - Initial tests set.
	 * @param failed_tests - Failed tests set.
	 * @param pool - Pool of tests.
	 *********************************************/
	public ExperimentInstance(String name, 
			Set<String> bugs, 
			Set<String> initial_tests, 
			Set<String> failed_tests, 
			Tests_Pool pool	){
		
		this.name = name;
		this.bugs = bugs;
		this.initial_tests=initial_tests;
		this.failed_tests=failed_tests;
		this.pool = pool;
	}
	

	/**************************
	 * Tests pool getter.
	 * @return the tests-pool.
	 **************************/
	public Tests_Pool get_pool(){
		return pool;
	}
	
	
	/************************************
	 * Name getter.
	 * @return the name of the instance.
	 ************************************/
	public String get_name(){
		return name;
	}
	
	
	/****************************************************
	 * Bugged methods getter.
	 * @return a set of the names of the bugged methods.
	 ****************************************************/
	public Set<String> get_bugs(){
		return bugs;
	}
	
	
	/******************************************
	 * Failed tests getter.
	 * @return the idices of the failed tests.
	 ******************************************/
	public Set<String> get_failed_tests(){
		return failed_tests;
	}
	
	
	/********************************************************************************
	 * Initial tests getter.
	 * @return the indices of the tests that are to be present in the intial matrix.
	 ********************************************************************************/
	public Set<String> get_initial_tests() {
		return initial_tests;
	}	
	
	
	/************************
	 * Output to file.
	 * @param instance_file.
	 * @throws IOException 
	 ************************/
	public void write_to_file(File instance_file) throws IOException{
		//create file
		if (!instance_file.exists())
			instance_file.createNewFile();
		
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
			if(failed_tests.contains(test.get_name()))
				writer.println(1);
			else 
				writer.println(0);			
		}
		writer.close();
	}
	
	/**************************************************
	 * Reads an instance file.
	 * @param instance_file.
	 * @param coder_file.
	 * @return an instance object to experiment with.
	 * @throws IOException. 
	 **************************************************/
	public static ExperimentInstance read_from_file(File file) throws IOException{
		Set<String> new_bugs = new HashSet<String>();
		Set<String> new_initial_tests = new HashSet<String>();
		Set<String> new_failed_tests = new HashSet<String>();
		LinkedList<Test> tests = new LinkedList<Test>();
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
				if(line.equals("[Priors]")){
					state="priors";
					continue;
				}		
				
					
			break;
			case "priors":
				if(line.equals("[Bugs]")){
					state="bugs";
					continue;
				}			
				line=line.substring(1,line.length()-1);
				StringTokenizer st=new StringTokenizer(line, ",");
				LinkedList<Double> l=new LinkedList<Double>();
				while(st.hasMoreElements())
					l.add(Double.parseDouble(st.nextToken()));
				priors= new double[l.size()];
				int i=0;
				for(Double d:l){
					priors[i]=d.doubleValue();
					i++;
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
				
				//participating (actual) comps
				test.set_part_comps(part_comps);
				
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
		
		return new ExperimentInstance(file.getName().replace(".txt", ""),new_bugs, new_initial_tests, new_failed_tests, pool);
	}
	
	
	/*********************************************************************************
	 *********************************** For Debug ***********************************
	 *********************************************************************************/
	public static void main(String[] args){
		//initialize
		ExperimentInstance ei = null;
		File file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/instances/_initials_4_ratio_0.001-0.txt");
		
		//try
		try {
			ei = read_from_file(file);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		System.out.println("Done. " + ei.toString());
	}
}
