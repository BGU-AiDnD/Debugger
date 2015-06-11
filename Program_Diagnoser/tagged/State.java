package Planner;
import Implant.*;


import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;

import Diagnoser.Barinel;
import Diagnoser.Diagnosis;
import Diagnoser.Dynamic_Spectrum;
import Experimenter.TDP_Run;
import Infrastrcture.Link;
import Infrastrcture.Linked_List;
import Infrastrcture.OrderAssist;

public class State {
	//main vars
	private int[][] M_matrix;
	private int[] e_vector;
	private Dynamic_Spectrum ds;

	//additional vars
	private int[] tests_done;
	private TreeSet<Diagnosis> state_diags; //state diagnoses
	private LinkedList<Diagnosis> best_diags; //best diagnosis
	private StateKey key;
	private final double log2 = Math.log(2);
	
	//buffer vars (for avoiding repeated calculations)
	private double[] c_probs; //components probabilities of being faulty
	private int[] c_ranks; //components rank of being faulty
	private double best_c_prob;
	private Hashtable<String, Double> probs_for_tests;
	private double state_entropy;
	private double max_entropy;
	
	/***************************
	 * Constructor.
	 * @param M - M matrix.
	 * @param e - error vector.
	 ***************************/
	public State(int[][] M, int[] e){
		M_matrix = M;
		e_vector = e;
		ds = null;
		
		initialize();
	}
	
	
	/***************************
	 * Constructor.
	 * @param M - M matrix.
	 * @param e - error vector.
	 ***************************/
	public State(Dynamic_Spectrum ds){
		M_matrix = null;
		e_vector = null;
		this.ds = ds;
		
		initialize();

	}
	
	
	/*************************************
	 * Initializes the object parameters.
	 *************************************/
	private void initialize(){
Logger.log("State.initialize");
boolean _bug_switch = Bug_Switcher.has_bug("State.initialize");
if (_bug_switch)
	return;

		state_diags = new TreeSet<Diagnosis>();
		key = new StateKey();
		
		//buffer vars
		probs_for_tests = new Hashtable<String, Double>();
		c_probs = null;
		c_ranks = null;
		best_diags = null;
		tests_done = null; //Linked_List();
		state_entropy = -1;
		max_entropy = -1;
		best_c_prob = -1;
	}
	
	
	/****************************************************
	 * Key getter.
	 * @return String representation of the state's key.
	 ****************************************************/
	public String get_key(){
Logger.log("State.get_key");
boolean _bug_switch = Bug_Switcher.has_bug("State.get_key");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return key.toString();
	}
	
	
	/**********************************
	 * Key setter.
	 * @param new_key - new state key.
	 **********************************/
	public void set_key(StateKey new_key){
Logger.log("State.set_key");
boolean _bug_switch = Bug_Switcher.has_bug("State.set_key");
if (_bug_switch)
	return;

		key = new_key;
	}
	
	
	/**************************************
	 * Clones and returns the state's key.
	 * @return a clone of the state's key.
	 **************************************/
	public StateKey clone_key(){
Logger.log("State.clone_key");
boolean _bug_switch = Bug_Switcher.has_bug("State.clone_key");
if (_bug_switch)
	return null;

		return key.clone();
	}
	
	
	/*********************************************
	 * Compute diagnoses and their probabilities.
	 *********************************************/
	public void compute_diags(){
Logger.log("State.compute_diags");
boolean _bug_switch = Bug_Switcher.has_bug("State.compute_diags");
if (_bug_switch)
	return;

		//avoid double calculations
		Barinel barinel;
		if (state_diags.size() == 0){
			
			if(ds == null)
				barinel = new Barinel(M_matrix,e_vector);
			else barinel = new Barinel(ds);
			
			state_diags = barinel.run();
		}
	}
	
	
	/***************************************
	 * State's diagnoses getter.
	 * @return All diagnoses of the state.
	 **************************************/
	public TreeSet<Diagnosis> get_state_diags(){
Logger.log("State.get_state_diags");
boolean _bug_switch = Bug_Switcher.has_bug("State.get_state_diags");
if (_bug_switch)
	return null;

		//make sure diagnoses were  generated
		compute_diags(); //over-calc avoidance is intrinsic
		
		return state_diags;
	}
	
	
	/************************************
	 * Calculates the state's entropy.
	 * @return the entropy of the state.
	 ************************************/
	public double get_entropy(){
Logger.log("State.get_entropy");
boolean _bug_switch = Bug_Switcher.has_bug("State.get_entropy");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		double diag_prob = 0;
		Diagnosis current_diag = null;
		
		//over-calc avoidance
		if (state_entropy < 0 ){
			//Initialize
			state_entropy = 0;
			
			//process
			//make sure diagnoses were generated
			compute_diags(); //over-calc avoidance is intrinsic
			
			Iterator<Diagnosis> iterator = state_diags.iterator();
			while(iterator.hasNext()){
				current_diag = iterator.next();
				diag_prob = current_diag.get_prob();
				
				//for debug
				if (diag_prob <= 0)
					System.out.println("Error - diag prob zero or less");
				
				state_entropy += diag_prob * (Math.log(1 / diag_prob) / log2);
			}//end while
		}//end if
		
		return state_entropy;
	}
	
	
	/*****************************
	 * Components number getter.
	 * @return Components number.
	 *****************************/
	public int get_comps_num(){
		if (ds == null)
			return M_matrix[0].length;
		
		else return ds.M[0].length;
	}
	
	
	/************************
	 * Tests number getter.
	 * @return Tests number.
	 ************************/
	public int get_tests_num(){
		if (ds == null)
			return M_matrix.length;
		
		else return ds.M.length;
	}
	
	
	/*******************************************************
	 * Calculates components probabilities of being faulty.
	 *******************************************************/
	public void calc_c_probs(){
		//make sure state diagnoses were generated
		if (state_diags.size() == 0)
			compute_diags();
		
		//declare vars
		c_probs = new double[TDP_Run.get_comps_num()]; //assuming java creates it initialized
		
		//calculate probabilities
		Iterator<Diagnosis> iterator = state_diags.iterator();
		int[] diag_comps;
		Diagnosis diag;
		while(iterator.hasNext()){
			diag = iterator.next();
			diag_comps = diag.get_diag();
			for(int i=0; i < diag_comps.length; i++)
				c_probs[diag_comps[i]] += diag.get_prob();
		}//end while (diagnoses)
	}
	
	
	/********************************************************************
	 * Calculates and returns components' probabilities of being faulty.
	 * @return components' probabilities of being faulty.
	 ********************************************************************/
	public double[] get_c_probs(){
		if (c_probs == null)
			calc_c_probs();
		
		return c_probs;
	}
	
	
	/********************************************************************
	 * Calculates the best single component probability of being faulty.
	 * @return the best single component probability of being faulty.
	 ********************************************************************/
	public double get_best_c_prob(){
		//case diagnoses are not generated
		if (c_probs == null)
			calc_c_probs();
		
		//avoid over calculations
		if (best_c_prob < 0){
			for(int i=0; i < c_probs.length; i++)
				if (c_probs[i] > best_c_prob)
					best_c_prob = c_probs[i];
		}
	
		return best_c_prob;
	}
	
	
	/********************************************************
	 * Updates spectrum matrix with new test.
	 * @param test - new single test spectrum.
	 * @param e - new error result.
	 * @entropy_reduction - Enforce entropy reduction flag.
	 ********************************************************/
	public void update_spectrum(int[] test, int e){
		if (ds != null){
			ds.update(test, e);
			return;
		}
			
		//declare vars
		int[] new_row = new int[M_matrix[0].length];
	
		//build new row
		test = OrderAssist.quickSort(test);
		for(int i=0; i<new_row.length; i++)
			if (OrderAssist.binarySearch(test, i) == true)
				new_row[i] = 1;
			else new_row[i] = 0;
		
		//update M
		int[][] new_M = new int[M_matrix.length + 1][M_matrix[0].length];
		for(int i=0; i<M_matrix.length; i++)
			new_M[i] = M_matrix[i];
		new_M[new_M.length - 1] = new_row;
		M_matrix = new_M;
		
		//update e
		int[] new_e = new int[e_vector.length + 1];
		for(int i=0; i<e_vector.length; i++)
			new_e[i] = e_vector[i];
		new_e[new_e.length - 1] = e;
		e_vector = new_e;
	}
	
	
	/******************************************
	 * Sets list of tests that have been done.
	 * @param test_list - tests list.
	 ******************************************/
	public void set_tests_done(int[] tests_array){
		tests_done = tests_array;
	}
	
	
	/*****************************************
	 * Adds a test to the list of tests done.
	 * @param test_i - test index.
	 *****************************************/
	public void add_test_done(int test_i){
		//declare vars
		int[] tests_temp = null;
		
		//create new array
		if (tests_done != null){ //this is not the first test
			tests_temp = new int[tests_done.length + 1];
			for(int i=0; i<tests_done.length; i++)
				tests_temp[i] = tests_done[i];
		}
		else tests_temp = new int[1];

		
		//add the new test index
		tests_temp[tests_temp.length - 1] = test_i;
		tests_done = tests_temp;
		
		//sort array
		tests_done = OrderAssist.quickSort(tests_done);
	}
	
	
	/***********************************************************
	 * Checks whether a test has been done already.
	 * @param test - index. 
	 * @return True - if test has been done. False - otherwise.
	 ***********************************************************/
	public boolean is_test_done(int test){
		if (tests_done != null)
			return OrderAssist.binarySearch(tests_done, test);
		else return false;
	}
	
	
	/*************************************************************
	 * Calculates probability of test to pass, given a diagnosis.
	 * @param test - test.
	 * @param diag - diagnosis.
	 * @return probability of test to pass, given a diagnosis.
	 *************************************************************/
	private double calc_prob_for_test(Test test, Diagnosis diag){
		//declare vars
		Linked_List h_list;
		LinkedList<Integer> temp_list = new LinkedList<Integer>();
		double result = 1; //0;
		
		//avoid repeated calculations	
		String key = "t:" + test.get_string_id() + ",d:" + diag.get_h_list().toString();
		if (!probs_for_tests.containsKey(key)){
			
			//get relevant h probabilities
			h_list = diag.get_h_list();
			Link current_link = h_list.get_anchor().get_next();
			while(current_link != null){
				if (test.contains((int) current_link.get_val()))
					temp_list.add((int)current_link.get_sec());
				
				current_link = current_link.get_next();
			}//end while
			
			//calculate test probability to pass
				//handle base cases
			if (temp_list.size() == 0)
				result = 1;
			
			else if (temp_list.size() == 1)
				result = temp_list.get(0);
		
			
			else{ //handle most cases
				Iterator<Integer> iterator = temp_list.iterator();
				while(iterator.hasNext())
					result *= iterator.next();
			}//end if
			
			//update buffer
			probs_for_tests.put(key, result);
			return result;
		}//end super if

		return probs_for_tests.get(key);
	}
	
	
	/********************************************
	 * Calculates probability of a test to pass.
	 * @param test - test.
	 * @return probability of a test to pass.
	 ********************************************/
	public double calc_prob_for_test(Test test){
		//declare vars
		double result = 0;
		Diagnosis temp_diag;
		
		//clear memory
		if (probs_for_tests.size() >= 100)
			probs_for_tests.clear();
		
		//avoid repeated calculations	
				String key = "t:" + test.get_string_id();
				if (! probs_for_tests.containsKey(key)){
					//start calculation
					Iterator<Diagnosis> iterator = state_diags.iterator();
					while(iterator.hasNext()){
						temp_diag = iterator.next();
						result += calc_prob_for_test(test, temp_diag) * temp_diag.get_prob();
					}//end while
					
					//update buffer
					probs_for_tests.put(key, result);
					return result;
				}
				
		return probs_for_tests.get(key);
	}
	
	
	/***************************************************************
	 * Lists all the components that produce no information gain.
	 * Also sorts the list!
	 * @return all the components that produce no information gain.
	 ***************************************************************/
	public int[] no_info_gain_comps(){
		//make sure components probabilities have been generated
		if (c_probs == null)
			calc_c_probs();
		
		//declare vars
		Linked_List list = new Linked_List();
		
		//start process
		for(int i=0; i<c_probs.length; i++)
			if (c_probs[i] == 1 || c_probs[i] == 0)
				list.add_val(i);
		
		return OrderAssist.quickSort(list.to_int_array());
	}
	
	
	/******************************************
	 * Calculates the entropy of a given test.
	 * @param test - test.
	 * @return the entropy of a given test.
	 ******************************************/
	public double calc_strong_test_entropy(Test test, State state0, State state1){
		//declare vars
		double result = 0;
		double pass_prob, fail_prob;
		
		//start calculation
		pass_prob = calc_prob_for_test(test);
		fail_prob = 1 - pass_prob;
		
		result = pass_prob * state0.get_entropy() + fail_prob * state1.get_entropy();
		
		return result;
	}
	
	
	/******************************************
	 * Calculates the entropy of a given test.
	 * @param test - test.
	 * @return the entropy of a given test.
	 ******************************************/
	public double calc_weak_test_entropy(Test test){
		//declare vars
		double result = 0;
		double pass_prob, fail_prob;
		
		//start calculation
		pass_prob = calc_prob_for_test(test);
		fail_prob = 1 - pass_prob;
		
		if (pass_prob == 1 || fail_prob == 1)
			result = 0;
		
		else{
			result = pass_prob * Math.log(1 / pass_prob) + fail_prob * Math.log(1 / fail_prob) ;
//			result = result / log2;	
		}
	
		return result;
	}
	
	
	/******************************************
	 * Calculates Entropy Reduction Potential.
	 * @param test - Test.
	 * @return test's ERP measure.
	 ******************************************/
	public double calc_ERP(Test test){
		//declare vars
		HashSet<Integer> seen = new HashSet<Integer>();
		double result = 0;
		double pass_prob, fail_prob;
		int relevant_comps = 0;
		int[] temp_diag;
		Diagnosis diag;
		
		//calculate probabilities
		pass_prob = calc_prob_for_test(test);
		fail_prob = 1 - pass_prob;
		
		//calculate number of relevant components
		TreeSet<Diagnosis> diags = get_state_diags();
		Iterator<Diagnosis> iterator = diags.iterator();
		while(iterator.hasNext()){
			diag = iterator.next();
			temp_diag = diag.get_diag();
			for(int i=0; i < temp_diag.length; i++)
				if (test.contains(temp_diag[i]) && !seen.contains(temp_diag[i])){
					relevant_comps++;
					seen.add(temp_diag[i]);
					}
		}//end while
		
		//wrap
		seen.clear();
		result = ( relevant_comps / test.get_part_comps().length ) + ( fail_prob / pass_prob ) + pass_prob;
		
		return result;
	}
	
	
	/***************************************
	 * Finds the most probable diagnoses.
	 * @return the most probable diagnoses.
	 ***************************************/
	public LinkedList<Diagnosis> get_best_diags(){
		//make sure diagnoses were  generated
		compute_diags(); //over-calc avoidance is intrinsic
		
		//declare vars
		Diagnosis temp_diag;
		double best = 0;
		
		//avoid double calculations
		if (best_diags == null){
			//start process
			best_diags = new LinkedList<Diagnosis>();
			Iterator<Diagnosis> iterator = state_diags.iterator();
			
			while(iterator.hasNext()){
				temp_diag = iterator.next();
				if (best <= temp_diag.get_prob()){
					if (best == temp_diag.get_prob())
						best_diags.add(temp_diag);
					
					else{
						best = temp_diag.get_prob();
						best_diags = new LinkedList<Diagnosis>();
						best_diags.add(temp_diag);
					}
				}//end if
			}//end while
		}//end super if
		
		return best_diags;
	}
	
	
	/******************************************
	 * Finds the most probable diagnosis.
	 * Randomize the result in case of a tie!!
	 * @return the most probable diagnosis.
	 ******************************************/
	public Diagnosis get_best_diag(){
		//make sure best diagnoses were generated
		get_best_diags();
		
		int index = (int)(Math.random() * (best_diags.size())); 
		
		if(best_diags.size() == 0)
			System.out.println("Error - diagnoses list is empty");
		return best_diags.get(index);
	}
	
	
	/**********************************************
	 * Finds the most probable faulty component.
	 * @return the most probable faulty component.
	 **********************************************/
	public int get_best_comp(int place){
		//make sure components probabilities have been generated
		if (c_probs == null)
			calc_c_probs();
		
		//make sure components ranks have been generated
		if (c_ranks == null){
			//declare vars
			Linked_List list = new Linked_List(); 
			
			//sort
			for (int i=0; i < c_probs.length; i++)
				if (c_probs[i] > 0)
					list.add_by_order(c_probs[i],i);
				
			//copy to array
			c_ranks = new int[list.get_length()];
			Link current_link = list.get_anchor().get_next();
			int i = 0;
			while(current_link != null){
				c_ranks[i] = (int)current_link.get_sec();
				
				//advance
				i++;
				current_link = current_link.get_next();
			}//end while
		}//end if
		
		return c_ranks[c_ranks.length - place];
	}
	
	
	/******************************
	 * Prints all state diagnoses.
	 ******************************/
	public void print_diagnoses(){
		synchronized (System.out){
			//make sure diagnoses were  generated
			if (state_diags.size() == 0)
				compute_diags();
			
			//process
			Iterator<Diagnosis> iterator = state_diags.iterator();
			Diagnosis diag;
			while(iterator.hasNext()){
				diag = iterator.next();
				System.out.print(diag.toString());
				System.out.println(" ,Probability: " + diag.get_prob());
			}//end while	
		}
	}
	
	
	/*****************************************************************
	 * Saves the state's matrix (including error vector) as CSV file.
	 * @throws IOException when file can't be created.
	 *****************************************************************/
	public void save_matrix() throws IOException{
		//handle dynamic spectrum
		if (ds != null){
			M_matrix = ds.M;
			e_vector = ds.e;
		}
		
		//ready file
		File res_file = new File("result_matrix.csv");
		if (res_file.exists() == false)
			res_file.createNewFile();
		
    	//clear file
    	PrintWriter out = new PrintWriter(new FileWriter(res_file, false));
	    out.print("");
	    out.close();
	    out = new PrintWriter(new FileWriter(res_file, true));
	    
	    //write header
	    for(int i=0; i < M_matrix[0].length; i++)
	    	out.print(ds.decode_comp(i) + ",");
	    out.println("error,");
	    
	    //write
	    for(int i=0; i < M_matrix.length; i++){
	    	for(int j=0; j < M_matrix[0].length; j++){
	    		out.print(M_matrix[i][j] + ",");
	    	}
	    	
	    	out.println(e_vector[i] + ",");
	    }
	    
	    //wrap
	    out.close();
	    System.out.println("Final matrix was saved to: " + res_file.toPath().toRealPath());
	}
	
	
	/**********************************************************
	 * Calculates the maximum possible entropy for this state.
	 * @return the maximum possible entropy for this state.
	 **********************************************************/
	public double get_max_entropy(){
		if (max_entropy < 0)
			max_entropy = Math.log((double)state_diags.size()) / log2;
		
		return max_entropy;
	}
	
	
	/********************
	 * Clones the state.
	 ********************/
	public State clone(){
		State new_state;
		if (ds == null)
			new_state = new State(M_matrix, e_vector); //!!!cloning issue!!!
		else new_state = new State(ds.clone());
		
		if (tests_done != null) //there are tests that have been done
			new_state.set_tests_done(tests_done.clone());
		
		else new_state.set_tests_done(null); //no tests have been done
		
		return new_state;
	}
}
