package Experimenter;
import Implant.*;

import Implant.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.Set;

import org.apache.commons.io.FileUtils;

import Implant.TestsRunner;
import Parsing.FilesAssist;
import Parsing.TraceToCode;
import Planner.StateKey;
import Planner.Test;
import Planner.Tests_Pool;

public class InstanceGenerator {

	private TraceToCode testsCoder = new TraceToCode();
	private Tests_Pool pool = new Tests_Pool();
	
	public InstanceGenerator(boolean load_conversion_table) throws FileNotFoundException, IOException, InterruptedException{
		if(load_conversion_table){
			testsCoder.load_conversion_table(new File(TestsRunner.COMPONENT_INDEX_TABLE));
			testsCoder.addFilesToPool(pool, FilesAssist.get_base_trace_files());
		}
		else{
			load_code_and_traces();
		}
	}
	
	/**
	 * Runs tests without bugs and analyze their trace, output the conversion table and update the pool
	 * 
	 * @throws IOException
	 * @throws InterruptedException 
	 */
	private void load_code_and_traces() throws IOException, InterruptedException{
Logger.log("InstanceGenerator.load_code_and_traces");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.load_code_and_traces");
if (_bug_switch)
	return;

		// Runs the code without bug
		write_bugs(new HashSet<String>());		
		TestsRunner.run_from_remote();
		
		FileUtils.copyDirectory(FilesAssist.traces_path.toFile(),
				FilesAssist.base_traces_path.toFile());
				
		// Analyze traces to extract tests and components
		testsCoder = new TraceToCode();
		
		pool = new Tests_Pool();
		testsCoder.addFilesToPool(pool, FilesAssist.get_base_trace_files());
		testsCoder.store_conversion_table(new File(TestsRunner.COMPONENT_INDEX_TABLE));
	}
	
	/*************************************************
	 * Randomize components to simulate bugs in them.
	 *************************************************/
	private Set<String> randomize_bugs(double asked_ratio){
Logger.log("InstanceGenerator.randomize_bugs");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.randomize_bugs");
if (_bug_switch)
	return null;


		//initialize
		double ratio = 0;
		Set<String> random_comps = new HashSet<String>();

		int comps_num = testsCoder.get_comps_num();
		String temp_comp;
		
		//process
		while(ratio < asked_ratio){
			//raffle component
			temp_comp = testsCoder.raffle_component().getKey();
			random_comps.add(temp_comp);
			
			//adjust ratio
			ratio = (double)random_comps.size() / comps_num;
		}//end while
		
		//wrap
		return random_comps;
	}
	
	
	/**
	 * Activate a set of given bug names before running
	 * @param method_names the names of the methods where to activate the bugs
	 * @returns an array of test outcomes
	 * @throws IOException
	 */
	private int[] run_tests(Set<String> method_with_bugs) throws IOException {
Logger.log("InstanceGenerator.run_tests");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.run_tests");
if (_bug_switch)
	return null;


		////generate random bugs and decide tests results (run tests!)
		//simulate bugs
		//get ready
		//HashSet<String> random_comps = get_random_comps(TDP_Run.random_bugs_ratio);
		
		this.write_bugs(method_with_bugs);
		
		//run tests
		System.out.println("\nRun tests to collect traces...");
		try {
			TestsRunner.run_from_remote();
			System.out.println("Finished running tests!");
		} catch (InterruptedException e) {
			System.out.println("Exception while running tests :(");
			e.printStackTrace();
		}
		
		
		// Update the outcome of tests, given the activated bugs
		Test test;
		for(int i=0;i<pool.size();i++){
			test = pool.get_test(i);
			test.update_after_fail(testsCoder);
		}
						
		return FilesAssist.load_failed_tests_knowledge(pool);				
	}

	/**
	 * Writes a bugs file has_bugs.txt for the given set of method names that are assumed to have a bug
	 * @param method_with_bugs set of method names
	 * @throws IOException
	 */
	private void write_bugs(Set<String> method_with_bugs) throws IOException {
Logger.log("InstanceGenerator.write_bugs");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.write_bugs");
if (_bug_switch)
	return;

		File bugs_file = new File(Implant.TestsRunner.HAS_BUGS_PATH);
				
		//clear file
		PrintWriter writer = new PrintWriter(new FileWriter(bugs_file, false));
		
		//process
		for(String method_name : method_with_bugs){
			System.out.println("->" + method_name);
			writer.println(method_name);
		}
		//wrap
		writer.close();
		System.out.println("Bugs were activated.");
	}	
	

	
	/**
	 * Choose randomly a set of initial tests. 
	 * @param num
	 * @return
	 */
	private Set<String> randomize_initial_tests(int num_of_initials, int[] actual_test_result){
Logger.log("InstanceGenerator.randomize_initial_tests");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.randomize_initial_tests");
if (_bug_switch)
	return null;

		//declare vars
		int t;
		Set<String> result = new HashSet<String>();
		
		//process
		int i = 0;
		boolean has_bug = false;
		while( i < num_of_initials ){
			if((i==num_of_initials-1) && (has_bug==false)){
				List<Integer> failed_tests = new ArrayList<Integer>();
				for(int test_index=0;test_index<actual_test_result.length;test_index++)
					if (actual_test_result[test_index]==1)
						failed_tests.add(test_index);						
				if(failed_tests.size()==0)
					throw new RuntimeException("No failed tests in instance!");
				int random_index = new Random().nextInt(failed_tests.size());
				t = failed_tests.get(random_index).intValue();
			}
			else{
				t = pool.raffle_a_test();
			}
			
			pool.block_test(t);
			
			//update bug flag
			if (actual_test_result[t] == 1)
				has_bug = true;
			
			result.add(pool.get_test(i).get_name());
			i++;						
		}//end while	
		
		return result;
	}


	
	/**
	 * Generate a random instance
	 * @param asked_ratio fault probabiltiy
	 * @param num_of_initials num of initial tests
	 * 
	 * @return a new, randomly generated instance
	 * @throws IOException 
	 */
	public ExperimentInstance generateInstance(double asked_ratio, int num_of_initials) throws IOException{
Logger.log("InstanceGenerator.generateInstance");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.generateInstance");
if (_bug_switch)
	return null;

		Set<String> bugs = randomize_bugs(asked_ratio);
		
		System.out.println(bugs);
		
		int[] test_outcomes = run_tests(bugs); // Also update test pool
		Set<String> failedTests = new HashSet<String>();
		for(int i=0;i<test_outcomes.length;i++)
			if(test_outcomes[i]==1)
				failedTests.add(pool.get_test(i).get_name());
		
		System.out.println(failedTests);
		
		Set<String> initial_tests = randomize_initial_tests(num_of_initials, test_outcomes);
		
		return new ExperimentInstance(bugs, initial_tests,failedTests, pool);
	}
	
	
	/**
	 * Generate a set of instances
	 * @param args
	 * @throws IOException
	 * @throws InterruptedException 
	 */
	public static void main(String[] args) throws IOException, InterruptedException{
Logger.log("InstanceGenerator.main");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGenerator.main");
if (_bug_switch)
	return;

		double asked_ratio = 0.001;
		int num_of_initials = 4;
		InstanceGenerator generator = new InstanceGenerator(true);
		ExperimentInstance instance;
		String file_prefix = "c:/temp/instance";
		File output;
		
		for(int i=0;i<1;i++){
			instance = generator.generateInstance(asked_ratio, num_of_initials);
			output = new File(file_prefix+i+".txt");
			
			instance.write_to_file(output);
		}
			
	}
}
