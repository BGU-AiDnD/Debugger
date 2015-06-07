package Experimenter;

import java.awt.Toolkit;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.ForkJoinTask;

import Diagnoser.Diagnosis;
import Diagnoser.Dynamic_Spectrum;
import Implant.TestsRunner;
import Infrastrcture.OrderAssist;
import Parsing.FilesAssist;
import Parsing.TraceToCode;
import Planner.StateKey;
import Planner.TDP;
import Planner.Test;
import Planner.Tests_Pool;

public class ExpThread extends ForkJoinTask<Object>{
	//declare vars
	private static final long serialVersionUID = -8201270664406126310L;
	
	private int lookahead, samples;
	private double threshold_prob;
	private int[] actual_tests_result;
	private String return_code = "normal";
	private String file_Name;
	private long stopper; //counter for run-time
	
	//entropy foul handlers
	double last_entropy = 0;
	int same_entropy_in_a_row = 0;
	
	//Diclare initial spectrum holders
	private Dynamic_Spectrum ds;
	private StateKey base_key;
	private Set<Integer> initial_tests;
	
	//Ready structure for tests pool
	private Tests_Pool pool;
	private TraceToCode testsCoder;
	
	//placeholder for benchmark instance
	private ExperimentInstance ei = null;
	
	
	/*****************************************
	 * Constructor - Workbench mode. 
	 * @param bm_instance - WB Instance file.
	 * @throws IOException 
	 *****************************************/
	public ExpThread(File bm_instance) throws IOException{
		//set basic parameters
		lookahead = TDP_Run.lookahead;
		samples = TDP_Run.samples;
		threshold_prob = TDP_Run.threshold_prob;
		file_Name=bm_instance.getName();
		//set others
		testsCoder = new TraceToCode();
		ds = new Dynamic_Spectrum();
		base_key = new StateKey();
		initial_tests = new HashSet<Integer>();
		
		//read instance file
		ei = ExperimentInstance.read_from_file(bm_instance);
		
		//construct tests-pool
		pool = ei.get_pool();
		
		//upload components conversion table
		File conv_table_file = new File(FilesAssist.get_instances_path() + "/conv_comp_table.csv");
		testsCoder.load_conversion_table(conv_table_file);
		TDP_Run.testsCoder = this.testsCoder;
		TDP_Run.set_comps_num(testsCoder.get_comps_num());
		
		//handle failed tests knowledge and update global vars
		get_bugged_comps();
		actual_tests_result = FilesAssist.load_failed_tests_knowledge(pool, ei);
		//System.out.println("Finished loading experiment-instance.");
		TDP_Run.tests_pool = pool;
	}
	
	
	
	/*************************************************
	 * Constructor - Free mode.
	 * @throws IOException when unable to load files.
	 *************************************************/
	public ExpThread() throws IOException{
		//set basic parameters
		lookahead = TDP_Run.lookahead;
		samples = TDP_Run.samples;
		threshold_prob = TDP_Run.threshold_prob;
		pool = new Tests_Pool();
		initial_tests = new HashSet<Integer>();
		
		//load base traces to pool
		testsCoder = new TraceToCode();
		testsCoder.add_traces_to_pool(pool);
		TDP_Run.testsCoder = this.testsCoder;
		System.out.println("\nBase traces were loaded.");
		TDP_Run.set_comps_num(testsCoder.get_comps_num());
		
		//dump components conversion table
		testsCoder.saveConvTable();
		
		if (TDP_Run.bug_simulation_mode == TDP_Run.bug_sim_mode.RANDOMIZE_NEW){
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
		}// bug simulation
		
		//update global vars
		get_bugged_comps();
		actual_tests_result = FilesAssist.load_failed_tests_knowledge(pool);
		System.out.println("Finished determining all tests results.");
		TDP_Run.tests_pool = pool;
	}
	
	
	/*************************************************
	 * Randomize components to simulate bugs in them.
	 *************************************************/
	private void randomize_bugs(){
		//get ready
		HashSet<String> random_comps = get_random_comps(TDP_Run.random_bugs_ratio);
		File bugs_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/src/Implant/has_bugs.txt");
		
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
		pool.refresh();
	}
	
	
	/***********************************
	 * Block initial tets (randomized).
	 ***********************************/
	private void initial_tests_random(){
		//declare vars
		int t;
		base_key = new StateKey();
		
		//process
		int i = 0;
		boolean has_bug = false;
		while( i < TDP_Run.initial_tests_num ){ 
			t = pool.raffle_a_test();
			
			if (i < (TDP_Run.initial_tests_num - 1) || has_bug || actual_tests_result[t] == 1){
				pool.block_test(t);
				
				//update bug flag
				if (actual_tests_result[t] == 1){
					has_bug = true;
					pool.get_test(t).update_after_fail(testsCoder, false);
				}
				
				//update spectrum
//				update_spectrum(pool.get_test(t).get_part_comps(),actual_test_result[t]);
				ds.update(pool.get_test(t).get_part_comps(),actual_tests_result[t]);
				
				//update base key
				base_key.update_key(t, actual_tests_result[t]);
				
				//save chosen test in cache
				initial_tests.add(t);
				
				i++;
			}//end if
		}//end while
		
	}
	
	
	/****************************************************
	 * Block initial tests (according to instance data).
	 ****************************************************/
	private void initial_tests_BM(){
		if (ei == null){
			System.out.println("Error - no instance was specified for run!");
			return;
		}
		
		//declare vars
		base_key = new StateKey();
		
		//get initial tests from instance
		Set<String> set = ei.get_initial_tests();
		for(int t=0; t < pool.size(); t++)
			if (set.contains(pool.get_test(t).get_name())){
				//update spectrum
				ds.update(pool.get_test(t).get_part_comps(),actual_tests_result[t]);
				pool.block_test(t);
				//update base key
				base_key.update_key(t, actual_tests_result[t]);
				
				//save chosen test in cache
				initial_tests.add(t);
			}
	}
	
	
	/****************************************************
	 * Block initial tests (according to chosen method).
	 ****************************************************/
	private void initial_tests(){
		//handle Free mode
		switch(TDP_Run.initial_tests_method){
		case BENCHMARK:
			initial_tests_BM();
			break;
			
		case RANDOM: //Free mode
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
	private int next_test(TDP tdp, Tests_Pool pool, int steps ){
		switch(TDP_Run.method_of_choice){
		case RAFFLE:
			return pool.raffle_a_test();
		
		case HP:
			return tdp.best_test_by(TDP_Run.method_types.HP, TDP_Run.debug_mode);
			
		case BD:
			return tdp.best_test_by(TDP_Run.method_types.BD, TDP_Run.debug_mode);
			
		case ENTROPY:
			return tdp.best_test_by(TDP_Run.method_types.ENTROPY, TDP_Run.debug_mode);
			
		case ORACLE:
			return tdp.best_test_by(TDP_Run.method_types.HP, TDP_Run.debug_mode);		
			
		case FUZZY:
			if (steps <= 7)
				return tdp.best_test_by(TDP_Run.method_types.FUZZY, TDP_Run.debug_mode);
			else{ 
				if (!TDP_Run.fuzzy_supports.toString().contains("MDP"))
					return tdp.best_test_by(TDP_Run.fuzzy_supports, TDP_Run.debug_mode);
				else 
					return tdp.best_test_by_MDP(TDP_Run.fuzzy_supports, TDP_Run.debug_mode);
			}
			
		case MDP_MC:
			return tdp.best_test_by_MDP(TDP_Run.method_types.RAFFLE, TDP_Run.debug_mode);
			
		case MDP_HP:
			return tdp.best_test_by_MDP(TDP_Run.method_types.HP, TDP_Run.debug_mode);
			
		case MDP_BD:
			return tdp.best_test_by_MDP(TDP_Run.method_types.BD, TDP_Run.debug_mode);
			
		case MDP_ENTROPY:
			return tdp.best_test_by_MDP(TDP_Run.method_types.ENTROPY, TDP_Run.debug_mode);		
		
		default: return -1;
		}//end switch
	}
	
	
	/***************************
	 * Synchronized println.
	 * @param string - string.
	 ***************************/
	private void print_result(String string){
		synchronized(System.out){
			//System.out.println(string);
			int x=0;
		}
	}
	
	
	/********************************
	 * Prints a list of diagnoses.
	 * @param list - Diagnoses list.
	 ********************************/
	private void print_diagnoses(LinkedList<Diagnosis> list){
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
		if (Double.isNaN(result))
			return 0;
		else return result;
	}
	
	
	/*****************************************************
	 * Assembles array of bugged components.
	 * @return an array containing the bugged components.
	 *****************************************************/
	private int[] get_bugged_comps(){
		//initialize
		int[] has_bugs = null;
		
		//if in Free Mode: read has-bugs-file
		if (ei == null){
			File file = FilesAssist.get_has_bugs_file();
			try {
				has_bugs = testsCoder.fileToArray(file);
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		else{ //in Benchmark Mode
			Set<String> has_bugs_set = ei.get_bugs();
			has_bugs = testsCoder.setToArray(has_bugs_set);
		}
		
		//update global variable
		TDP_Run.bugged_comps = has_bugs;
		
		return has_bugs;
	}
	
	
	/**************************************************
	 * Precision calculation for a batch of diagnosis.
	 * @param diagnoses - Diagnoses batch.
	 * @return averaged precision of given diagnoses.
	 **************************************************/
	private double precision(LinkedList<Diagnosis> diagnoses){
		//initialize
		double result = 0;
		double[] precisions = new double[diagnoses.size()];
		int[] has_bugs = null;
		Iterator<Diagnosis> iterator = diagnoses.iterator();
		Diagnosis current_diag;
		
		has_bugs = get_bugged_comps();
		
		//sort bugs - a must!!
		has_bugs = OrderAssist.quickSort(has_bugs);
		
		//process
		int i = 0;
		while(iterator.hasNext()){
			current_diag = iterator.next();
			
			precisions[i] = current_diag.get_prob()*precision(current_diag, has_bugs);
			i++;
		}//end while
		
		//average
		for(int d=0; d < precisions.length; d++)
			result += precisions[d];
		
		//result /= precisions.length;	
		
		//wrap
		return result;
	}
	
	
	/**************************************************
	 * Precision calculation for a batch of diagnosis.
	 * @param diagnoses - Diagnoses batch.
	 * @return averaged precision of given diagnoses.
	 **************************************************/
	private double recall(LinkedList<Diagnosis> diagnoses){
		//initialize
		double result = 0;
		double[] recalls = new double[diagnoses.size()];
		int[] has_bugs = null;
		Iterator<Diagnosis> iterator = diagnoses.iterator();
		Diagnosis current_diag;
		
		has_bugs = get_bugged_comps();
		
		//ignore bugs that are not present in initial tests
		Test test;
		Set<Integer> new_has_bugs = new HashSet<Integer>();
		for (Integer t : initial_tests){
			test = pool.get_test(t);
			for(int i=0; i < has_bugs.length; i++){
				if (test.contains(has_bugs[i]))
					new_has_bugs.add(has_bugs[i]);
			}
		}
		
		has_bugs = new int[new_has_bugs.size()];
		int b = 0;
		for (Integer bug : new_has_bugs){
			has_bugs[b] = bug;
			b++;
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
	
	public void export_diags_to_csv(String file_name,TreeSet<Diagnosis> diagnoses) throws IOException{
		//handle file
		file_name.replace(".csv", "");
		file_name += ".csv";
		File file = new File(file_name);
		if (!file.exists())
			file.createNewFile();
		
		//get ready
		PrintWriter writer = new PrintWriter(file);
		Iterator<Diagnosis> iterator = diagnoses.descendingIterator();
		Diagnosis current_diag;
		int[] current_array;
		
		//process
		while(iterator.hasNext()){
			current_diag = iterator.next();
			current_array = current_diag.get_diag();
			for(int i=0; i < current_array.length; i++)
				writer.print(current_array[i] + ",");
			
			//write probability
			writer.print("P," + current_diag.get_prob());
			writer.println();
		}//end while
		
		//wrap
		writer.close();
	}
	
	
	private void wrap(TDP tdp, int i, int steps){
		//stop stopper!
		double duration = ( System.currentTimeMillis() - stopper ) / 1000.0;
		
		TreeSet<Diagnosis> diags =TDP.current_state.get_state_diags();
		
		LinkedList<Diagnosis> list_diags=new LinkedList<Diagnosis>(diags);
		
		//calculate factors
		double precision 		= precision(list_diags);
		double recall 			= recall(list_diags);
		double best_diag_prob 	= TDP.current_state.get_best_diag().get_prob();
		double best_c_prob 		= TDP.current_state.get_best_c_prob();
		
		//report
		String temp_name = "";
		
		/*print_result("\nTotal steps: " + i + " " + steps);
		print_result("Final best diagnoses: [P-diag = " + best_diag_prob + ", "	+ "P-comp = " + best_c_prob + "]");
		print_result("Precision: " + precision);
		print_result("Recall: " + recall);
		print_result("Best Diagnoses found:");
		print_diagnoses(TDP.current_state.get_best_diags());
		print_result("");
		print_result("True bugged components:");
		for(int comp: get_bugged_comps())
			System.out.print(comp + " ");
		print_result("");
		*/
		//save result matrix
		if (i == TDP_Run.executions_num - 1)
			try {
				TDP.current_state.save_matrix();
			} catch (IOException e1) {
				print_result("Error - final matrix could not be saved!");
			}
		
		//in BM mode, save record
		if (ei != null){
			//ready record
			String record = "";
			
			////fill record with data////
			//date & time
			DateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy,HH:mm:ss,");
			Date date = new Date();
			record += dateFormat.format(date); 
			
			//instance name
			record += ei.get_name() + ',' ;
			
			//technique name
			if (TDP_Run.use_entropy_foul)
				temp_name = "" + 'i';
			temp_name += TDP_Run.method_of_choice ;
			record += "" + temp_name + ',' ;
			
			//best diagnosis prob
			record += "" + best_diag_prob + ',' ;
			
			//best comp prob
			record += "" + best_c_prob + ',' ;
			
			//recall
			record += "" + recall + ',' ;
			
			//precision
			record += "" + precision + ',' ;
			
			//total steps
			record += "" + steps + ',' ;
			
			//duration[sec]
			record += "" + duration + ',';
			
			//return code
			record += return_code + ',' ;
			record +=""+ initial_tests.size() + ',' ; 
			record +=""+ pool.size() + ',' ; 
			//System.out.println(record);
			////write to file//
			try {
				File records_file = new File(FilesAssist.outPath+file_Name+".csv");
				PrintWriter writer = new PrintWriter(new FileWriter(records_file, true));
				writer.println(record);
				writer.close();
				export_diags_to_csv(FilesAssist.outPath+file_Name+i+"_AllDiags.csv",diags);
				//System.out.println("Results were added to: " + records_file.toPath().toRealPath());
			} catch (IOException e) {
				print_result("Error - experiment record could not be saved!");
			}
			
		}//end if
	}
	
	
	/***********************
	 * Runs the experiment!
	 ***********************/
	public boolean exec(){
		System.out.println(file_Name);
		for(int i=0; i < TDP_Run.executions_num; i++){
			//initialize
			int steps = 0; //steps counter
			same_entropy_in_a_row = 0;
			reset_tests();
			return_code = "normal";
			
			//reset spectrum
			ds = new Dynamic_Spectrum();

			///block "initial" tests
			reset_tests();
			initial_tests();
				
			//construct TDP engine
			//int[] comps =pool.blocked_tests_comps();
			TDP tdp = new TDP(lookahead, samples, threshold_prob,ei.priors);
			
			//set initial state
			tdp.set_current_state(ds);
			TDP.current_state.set_key(base_key.clone());
			tdp.set_tests_pool(pool);
			
			//diagnose initial state
			if (i == 0){
				print_result("\nStep 0:");
				tdp.diagnose_current();
				print_result("");
			}
			
			//plan
			stopper = System.currentTimeMillis(); //intitialize stoper
			int next_test = next_test(tdp, pool, steps);
			while(next_test >= 0 && (TDP.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob)
					/*&& tdp.current_state.get_best_c_prob() < 0.9*/){
				
				//update step
				steps++;
				//System.out.println("\nstep: " + steps); 
				pool.block_test(next_test);
				
				//update spectrum with ACTUAL result
				if (actual_tests_result[next_test] == 1){
					pool.get_test(next_test).update_after_fail(testsCoder, false);
					//System.out.println("test has failed."); //for debug
				}

				//update state	
				TDP.current_state = TDP.update_state(TDP.current_state, next_test, actual_tests_result[next_test]);
				if (TDP_Run.method_of_choice.equals(TDP_Run.method_types.ORACLE) && pool.get_test(next_test).contains_any(get_bugged_comps()) 
						&& actual_tests_result[next_test] != 1)
					steps--; //if Oracle && test failed and contains bug --> ignore this step (matrix doesn't get updated)
				
				//for debug
				//System.out.println("Best diag> " + TDP.current_state.get_best_diag() + ": " + TDP.current_state.get_best_diag().get_prob());
				//System.out.println("Best comp> " + TDP.current_state.get_best_comp(1) + ": " + TDP.current_state.get_best_c_prob());
				TDP.current_state.print_diagnoses();
				
				//break if too many steps
				if (steps >= 150){
					//System.out.println("\nToo many steps break!");
					return_code = "too many steps";
					break;
				}
				
				//brake if entropy foul
				if(TDP_Run.use_entropy_foul){
					if (TDP.current_state.get_entropy() >= last_entropy){
						same_entropy_in_a_row++;
						last_entropy = TDP.current_state.get_entropy();
						
						if (same_entropy_in_a_row >= 5){
							System.out.println("\nEntropy foul!");
							return_code = "entropy foul";
							break;
						}
						
					} else{
						//reset
						same_entropy_in_a_row = 0;
						last_entropy = TDP.current_state.get_entropy();
					}
				}
				
				//plan next test 
				next_test = next_test(tdp, pool, steps);
				
				//break if can't solve
				if (next_test < 0 && TDP.current_state.get_best_diag().get_prob() < TDP_Run.threshold_prob){
					System.out.println("\nCan't solve!");
					return_code = "can't advance";
					break;
				}
			}//end while
			
			//wrap
			wrap(tdp, i, steps);
			
		}//end super loop (for)
		print_result("Finished!");
    	//Toolkit.getDefaultToolkit().beep(); //beep!
		
		return true;
	}//end run()


	@Override
	public Object getRawResult() {
		//unimplemented
		return null;
	}


	@Override
	protected void setRawResult(Object arg0) {
		//unimplemented
		
	}

}//end Exp class
