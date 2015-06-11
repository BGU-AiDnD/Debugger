package Experimenter;
import Implant.*;


import Implant.*;

import java.awt.Toolkit;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Set;
import java.util.concurrent.ForkJoinTask;

import Diagnoser.Diagnosis;
import Diagnoser.Dynamic_Spectrum;
import Implant.TestsRunner;
import Infrastrcture.OrderAssist;
import Parsing.FilesAssist;
import Parsing.TraceToCode;
import Planner.StateKey;
import Planner.TDP;
import Planner.Tests_Pool;

public class ExpThread extends ForkJoinTask<Object>{
	//declare vars
	private static final long serialVersionUID = -8201270664406126310L;
	public Hashtable<String, Planner.State> buffer = new Hashtable<String, Planner.State>();
	private int lookahead, samples;
	private double threshold_prob;
	private int[] actual_test_result;
	
	//Diclare initial spectrum holders
	private Dynamic_Spectrum ds = new Dynamic_Spectrum();
	private StateKey base_key= new StateKey();
	
	//Ready structure for tests pool
	private Tests_Pool pool = new Tests_Pool();
	private TraceToCode testsCoder = new TraceToCode();
	
	
	/*************************************************
	 * Constructor.
	 * @param la - lookahead num.
	 * @param s - samples num.
	 * @param buff - states buffer.
	 * @throws IOException when unable to load files.
	 *************************************************/
	public ExpThread() throws IOException{
		this(true);
	}

	public ExpThread(boolean load_data) throws IOException{
		lookahead = TDP_Run.lookahead;
		samples = TDP_Run.samples;
		threshold_prob = TDP_Run.threshold_prob;
			
		//load base traces to pool
		if(load_data){
			File[] file_names = FilesAssist.get_base_trace_files();
			testsCoder.addFilesToPool(pool, file_names);
			System.out.println("\nBase traces were loaded.");
			TDP_Run.set_comps_num(testsCoder.get_comps_num());
			
			//dump components conversion table
			testsCoder.saveConvTable();
			
			if (TDP_Run.bug_simulation_mode == TDP_Run.bug_sim_mode.RANDOMIZE_NEW)
				generate_random_bugs();
	
			actual_test_result = FilesAssist.load_failed_tests_knowledge(pool);
			System.out.println("Finished determining all tests results.");
		}
		else{
			testsCoder.load_conversion_table(new File(TestsRunner.COMPONENT_INDEX_TABLE));			
		}
	}
	
	/**
	 * Generate a set of random bugs
	 * @throws IOException
	 */
	private void generate_random_bugs() throws IOException {
Logger.log("ExpThread.generate_random_bugs");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.generate_random_bugs");
if (_bug_switch)
	return;

		////generate random bugs and decide tests results (run tests!)
		//simulate bugs
		randomize_bugs();
		System.out.println("Bugs were randomized.");
		
		//run tests
		System.out.println("\nRun tests to collect traces...");
		try {
			TestsRunner.run_from_remote();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("Done!");	
	}
	
	/**
	 * Activate a set of given bug names before running
	 * @param method_names the names of the methods where to activate the bugs
	 * @throws IOException
	 */
	private void activate_bugs(String[] method_names) throws IOException {
Logger.log("ExpThread.activate_bugs");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.activate_bugs");
if (_bug_switch)
	return;

		////generate random bugs and decide tests results (run tests!)
		//simulate bugs
		//get ready
		//HashSet<String> random_comps = get_random_comps(TDP_Run.random_bugs_ratio);
		
		File bugs_file = new File(TestsRunner.WORKSPACE_PATH +"/src/Implant/has_bugs.txt");
				
		//clear file
		PrintWriter writer = new PrintWriter(new FileWriter(bugs_file, false));
		
		//process
		for(String method_name : method_names){
			System.out.println("->" + method_name);
			writer.println(method_name);
		}
		//wrap
		writer.close();
		System.out.println("Bugs were activated.");
		
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
		actual_test_result = FilesAssist.load_failed_tests_knowledge(pool);		
		System.out.println("Finished determining all tests results.");

			
	}
	
	
	/*************************************************
	 * Randomize components to simulate bugs in them.
	 *************************************************/
	private void randomize_bugs(){
Logger.log("ExpThread.randomize_bugs");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.randomize_bugs");
if (_bug_switch)
	return;

		//get ready
		HashSet<String> random_comps = get_random_comps(TDP_Run.random_bugs_ratio);
		File bugs_file = new File(TestsRunner.WORKSPACE_PATH +"/src/Implant/has_bugs.txt");
		
		//clear file
		PrintWriter writer = null;
		try {
			writer = new PrintWriter(new FileWriter(bugs_file, false));
			writer.print("");
		} catch (IOException e) {
			e.printStackTrace();
		}
		writer.close();
		
		//re-establish file writer
		try {
			writer = new PrintWriter(new FileWriter(bugs_file, true));
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		//process
		String temp_comp;
		Iterator<String> iterator = random_comps.iterator();
		System.out.println("\nMethods selected for bug injection:");
		while(iterator.hasNext()){
			temp_comp = iterator.next();
			writer.println(temp_comp);
			System.out.println("->" + temp_comp);
		}//end while
		
		//wrap
		writer.close();
	}
	
	
	/************************************************************************
	 * Raffles a specific ratio of random components, out of all components.
	 * @param asked_ratio - Ratio of selected components.
	 * @return random components.
	 ************************************************************************/
	private HashSet<String> get_random_comps(double asked_ratio){
Logger.log("ExpThread.get_random_comps");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.get_random_comps");
if (_bug_switch)
	return null;

		//initialize
		double ratio = 0;
		HashSet<String> random_comps = new HashSet<String>();
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
	
	
	/***********************
	 * Resets tests in pool.
	 ***********************/
	private void reset_tests(){
Logger.log("ExpThread.reset_tests");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.reset_tests");
if (_bug_switch)
	return;

		pool.refresh();
	}
	
	
	/***********************************
	 * Block initial tets (randomized).
	 * @throws FileNotFoundException 
	 ***********************************/
	private void initial_tests_random(){
Logger.log("ExpThread.initial_tests_random");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.initial_tests_random");
if (_bug_switch)
	return;

		//declare vars
		int t;
		base_key = new StateKey();
		
		//process
		int i = 0;
		boolean has_bug = false;
		while( i < TDP_Run.initial_tests_num ){ 
			t = pool.raffle_a_test();
			
			if (i < (TDP_Run.initial_tests_num - 1) || has_bug || actual_test_result[t] == 1){
				pool.block_test(t);
				
				//update bug flag
				if (actual_test_result[t] == 1){
					has_bug = true;
					pool.get_test(t).update_after_fail(testsCoder);
				}
				
				//update spectrum
//				update_spectrum(pool.get_test(t).get_part_comps(),actual_test_result[t]);
				ds.update(pool.get_test(t).get_part_comps(),actual_test_result[t]);
				
				//update base key
				base_key.update_key(t, actual_test_result[t]);
				
				i++;
			}//end if
		}//end while
		
	}
	
	
	/************************************
	 * Block initial tests (predefined).
	 * @param i - predefenition index.
	 ************************************/
	private void initial_tests_predef(){
Logger.log("ExpThread.initial_tests_predef");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.initial_tests_predef");
if (_bug_switch)
	return;

		//declare vars
		boolean has_bug = false;
		int[] tests_vector;
		int i = Predef_Cases.pointer;
		base_key = new StateKey();
		
		//know when finished
		if (Predef_Cases.pointer > Predef_Cases.predef_initial_tests.length - 1)
			return;
		
		//process
		while(i < Predef_Cases.predef_initial_tests.length && !has_bug ){
			tests_vector = Predef_Cases.predef_initial_tests[i];
			for(int t=0; t < tests_vector.length; t++)
				if (actual_test_result[tests_vector[t]] == 1)
					has_bug = true;
			
			if (has_bug){
				Predef_Cases.pointer = i+1; //update static pointer
				
				//update initial matrix
				for(int t=0; t < tests_vector.length; t++){
					//block test
					pool.block_test(tests_vector[t]);
					
					//update spectrum
					ds.update(pool.get_test(tests_vector[t]).get_part_comps(),actual_test_result[tests_vector[t]]);
					
					//update base key
					base_key.update_key(tests_vector[t], actual_test_result[tests_vector[t]]);
				}//end for
			}//end if
			
			i++;
		}//end while	
	}
	
	/************************************
	 * Block given set of initial tests
	 * @param initial_test_names - names of initial tests
	 ************************************/	
	private void initial_tests(Set<String> initial_tests){
Logger.log("ExpThread.initial_tests");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.initial_tests");
if (_bug_switch)
	return;

		//declare vars
		int test_index;
		base_key = new StateKey();
		
		for(String initial_test : initial_tests){
			test_index=pool.get_index(initial_test);
		
			//block test
			pool.block_test(test_index);
			
			//update spectrum
			ds.update(pool.get_test(test_index).get_part_comps(),actual_test_result[test_index]);
			
			//update base key
			base_key.update_key(test_index, actual_test_result[test_index]);				
		}
	}
	
	
	/****************************************************
	 * Block initial tests (according to chosen method).
	 * @throws FileNotFoundException 
	 ****************************************************/
	private void initial_tests(){
Logger.log("ExpThread.initial_tests");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.initial_tests");
if (_bug_switch)
	return;

		switch(TDP_Run.initial_tests_method){
		case PREDEFINED:
			initial_tests_predef();
			break;
			
		case RANDOM:
			initial_tests_random();
			break;
		}//end switch
	}
	
	
	/****************************************
	 * Calculate next test by chosen method.
	 * @param tdp - TDP engine.
	 * @param pool - Tests pool.
	 * @return next test by chosen method.
	 ****************************************/
	private int next_test(TDP tdp, Tests_Pool pool ){
Logger.log("ExpThread.next_test");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.next_test");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		switch(TDP_Run.method_of_choice){
		case RAFFLE:
			return pool.raffle_a_test();
		
		case HP:
			return tdp.best_test_by(TDP_Run.method_types.HP, TDP_Run.debug_mode);
			
		case BD:
			return tdp.best_test_by(TDP_Run.method_types.BD, TDP_Run.debug_mode);
			
		case ENTROPY:
			return tdp.best_test_by(TDP_Run.method_types.ENTROPY, TDP_Run.debug_mode);
			
		case ERP:
			return tdp.best_test_by(TDP_Run.method_types.ERP, TDP_Run.debug_mode);
			
		case MDP_MC:
			return tdp.best_test_by_MDP(TDP_Run.method_types.RAFFLE, TDP_Run.debug_mode);
			
		case MDP_HP:
			return tdp.best_test_by_MDP(TDP_Run.method_types.HP, TDP_Run.debug_mode);
			
		case MDP_BD:
			return tdp.best_test_by_MDP(TDP_Run.method_types.BD, TDP_Run.debug_mode);
			
		case MDP_ENTROPY:
			return tdp.best_test_by_MDP(TDP_Run.method_types.ENTROPY, TDP_Run.debug_mode);
			
		case MDP_ERP:
			return tdp.best_test_by_MDP(TDP_Run.method_types.ERP, TDP_Run.debug_mode);
		
		default: return -1;
		}//end switch
	}
	
	
	/***************************
	 * Synchronized println.
	 * @param string - string.
	 ***************************/
	private void print_result(String string){
Logger.log("ExpThread.print_result");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.print_result");
if (_bug_switch)
	return;

		synchronized(System.out){
			System.out.println(string);
		}
	}
	
	
	/********************************
	 * Prints a list of diagnoses.
	 * @param list - Diagnoses list.
	 ********************************/
	private void print_diagnoses(LinkedList<Diagnosis> list){
Logger.log("ExpThread.print_diagnoses");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.print_diagnoses");
if (_bug_switch)
	return;

		Iterator<Diagnosis> iterator = list.iterator();
		while(iterator.hasNext())
			print_result(iterator.next().toString());
	}
	
	
	/*********************************************************
	 * Precision calculation for a single diagnosis.
	 * @param diagnosis - Diagnosis.
	 * @param has_bugs - Sorted(!) codes for bugged methods.
	 * @return Precision for given diagnosis.
	 *********************************************************/
	private double precision(Diagnosis diagnosis, int[] has_bugs){
Logger.log("ExpThread.precision");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.precision");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize
		double result = 0;
		int[] diag = diagnosis.get_diag();
		int TP = 0;
		int FP = 0;
		
		//process
		for(int i=0; i < diag.length; i++)
			if (OrderAssist.binarySearch(has_bugs, diag[i])) //bug-list is assumed to be sorted!!
				TP++;
			else FP++;
		
		//wrap
		result = (double)TP / (TP + FP);
		return result;
	}
	
	
	/*********************************************************
	 * Recall calculation for a single diagnosis.
	 * @param diagnosis - Diagnosis.
	 * @param has_bugs - codes for bugged methods.
	 * @return Recall for a given diagnosis.
	 *********************************************************/
	private double recall(Diagnosis diagnosis, int[] has_bugs){
Logger.log("ExpThread.recall");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.recall");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize
		double result = 0;
		int TP = 0;
		int FN = 0;
		
		//process
		for(int i=0; i < has_bugs.length; i++)
			if (diagnosis.contains(has_bugs[i])) 
				TP++;
			else FN++;
		
		//wrap
		result = (double)TP / (TP + FN);
		return result;
	}
	
	
	/**************************************************
	 * Precision calculation for a batch of diagnosis.
	 * @param diagnoses - Diagnoses batch.
	 * @return averaged precision of given diagnoses.
	 **************************************************/
	private double precision(LinkedList<Diagnosis> diagnoses){
Logger.log("ExpThread.precision");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.precision");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize
		double result = 0;
		double[] precisions = new double[diagnoses.size()];
		int[] has_bugs = null;
		Iterator<Diagnosis> iterator = diagnoses.iterator();
		Diagnosis current_diag;
		
		//read has-bugs-file
		File file = FilesAssist.get_has_bugs_file();
		try {
			has_bugs = testsCoder.fileToArray(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		//sort bugs - a must!!
		has_bugs = OrderAssist.quickSort(has_bugs);
		
		//process
		int i = 0;
		while(iterator.hasNext()){
			current_diag = iterator.next();
			precisions[i] = precision(current_diag, has_bugs);
			i++;
		}//end while
		
		//average
		for(int d=0; d < precisions.length; d++)
			result += precisions[d];
		
		result /= precisions.length;	
		
		//wrap
		return result;
	}
	
	
	/**************************************************
	 * Precision calculation for a batch of diagnosis.
	 * @param diagnoses - Diagnoses batch.
	 * @return averaged precision of given diagnoses.
	 **************************************************/
	private double recall(LinkedList<Diagnosis> diagnoses){
Logger.log("ExpThread.recall");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.recall");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize
		double result = 0;
		double[] recalls = new double[diagnoses.size()];
		int[] has_bugs = null;
		Iterator<Diagnosis> iterator = diagnoses.iterator();
		Diagnosis current_diag;
		
		//read has-bugs-file
		File file = FilesAssist.get_has_bugs_file();
		try {
			has_bugs = testsCoder.fileToArray(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		//process
		int i = 0;
		while(iterator.hasNext()){
			current_diag = iterator.next();
			recalls[i] = recall(current_diag, has_bugs);
			i++;
		}//end while
		
		//average
		for(int d=0; d < recalls.length; d++)
			result += recalls[d];
		
		result /= recalls.length;	
		
		//wrap
		return result;
	}
	
	
	/******************************
	 * Wrap protocol.
	 * @param tdp - TDP engine.
	 * @param i - Execution index.
	 * @param steps - Step index.
	 ******************************/
	private void wrap(TDP tdp, int i, int steps){
Logger.log("ExpThread.wrap");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.wrap");
if (_bug_switch)
	return;

		print_result("\nTotal steps: " + i + " " + steps);
		print_result("Final best diagnoses: [P-diag = " + tdp.current_state.get_best_diag().get_prob() + ", "
				+ "P-comp = " + tdp.current_state.get_best_c_prob() + "]");
		print_result("Precision: " + precision(tdp.current_state.get_best_diags()));
		print_result("Recall: " + recall(tdp.current_state.get_best_diags()));
		print_diagnoses(tdp.current_state.get_best_diags());
		print_result("");
		
		//save matrix
		if (i == TDP_Run.executions_num - 1)
			try {
				tdp.current_state.save_matrix();
			} catch (IOException e1) {
				print_result("Error - final matrix could not be saved!");
			}
	}

	/*************** Let's try 
	 * @throws IOException *****/
	public boolean exec(ExperimentInstance instance) throws IOException{
Logger.log("ExpThread.exec");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.exec");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

	
		pool = instance.get_pool();
		Set<String> failed_tests = instance.get_failed_tests();

		// Load actual test results from ExperimentInstance
		for(int i=0;i<pool.size();i++)
			if(failed_tests.contains(pool.get_test(i).get_name()))
				actual_test_result[i]=1;
			else
				actual_test_result[i]=0;
			
		for(int i=0; i < TDP_Run.executions_num; i++){			
			int steps = 0; //steps counter
			
			//load tests to pool
			reset_tests();
			
			//reset spectrum
			ds = new Dynamic_Spectrum();

			///block "initial" tests			
			initial_tests(instance.get_initial_tests());
							
			//construct TDP engine
			TDP tdp = new TDP(lookahead, samples, threshold_prob);
			
			//set initial state
			tdp.set_current_state(ds);
			tdp.current_state.set_key(base_key.clone());
			tdp.set_tests_pool(pool);
			
			//diagnose initial state
			if (i == 0){
				print_result("\nStep 0:");
				tdp.diagnose_current();
				print_result("");
			}
			
			//plan
			int next_test = next_test(tdp, pool);
			while(next_test >= 0 && tdp.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob){
				
				//for debug
				steps++;
				System.out.println("\nstep: " + steps); 
				pool.block_test(next_test);
				
				//update spectrum with ACTUAL result
				if (actual_test_result[next_test] == 1){
					pool.get_test(next_test).update_after_fail(testsCoder);
					System.out.println("test has failed."); //for debug
				}

				//update state	
				tdp.current_state = tdp.update_state(tdp.current_state, next_test, actual_test_result[next_test], 99);
				
				//for debug
				System.out.println("Best diag> " + tdp.current_state.get_best_diag() + ": " + tdp.current_state.get_best_diag().get_prob());
				System.out.println("Best comp> " + tdp.current_state.get_best_comp(1) + ": " + tdp.current_state.get_best_c_prob());
				tdp.current_state.print_diagnoses();
				
				//break if too many steps
				if (steps >= 100){
					System.out.println("\nToo many steps break!");
					break;
				}
				
				//plan next test
				next_test = next_test(tdp, pool);
				
				//break if can't solve
				if (next_test < 0 && tdp.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob){
					System.out.println("\nCan't solve!");
					break;
				}
			}//end while
			
			//wrap
			wrap(tdp, i, steps);
			
		}//end super loop (for)
		print_result("Finished!");
    	Toolkit.getDefaultToolkit().beep(); //beep!
		
		return true;	
		
	}	
	
	public boolean exec_benchmark(){
Logger.log("ExpThread.exec_benchmark");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.exec_benchmark");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

Logger.log("ExpThread.exec_benchmark");
		//TODO
		return true;
		
		
		
	}
	/*************** End Let's try *****/
	
	/***********************
	 * Runs the experiment!
	 ***********************/
	public boolean exec(){
Logger.log("ExpThread.exec");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.exec");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		for(int i=0; i < TDP_Run.executions_num; i++){
			
			int steps = 0; //steps counter
			//load tests to pool
			reset_tests();
			
			//reset spectrum
			ds = new Dynamic_Spectrum();

			///block "initial" tests
			initial_tests();
				
			//construct TDP engine
			TDP tdp = new TDP(lookahead, samples, threshold_prob);
			
			//set initial state
			tdp.set_current_state(ds);
			tdp.current_state.set_key(base_key.clone());
			tdp.set_tests_pool(pool);
			
			//diagnose initial state
			if (i == 0){
				print_result("\nStep 0:");
				tdp.diagnose_current();
				print_result("");
			}
			
			//plan
			int next_test = next_test(tdp, pool);
			while(next_test >= 0 && tdp.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob){
				
				//for debug
				steps++;
				System.out.println("\nstep: " + steps); 
				pool.block_test(next_test);
				
				//update spectrum with ACTUAL result
				if (actual_test_result[next_test] == 1){
					pool.get_test(next_test).update_after_fail(testsCoder);
					System.out.println("test has failed."); //for debug
				}

				//update state	
				tdp.current_state = tdp.update_state(tdp.current_state, next_test, actual_test_result[next_test], 99);
				
				//for debug
				System.out.println("Best diag> " + tdp.current_state.get_best_diag() + ": " + tdp.current_state.get_best_diag().get_prob());
				System.out.println("Best comp> " + tdp.current_state.get_best_comp(1) + ": " + tdp.current_state.get_best_c_prob());
				tdp.current_state.print_diagnoses();
				
				//break if too many steps
				if (steps >= 100){
					System.out.println("\nToo many steps break!");
					break;
				}
				
				//plan next test
				next_test = next_test(tdp, pool);
				
				//break if can't solve
				if (next_test < 0 && tdp.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob){
					System.out.println("\nCan't solve!");
					break;
				}
			}//end while
			
			//wrap
			wrap(tdp, i, steps);
			
		}//end super loop (for)
		print_result("Finished!");
    	Toolkit.getDefaultToolkit().beep(); //beep!
		
		return true;
	}//end run()


	@Override
	public Object getRawResult() {
Logger.log("ExpThread.getRawResult");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.getRawResult");
if (_bug_switch)
	return null;

		//unimplemented
		return null;
	}


	@Override
	protected void setRawResult(Object arg0) {
Logger.log("ExpThread.setRawResult");
boolean _bug_switch = Bug_Switcher.has_bug("ExpThread.setRawResult");
if (_bug_switch)
	return;

		//unimplemented
		
	}

}//end Exp class
