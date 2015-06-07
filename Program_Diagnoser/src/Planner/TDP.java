package Planner;

import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.ForkJoinPool;

import Diagnoser.Diagnosis;
import Diagnoser.Dynamic_Spectrum;
import Experimenter.TDP_Run;

public class TDP {
	//declare main vars
	public static Tests_Pool tests_pool;
	public static State current_state;
	public static Hashtable<String, State> states_buffer;
	
	//testing vars
	int best_test;
	double best_score;
	static int max_penalty;
	
	//define params
	public static double min_prob = 0.9; 
	public static int lookahead = 3;
	public static int samples_num = 20;

	//for debug
	static int counter_buffered = 0;
	static int counter_unbuffered = 0;
	public double[] priors;

	/*****************************
	 * Constructor.
	 * @param priors 
	 * @param la - Lookahead num.
	 * @param s - Samoles num.
	 *****************************/
	public TDP(int lookahead, int samples, double min_prob, double[] priors){
		TDP.tests_pool = null;
		TDP.current_state = null;
		TDP.states_buffer = new Hashtable<String, State>();
		
		TDP.min_prob = min_prob;
		TDP.lookahead = lookahead;
		TDP.samples_num = samples;
		this.priors=priors;
		TDP.counter_buffered = 0;
		TDP.counter_unbuffered = 0;
	}
	
	
	/********************************
	 * Constructor with buffer.
	 * @param la - Lookahead num.
	 * @param s - Samoles num.
	 * @param buff - States buffer.
	 ********************************/
	public TDP(int la, int s, double min_prob, Hashtable<String, State> buff, double[] priors){
		this.priors=priors;
		tests_pool = null;
		current_state = null;
		states_buffer = buff;
		
		TDP.min_prob = min_prob;
		lookahead = la;
		samples_num = s;
	}
	
	
	/***********************************
	 * Current state setter.
	 * @param M_matrix - M matrix.
	 * @param e_vector - error vector.
	 ***********************************/
	public void set_current_state(int[][] M_matrix, int[] e_vector){
		current_state = new State(M_matrix, e_vector,priors);
	}
	
	
	/***********************************
	 * Current state setter.
	 ***********************************/
	public void set_current_state(Dynamic_Spectrum ds){
		current_state = new State(ds,priors);
	}
	
	
	/****************************
	 * Tests pool setter.
	 * @param pool - tests pool.
	 ****************************/
	public void set_tests_pool(Tests_Pool pool){
		tests_pool = pool;
	}
	
	
	/***********************************************************
	 * Finds best test's index, by BEST DIAGNOSIS method.
	 * @param state - State.
	 * @param debug - Debug swicth.
	 * @return best test's index, by HIGHEST PROBABILITY method. 
	 ************************************************************/
	private static int best_test_by_BD(State state, boolean debug){
		return best_test_by_BD(state, null, debug);
	}
	
	
	
	/*******************************************************
	 * Finds best test's index, by BEST DIAGNOSIS method.
	 * @param state - state.
	 * @return best test's index, by BEST DIAGNOSIS method.
	 *******************************************************/
	private static int best_test_by_BD(State state, LinkedList<Integer> tie_list, boolean debug){
		//declare vars
		TreeSet<Diagnosis> state_diags = state.get_state_diags();
		Iterator<Diagnosis> iterator = state_diags.descendingIterator();
		Diagnosis best_diag;
		Test temp_test;
		
		double best_cost = Double.POSITIVE_INFINITY;
		int best_test = -1;
		
		//prepare tie-list
		LinkedList<Integer> BD_tie_list;
		if(tie_list == null)
			BD_tie_list = new LinkedList<Integer>();
		else BD_tie_list = tie_list;
		
		//start process
		Set<Integer> tests;
		Set<Integer> test_already_in = new HashSet<Integer>();
		Set<Integer> comp_already_checked = new HashSet<Integer>();
		
		//scan all diagnoses by descending probability.
		while(iterator.hasNext() && best_test < 0){
			best_diag = iterator.next();
			int[] diag = best_diag.get_diag();
			
			//stop when doagnosis probability is redicilously low
			if (best_diag.get_prob() < 0.01)
				break;
			
			for(int i=0; i < diag.length; i++){ //components loop
				if (comp_already_checked.contains(diag[i]))
					continue;
				comp_already_checked.add(diag[i]);
				
				tests = tests_pool.get_all_tests_with_comp(diag[i]);
				
				for(int t : tests){
					if (test_already_in.contains(t))
						continue;			
					
					if (state.is_test_done(t))
						continue;
					
					if (tests_pool.is_test_blocked(t))
						continue;
					
					temp_test = tests_pool.get_test(t);
					test_already_in.add(t);
					
					if (temp_test.get_cost() == best_cost)
						BD_tie_list.add(t);	
					
					else{
						best_cost = temp_test.get_cost();
						BD_tie_list.clear();
						BD_tie_list.add(t);	
					}	
				}

			}//end loop (components)

		
		
			//randomize result for tie cases
			if (BD_tie_list.size() > 0){
				int index = (int)(Math.random() * (BD_tie_list.size()));
				best_test = (int) BD_tie_list.get(index);
			}
		}//end loop (diagnoses)

		
		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;
	}
	
	
	/***********************************************************
	 * Finds best test's index, by HIGHEST PROBABILITY method.
	 * @param state - State.
	 * @param debug - Debug swicth.
	 * @return best test's index, by HIGHEST PROBABILITY method. 
	 ************************************************************/
	private static int best_test_by_HP(State state, boolean debug){
		return best_test_by_HP(state, null, debug);
	}
	
	
	/************************************************************
	 * Finds best test's index, by HIGHEST PROBABILITY method.
	 * @param state - state.
	 * @param tie_list - Tie list holder.
	 * @param debug - Debug swicth.
	 * @return best test's index, by HIGHEST PROBABILITY method.
	 ************************************************************/
	private static int best_test_by_HP(State state, LinkedList<Integer> tie_list, boolean debug){
		//declare vars
		int best_comp = 0;
		Test temp_test;	
		double best_cost = Double.POSITIVE_INFINITY;
		int best_test = -1;
		
		//prepare tie-list
		LinkedList<Integer> HP_tie_list;
		if(tie_list == null)
			HP_tie_list = new LinkedList<Integer>();
		else HP_tie_list = tie_list;
		
		
		//start process
		int p = 1;
		while (best_test == -1 && p < state.get_comps_num()){
			//get best component at place p
			best_comp = state.get_best_comp(p); 
			
			//break if component probability is ridiculously low or we exausted all components in state
			if (best_comp < 0 || state.get_c_probs()[best_comp] < 0.01)
				break;
			
			//locate all tests that pass through it
			Set<Integer> unblocked = tests_pool.get_unblocked();
			Set<Integer> all_that_contain = tests_pool.get_all_tests_with_comp(best_comp);
			
			for(int t : all_that_contain){
				//make sure test hasn't been done and is unblocked
				if (state.is_test_done(t) || !unblocked.contains(t))
					continue;
				
				temp_test = tests_pool.get_test(t);
				
				if (temp_test.contains(best_comp) && temp_test.get_cost() <= best_cost){
						
					if (temp_test.get_cost() == best_cost)
						HP_tie_list.add(t);
					
					else{
						best_cost = temp_test.get_cost();
						HP_tie_list.clear();;
						HP_tie_list.add(t);
					}	
				}//end super if
			}//end loop (tests)
			
			//randomize result for tie cases
			if (HP_tie_list.size() > 0){
				int index = (int)(Math.random() * (HP_tie_list.size()));
				best_test = (int) HP_tie_list.get(index);
			}
			
			p++;
		}//end loop (comps)
			
		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;
	}
	
	/***********************************************************
	 * Finds best test's index, by highest ENTROPY method.
	 * @param state - State.
	 * @param debug - Debug swicth.
	 * @return best test's index, by highest ENTROPY method. 
	 ************************************************************/
	private static int best_test_by_ENTROPY(State state, boolean debug){
		return best_test_by_ENTROPY(state, null, debug);
	}
	
	
	/******************************************************
	 * Finds best test's index, by highest ENTROPY method.
	 * @param state - state.
	 * @param tie_list - Tie list holder.
	 * @param debug - Debug notes switch.
	 * @return test's index, by highest ENTROPY method.
	 ******************************************************/
	private static int best_test_by_ENTROPY(State state, LinkedList<Integer> tie_list, boolean debug){
		//declare vars
		int best_test = -1;
		double best_cost = Double.POSITIVE_INFINITY;
		double best_entropy = 0;
		double temp_entropy;
		Test temp_test;
		
		Set<Integer> unblocked = tests_pool.get_unblocked();
		
		//prepare tie-list
		LinkedList<Integer> Entropy_tie_list;
		if(tie_list == null)
			Entropy_tie_list = new LinkedList<Integer>();
		else Entropy_tie_list = tie_list;
		
		//start process
		for(int t : unblocked){
			temp_test = tests_pool.get_test(t);
			
			//make sure test hasn't been done already
			if (state.is_test_done(t))
				continue;
			
			//apply pruning
			if (!temp_test.prune_by_diags_test(state))
				continue;
				
			//calc entropy
			temp_entropy = state.calc_weak_test_entropy(temp_test);
			
			if (temp_entropy >= best_entropy){
				if (temp_entropy == best_entropy && temp_test.get_cost() <= best_cost){
					Entropy_tie_list.add(t);
					best_cost = temp_test.get_cost();
				}
				
				else{
					best_entropy = temp_entropy;
					best_cost = temp_test.get_cost();
					Entropy_tie_list.clear();
					Entropy_tie_list.add(t);
				}
			}//end if
		}//end tests loop
		
		//randomize result for tie cases
		if (Entropy_tie_list.size() > 0){
			int index = (int)(Math.random() * (Entropy_tie_list.size()));
			best_test = (int) Entropy_tie_list.get(index);
		}

		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;

	}
	
	
	/***********************************************************
	 * Finds best test's index, by FUZZY ENTROPY method.
	 * @param state - State.
	 * @param debug - Debug swicth.
	 * @return best test's index, by HIGHEST FUZZY method. 
	 ************************************************************/
	private static int best_test_by_FUZZY(State state, boolean debug){
		return best_test_by_FUZZY(state, null, debug);
	}
	
	
	/************************************************************
	 * Finds best test's index, by highest FUZZY ENTROPY method.
	 * @param state - state.
	 * @param tie_list - Tie list holder.
	 * @param debug - Debug notes switch.
	 * @return test's index, by highest FUZZY ENTROPY method.
	 ************************************************************/
	private static int best_test_by_FUZZY(State state, LinkedList<Integer> tie_list, boolean debug){
		//declare vars
		int best_test = -1;
		double best_cost = Double.POSITIVE_INFINITY;
		double best_entropy = Double.POSITIVE_INFINITY;//0;
		double temp_entropy;
		Test temp_test;
		
		Set<Integer> unblocked = tests_pool.get_unblocked();
		
		//prepare tie-list
		LinkedList<Integer> Entropy_tie_list;
		if(tie_list == null)
			Entropy_tie_list = new LinkedList<Integer>();
		else Entropy_tie_list = tie_list;
		
		//start process
		for(int t : unblocked){
			temp_test = tests_pool.get_test(t);
			
			//make sure test hasn't been done already
			if (state.is_test_done(t))
				continue;
			
			//apply pruning
			if (!temp_test.prune_by_diags_test(state))
				continue;
				
			//calc entropy
			temp_entropy = state.calc_fuzzy_test_entropy(temp_test);
			
			if (temp_entropy <= best_entropy){ //>=
				if (temp_entropy == best_entropy && temp_test.get_cost() <= best_cost){
					Entropy_tie_list.add(t);
					best_cost = temp_test.get_cost();
				}
				
				else{
					best_entropy = temp_entropy;
					best_cost = temp_test.get_cost();
					Entropy_tie_list.clear();
					Entropy_tie_list.add(t);
				}
			}//end if
		}//end tests loop
		
		//randomize result for tie cases
		if (Entropy_tie_list.size() > 0){
			int index = (int)(Math.random() * (Entropy_tie_list.size()));
			best_test = (int) Entropy_tie_list.get(index);
		}

		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;

	}
	
	
	/**************************************************
	 * Finds best test's index, by MONTE CARLO method.
	 * @param state - state.
	 * @return test's index, by MONTE CARLO method.
	 **************************************************/
	private static int best_test_by_MC(State state, boolean debug){
		//declare vars
		int best_test = -1;
		
		//start process
		best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;
	}
	
	
	/****************************************************
	 * Calculates the best test based on a given method.
	 * @param method - predefined testing method.
	 * @param state - state.
	 * @return the best test based on a given method.
	 ****************************************************/
	public static int best_test_by(TDP_Run.method_types method, State state, boolean debug){
		//declare vars
		int best_test = -1;
		
		//start process
		switch(method){
		case BD:
			best_test = best_test_by_BD(state, debug);
			break;
		
		case HP:
			best_test = best_test_by_HP(state, debug);
			break;
			
		case ENTROPY:
			best_test = best_test_by_ENTROPY(state, debug);
			break;
			
		case FUZZY:
			best_test = best_test_by_FUZZY(state, debug);
			break;	
			
		case RAFFLE:
			best_test = best_test_by_MC(state, debug);
			break;	
			
		default: best_test = -1;
		}//end switch
		
		return best_test;
	}
	
	
	/****************************************************
	 * Calculates the best test based on a given method.
	 * @param method - predefined testing method.
	 * @return the best test based on a given method.
	 ****************************************************/
	public int best_test_by(TDP_Run.method_types method, boolean display){
		return best_test_by(method, current_state, display);
	}
	
	
	/********************************************************************
	 * Updates the given state according to chosen test and its outcome.
	 * Doesn't change the original state object!
	 * @param state - Source state.
	 * @param test_i - Test index.
	 * @param test_outcome - Test's outcome.
	 * @param l - lookahead parameter.
	 * @return - Updated state.
	 *********************************************************************/
	public synchronized static State update_state(State state, int test_i, int test_outcome){
		//declare vars
		Test test = tests_pool.get_test(test_i);
		StateKey new_key = state.clone_key();
		State new_state;
		
		//start process	
		//handle unbuffered state
		new_key.update_key(test_i, test_outcome);
		String key_string = new_key.toString();
		
		//avoid over calculations
		if (! states_buffer.containsKey(new_key.toString())){
			counter_unbuffered++; //for debug!!!!!!!!
			
			new_state = state.clone();
			
			//if ORACLE, don't update unfailed tests that contain a bugged component
			if (TDP_Run.method_of_choice.equals(TDP_Run.method_types.ORACLE) && test_outcome != 1 && TDP_Run.tests_pool.get_test(test_i).contains_any(TDP_Run.bugged_comps))
					System.out.println("Oracle vision!"); //don't update spectrum				
			else new_state.update_spectrum(test.get_part_comps(), test_outcome);
			
			new_state.add_test_done(test_i);
			new_state.set_key(new_key);
			states_buffer.put(key_string, new_state);
		}
		
		//handle buffered state
		else{
			counter_buffered++; //for debug!!!!!!!!
			new_state = states_buffer.get(new_key.toString());
		}
		
		//handle cache
		if (states_buffer.size() > 300){
			states_buffer.clear();
			System.out.println(">>>states cache was cleared.");
		}
		
		return new_state;

	}
	
	
	/**********************************************************
	 * Update a state with the base trace of a specified test.
	 * For fuzzy enropy calculation.
	 * Doesn't alter the original state object!
	 * @param state - State.
	 * @param test_i - Test index.
	 * @param test_outcome - Test outcome.
	 * @return the updated state.
	 ***********************************************************/
	public static State udpate_state_with_base_trace(State state, int test_i, int test_outcome){
		//declare vars
		Test test = tests_pool.get_test(test_i);
		StateKey new_key = state.clone_key();
		State new_state;
		
		//start process
		//handle unbuffered state
		new_key.update_key(test_i, test_outcome);
		
		new_state = state.clone();
		new_state.update_spectrum(test.get_base_comps(), test_outcome);
		new_state.add_test_done(test_i);
		new_state.set_key(new_key);
		
		return new_state;
	}
	
	
	/************************************
	 * Jpoins together all tie lists.
	 * @param method - Method of choice.
	 * @param state - State.
	 * @param debug - Debug flag.
	 * @return joint tie-list.
	 ************************************/
	private LinkedList<Integer> fabricate_best_tests(TDP_Run.method_types method, State state, boolean debug){
		//initialize
		LinkedList<Integer> result = null;
		
		switch(method){
		case MDP_BD: 
			LinkedList<Integer> BD_tie_list = new LinkedList<Integer>();
			best_test_by_BD(state, BD_tie_list, debug);
			result = BD_tie_list;
			break;
	
		case MDP_HP: 
			LinkedList<Integer> HP_tie_list = new LinkedList<Integer>();
			best_test_by_HP(state, HP_tie_list, debug);
			result = HP_tie_list;
			break;
	
		case MDP_ENTROPY: 
			LinkedList<Integer> Entropy_tie_list = new LinkedList<Integer>();
			best_test_by_HP(state, Entropy_tie_list, debug);
			result = Entropy_tie_list;
			break;
	
			
		case MDP_MC:
			result = new LinkedList<Integer>(); //empty list
		
		default: System.out.println("Error - could not fabricate tests list.");
		}
		
		//wrap
		return result;
	}
	
	
	/*********************************
	 * Jpoins together all tie lists.
	 * @param state - State.
	 * @param debug - Debug flag.
	 * @return joint tie-list.
	 *********************************/
	private LinkedList<Integer> fabricate_best_tests(State state, boolean debug){
		//initialize
		LinkedList<Integer> result = null;
		
		//apply huristic
		if (TDP_Run.method_of_choice == TDP_Run.method_types.FUZZY)
			result = fabricate_best_tests(TDP_Run.fuzzy_supports, state, debug);
		
		else result = fabricate_best_tests(TDP_Run.method_of_choice, state, debug);
		
		//wrap
		return result;
	}
	
	
	/**********************************************
	 * Calculates the best test based on MDP.
	 * @param focus_method - MDP sub focus method.
	 * @return the best test based on MDP.
	 **********************************************/
	public int best_test_by_MDP(TDP_Run.method_types focus_method, boolean debug){		
		//initialize
		LinkedList<Integer> tests_list = fabricate_best_tests(current_state, debug);
		best_test = -1;
		tests_pool.init_scores(tests_list); //important!!
		max_penalty = tests_list.size();
		best_score = Double.POSITIVE_INFINITY;
		
		//initialize states statistics
		counter_buffered = 0;
		counter_unbuffered = 0;
		
		//clear cache
		states_buffer.clear();
		tests_pool.clear_lexer_cache();
		
		//for threading
		final int threads_num = 4; //<<<<<<<<<<<<<<<<<<<
		MDPThread[] threads = new MDPThread[threads_num];
		int delimiter = tests_list.size() / threads_num + 1;
		
		//initialize threads
		for(int i=0; i < threads.length; i++)
			threads[i] = new MDPThread(new LinkedList<Integer>(), focus_method);
		
		//divide list to parts and set up the threads
		LinkedList<Integer> temp_list = new LinkedList<Integer>();
		int index = 1;
		int thread_to_be_updated = 0;
		for(int t : tests_list){
			temp_list.add(t);
			
			if (index % delimiter == 0 || index == tests_list.size()){	
				threads[thread_to_be_updated] = new MDPThread(temp_list, focus_method);
				temp_list = new LinkedList<Integer>();
				thread_to_be_updated++;
			}//end if
			
			index++;
		}//end for
		
		//submit threads
		ForkJoinPool fork = new ForkJoinPool();
		for(int i=0; i < threads.length; i++)
			fork.submit(threads[i]);
		
		//join
		for(int i=0; i < threads.length; i++)
			threads[i].join();
		
		//find best test
		for(int i=0; i < threads.length; i++)
			if (threads[i].best_score < best_score){
				best_score = threads[i].best_score;
				best_test = threads[i].best_test;
			}
		
		//wrap
		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(current_state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		return best_test;
	}
	
	
	/***************************************
	 * Enumerates the state space.
	 * @param t - Test index.
	 * @param l - Current lookahead.
	 * @param state - State.
	 * @param focus_method - Focus method.
	 * @param debug - Debug mode flag.
	 * @return score for internal use only.
	 ***************************************/
	public static double enum_state_space(int t, int l, State state, TDP_Run.method_types focus_method, boolean debug){
		//initiazlize
		Test test = tests_pool.get_test(t);
		double score = 0;
		double ratio = 0;
		double penalty = 0;
		
		//update score (handle no more tests)
		if (t < 0)
			score += 1;
		else score += /*(test.get_cost() + */1; //+ iteration cost
		
		//continue updating recursively
		if (l < lookahead && t > 0){
			State state0 = update_state(state, t, 0);
			State state1 = update_state(state, t, 1);
			
			//choose NEXT test to conduct
			int t0 = best_test_by(focus_method, state0, debug);
			int t1 = best_test_by(focus_method, state1, debug);
			
			//calculate probability of CURRENT test to pass
			double prob_to_pass = state.calc_prob_for_test(test);
			
			//recursive action
			score += enum_state_space(t0, l + 1, state0, focus_method, debug) * prob_to_pass;
			score += enum_state_space(t1, l + 1, state1, focus_method, debug) * (1 - prob_to_pass);
		}
		
		else{ //terminal node
			if (state.get_max_entropy() != 0.0){
				ratio = state.get_entropy() / state.get_max_entropy();
				penalty = ratio * ((double)max_penalty - score);
				score += penalty;
			}
			
			else score += 1; //reached single-diagnosis state!!
		}
		
		//handle score tracking
		if (l == 0)
			test.add_to_score(score);
		
		//weird stuff!
		if (Double.isNaN(score))
			score = 1;
		
		return score;
	}
	
	
	/***************************************
	 * Samples the sate space.
	 * @param t - Current test index.
	 * @param focus_method - Focus method.
	 * @param debug - Debug mode flag.
	 ***************************************/
	public static void sample_state_space(int t, TDP_Run.method_types focus_method, boolean debug){
		//construct penalty assistance
		PenaltyAssist penAssist = new PenaltyAssist();
		
		/////////START SAMPLING//////////
		for(int s = 0; s < samples_num; s++){	
			//for debug
			if (debug == true)
				System.out.println("\n" + "Sample No. " + s);
			
			//declare vars
			boolean terminal_node = false;
			double score = 0; //for current sample
			int new_test_i = t; //index of new test to conduct
			int test_outcome;
			State new_state = current_state;
			String penalty_state_key = "";
			Test test = null;
			
			///START LOOKAHEAD///
			int l = 0;
			while( !terminal_node ){					
				//capture state key for penalty
				if (l == lookahead)
					penalty_state_key = "" + new_state.get_key();
				
				//handle penalty
				if (l == lookahead && penAssist.is_stored(penalty_state_key)){
					score = penAssist.get_penalty(penalty_state_key);
					if (debug)
						System.out.println("<<Pre-calculated penalty break>>"); //for debug
					
					break; 
				}
				
				//simulate the test effect
				test = tests_pool.get_test(new_test_i);
				if (l < lookahead ){ //within look ahead boundaries
					if (Math.random() <= new_state.calc_prob_for_test(test))
						test_outcome = 0; //test succeeded
					else test_outcome = 1; //test failed
					
					//update state
					new_state = update_state(new_state, new_test_i, test_outcome);
				}
				
				if (l == lookahead){//passed lookahead boundary			
					double ratio = new_state.get_entropy() / new_state.get_best_diag().get_prob(); //new_state.get_entropy(); //new_state.get_entropy() / new_state.get_max_entropy();
					double penalty = ratio  + score; //* (max_penalty - score);
					score += penalty;
					
					terminal_node = true; //acts as brake;
				}
				
				//update score						
				score += 1; //iteration cost
						
				//for debug
				if (debug)
					System.out.println("diagnosis prob: " + new_state.get_best_diag().get_prob()
							+ " || State's entropy: " + new_state.get_entropy()); //for debug
				
				if (new_state.get_best_diag().get_prob() >= min_prob)
					terminal_node = true;
				
				//find new best test (if not finished already)
				if (!terminal_node){
					
					//for debug
					if (debug)
						System.out.println(new_state.get_key());
					
					new_test_i = best_test_by(focus_method, new_state, debug);
					//handle "no test found"
					if (new_test_i < 0){
//						score = max_penalty;
						terminal_node = true; //acts as break;
					}	
				}//end if (non-terminal node)
				
				//update lookahead counter
				l++; 
			}//end while (look ahead)
			
			//handle cache
			if (l >= lookahead && ! penAssist.is_stored(penalty_state_key))
					penAssist.insert_penalty(penalty_state_key, score);
			
			//update TEST score
			tests_pool.get_test(t).add_to_score(score); //automatically averages
	
		}//end for (samples)
	}
	
	
	/************************************
	 * Prints current state's diagnoses.
	 ************************************/
	public void  diagnose_current(){
		current_state.print_diagnoses();
	}
	
	
	/******************************************************************************
	 ********************************** For Debug *********************************
	 ******************************************************************************/
	public static void main(String[] args){
		//Simulate initial spectrum
		int[][] M = {{1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0},
					 {1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0},
					 {1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0},
					 {1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0},
					 {1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0}};
		
		int[] e = {0,0,0,0,1};
		
		//Simulate tests pool
		Tests_Pool pool = new Tests_Pool();
		int[] test0  = {0,1,2,3,4,5,6,13};
		int[] test1  = {0,1,2,3,4,5,6,13};
		int[] test2  = {0,1,2,3,4,5,6,11,12,13,14};
		int[] test3  = {0,1,2,3,4,5,6,11,12,13,14};
		int[] test4  = {0,1,2,3,4,5,6,9,11,13};
		int[] test5  = {0,1,2,3,4,5,6,9,11,13};
		int[] test6  = {0,1,2,3,4,5,6,9,11,13};
		int[] test7  = {0,1,2,3,4,5,6,13};
		int[] test8  = {0,1,2,3,4,5,6,13};
		int[] test9  = {0,1,2,3,4,5,6,7,8,9,11,12,13,14};
		int[] test10 = {0,1,2,3,4,5,6,7,9,11,13};
		int[] test11 = {0,1,2,3,4,5,6,8,11,12,13,14};
		int[] test12 = {0,1,2,3,4,5,6,7,9,11,13};
		int[] test13 = {0,1,2,3,4,5,6,7,9,11,12,13,14};
		int[] test14 = {0,1,2,3,4,5,6,7,9,11,12,13,14};


		pool.add_test(test0,"");
		pool.add_test(test1,"");
		pool.add_test(test2,"");
		pool.add_test(test3,"");
		pool.add_test(test4,"");
		pool.add_test(test5,"");
		pool.add_test(test6,"");
		pool.add_test(test7,"");
		pool.add_test(test8,"");
		pool.add_test(test9,"");
		pool.add_test(test10,"");
		pool.add_test(test11,"");
		pool.add_test(test12,"");
		pool.add_test(test13,"");
		pool.add_test(test14,"");
		
		//block tests that have been already executed
		pool.block_test(0);
		pool.block_test(1);
		pool.block_test(2);
		pool.block_test(3);

		
		//construct TDP engine
		int lookahead = 3;
		int samples = 100;
		TDP tdp = new TDP(lookahead, samples, 0.9,null);
		tdp.set_current_state(M, e);
		tdp.set_tests_pool(pool);
		
		//diagnose
//		tdp.diagnose_current();
		System.out.println();
		
		//plan
		int best_test = tdp.best_test_by_MDP(TDP_Run.method_types.ENTROPY,true);
//		int best_test = tdp.best_test_by_MDP("HP");
		
		TDP.tests_pool.print_scores();
		if (! (best_test < 0 ))
			System.out.println("Best next test is: " + best_test );
		
		//print states statistics
		System.out.println();
		System.out.println("States statistics (access count):");
		System.out.println("buffered: " + TDP.counter_buffered);
		System.out.println("unbuffered: " + TDP.counter_unbuffered);
	}
}
