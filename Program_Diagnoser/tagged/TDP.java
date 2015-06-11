package Planner;
import Implant.*;


import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;

import Diagnoser.Barinel;
import Diagnoser.Diagnosis;
import Diagnoser.Dynamic_Spectrum;
import Experimenter.TDP_Run;
import Infrastrcture.Link;
import Infrastrcture.Linked_List;

public class TDP {
	//declare main vars
	public Tests_Pool tests_pool;
	public State current_state;
	public Hashtable<String, State> states_buffer;
	private PenaltyAssist penAssist;
	
	//testing vars
	int best_test;
	double best_score;
	int max_penalty;
	
	//define params
	private double min_prob = 0.9; 
	private int lookahead = 3;
	private int samples_num = 20;
	
	//tie lists
	private Linked_List BD_tie_list = new Linked_List();
	private Linked_List HP_tie_list = new Linked_List();
	private Linked_List Entropy_tie_list = new Linked_List();
	private Linked_List ERP_tie_list = new Linked_List();
	
	//for debug
	int counter_buffered = 0;
	int counter_unbuffered = 0;
	
	/*****************************
	 * Constructor.
	 * @param la - Lookahead num.
	 * @param s - Samoles num.
	 *****************************/
	public TDP(int lookahead, int samples, double min_prob){
		tests_pool = null;
		current_state = null;
		penAssist = new PenaltyAssist();
		states_buffer = new Hashtable<String, State>();
		
		this.min_prob = min_prob;
		this.lookahead = lookahead;
		samples_num = samples;
	}
	
	
	/********************************
	 * Constructor with buffer.
	 * @param la - Lookahead num.
	 * @param s - Samoles num.
	 * @param buff - States buffer.
	 ********************************/
	public TDP(int la, int s, double min_prob, Hashtable<String, State> buff){
		tests_pool = null;
		current_state = null;
		penAssist = new PenaltyAssist();
		states_buffer = buff;
		
		this.min_prob = min_prob;
		lookahead = la;
		samples_num = s;
	}
	
	
	/***********************************
	 * Current state setter.
	 * @param M_matrix - M matrix.
	 * @param e_vector - error vector.
	 ***********************************/
	public void set_current_state(int[][] M_matrix, int[] e_vector){
Logger.log("TDP.set_current_state");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.set_current_state");
if (_bug_switch)
	return;

		current_state = new State(M_matrix, e_vector);
	}
	
	
	/***********************************
	 * Current state setter.
	 ***********************************/
	public void set_current_state(Dynamic_Spectrum ds){
Logger.log("TDP.set_current_state");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.set_current_state");
if (_bug_switch)
	return;

		current_state = new State(ds);
	}
	
	
	/****************************
	 * Tests pool setter.
	 * @param pool - tests pool.
	 ****************************/
	public void set_tests_pool(Tests_Pool pool){
Logger.log("TDP.set_tests_pool");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.set_tests_pool");
if (_bug_switch)
	return;

		tests_pool = pool;
	}
	
	
	/*******************************************************
	 * Finds best test's index, by BEST DIAGNOSIS method.
	 * @param state - state.
	 * @return best test's index, by BEST DIAGNOSIS method.
	 *******************************************************/
	private int best_test_by_BD(State state, boolean debug){
Logger.log("TDP.best_test_by_BD");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_BD");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		LinkedList<Diagnosis> best_diags = state.get_best_diags();
		Diagnosis best_diag;
		Test temp_test;
		BD_tie_list = new Linked_List();
		
		boolean break_flag;
		double best_cost = Double.POSITIVE_INFINITY;
		int best_test = -1;
		
		//start process
		int t;
		Iterator<Integer> iterator = tests_pool.get_unblocked_list().iterator();
		while(iterator.hasNext()){
			t = iterator.next();
			if (state.is_test_done(t))
				continue;
			
			//produce raw tie list
			temp_test = tests_pool.get_test(t);
			
			Iterator<Diagnosis> iterator2 = best_diags.iterator();
			while(iterator2.hasNext()){ //diagnoses loop
				break_flag = false;
				best_diag = iterator2.next();
				
				for(int i=0; i < best_diag.get_diag().length; i++) //components loop
					if (temp_test.contains(best_diag.get_diag()[i])
						&& temp_test.get_cost() <= best_cost){
							
							if (temp_test.get_cost() == best_cost)
								BD_tie_list.add_val(t);	
							
							else{
								best_cost = temp_test.get_cost();
								BD_tie_list = new Linked_List();
								BD_tie_list.add_val(t);	
							}
							
							break_flag = true;
							break; //components loop
					}//end if
				
				if (break_flag)
					break;
			}//end while (diagnoses)
		}//end loop (tests)
		
		
		//randomize result for tie cases
		if (BD_tie_list.get_length() > 0){
			int index = (int)(Math.random() * (BD_tie_list.get_length())) + 1;
			best_test = (int) BD_tie_list.get_val(index);
		}

		
//		//if no suitable test found, raffle one
//		if (best_test == -1)
//			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;
	}
	
	
	/************************************************************
	 * Finds best test's index, by HIGHEST PROBABILITY method.
	 * @param state - state.
	 * @return best test's index, by HIGHEST PROBABILITY method.
	 ************************************************************/
	private int best_test_by_HP(State state, boolean debug){
Logger.log("TDP.best_test_by_HP");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_HP");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		int best_comp = 0;
		Test temp_test;
		HP_tie_list = new Linked_List();
		double best_cost = Double.POSITIVE_INFINITY;
		int best_test = -1;
		
		//start process
		int p = 1;
		while (best_test == -1 && p < state.get_comps_num()){
			//get best component at place p
			best_comp = state.get_best_comp(p); 
			
			//break if component probability is ridiculously low 
			if (state.get_c_probs()[best_comp] < 0.01)
				break;
			
			//locate all tests that pass through it
			int t;
			Iterator<Integer> iterator = tests_pool.get_unblocked_list().iterator();
			while(iterator.hasNext()){
				t = iterator.next();
				
				//make sure test hasn't been done
				if (state.is_test_done(t))
					continue;
				
				temp_test = tests_pool.get_test(t);
				
				if (temp_test.contains(best_comp) && temp_test.get_cost() <= best_cost){
						
					if (temp_test.get_cost() == best_cost)
						HP_tie_list.add_val(t);
					
					else{
						best_cost = temp_test.get_cost();
						HP_tie_list = new Linked_List();
						HP_tie_list.add_val(t);
					}	
				}//end super if
			}//end loop (tests)
			
			//randomize result for tie cases
			if (HP_tie_list.get_length() > 0){
				int index = (int)(Math.random() * (HP_tie_list.get_length())) + 1;
				best_test = (int) HP_tie_list.get_val(index);
			}
			
			p++;
		}//end loop (comps)
			
//		//if no suitable test found, raffle one
//		if (best_test == -1)
//			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;
	}
	
	
	/******************************************************
	 * Finds best test's index, by highest ENTROPY method.
	 * @param state - state.
	 * @return test's index, by highest ENTROPY method.
	 ******************************************************/
	private int best_test_by_ENTROPY(State state, boolean debug){
Logger.log("TDP.best_test_by_ENTROPY");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_ENTROPY");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		int best_test = -1;
		double best_cost = Double.POSITIVE_INFINITY;
		double best_entropy = 0;
		double temp_entropy;
		Test temp_test;
		Entropy_tie_list = new Linked_List();
		
		int t;
		Iterator<Integer> iterator = tests_pool.get_unblocked_list().iterator();
		
		//start process
		while(iterator.hasNext()){
			t = iterator.next();
			temp_test = tests_pool.get_test(t);
			
			//make sure test hasn't been done already
			if (state.is_test_done(t))
				continue;
			
			//apply pruning
			if (!temp_test.pass_prune_test(state))
				continue;
				
			//calc entropy
			temp_entropy = state.calc_weak_test_entropy(temp_test);
			
			if (temp_entropy >= best_entropy){
				if (temp_entropy == best_entropy && temp_test.get_cost() <= best_cost){
					Entropy_tie_list.add_val(t);
					best_cost = temp_test.get_cost();
				}
				
				else{
					best_entropy = temp_entropy;
					best_cost = temp_test.get_cost();
					Entropy_tie_list = new Linked_List();
					Entropy_tie_list.add_val(t);
				}
			}//end if
		}//end tests loop
		
		//randomize result for tie cases
		if (Entropy_tie_list.get_length() > 0){
			int index = (int)(Math.random() * (Entropy_tie_list.get_length())) + 1;
			best_test = (int) Entropy_tie_list.get_val(index);
		}

		//if no suitable test found, raffle one
		if (best_test == -1)
			best_test = tests_pool.raffle_a_test(state);
		
		//error handling
		if (debug && best_test < 0)
			System.out.println("Warning - no suitable test found!");
		
		return best_test;

	}
	
	
	/******************************************************
	 * Finds best test's index, by highest ENTROPY method.
	 * @param state - state.
	 * @return test's index, by highest ENTROPY method.
	 ******************************************************/
	private int best_test_by_ERP(State state, boolean debug){
Logger.log("TDP.best_test_by_ERP");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_ERP");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		int best_test = -1;
		double best_cost = Double.POSITIVE_INFINITY;
		double best_erp = 0;
		double temp_erp;
		Test temp_test;
		ERP_tie_list = new Linked_List();
		
		int t;
		Iterator<Integer> iterator = tests_pool.get_unblocked_list().iterator();
		
		//start process
		while(iterator.hasNext()){
			t = iterator.next();
			temp_test = tests_pool.get_test(t);
			
			//make sure test hasn't been done already
			if (state.is_test_done(t))
				continue;
			
			//apply pruning
			if (!temp_test.pass_prune_test(state))
				continue;
				
			//calc entropy
			temp_erp = state.calc_ERP(temp_test);
			
			if (temp_erp >= best_erp){
				if (temp_erp == best_erp && temp_test.get_cost() <= best_cost){
					ERP_tie_list.add_val(t);
					best_cost = temp_test.get_cost();
				}
				
				else{
					best_erp = temp_erp;
					best_cost = temp_test.get_cost();
					ERP_tie_list = new Linked_List();
					ERP_tie_list.add_val(t);
				}
			}//end if
		}//end tests loop
		
		//randomize result for tie cases
		if (ERP_tie_list.get_length() > 0){
			int index = (int)(Math.random() * (ERP_tie_list.get_length())) + 1;
			best_test = (int) ERP_tie_list.get_val(index);
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
	 * Finds best test's index, by LOWEST COST method.
	 * @param state - state.
	 * @return test's index, by LOWEST COST method.
	 **************************************************/
	@SuppressWarnings("unused")
	private int best_test_by_LC(State state, boolean debug){
Logger.log("TDP.best_test_by_LC");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_LC");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		int[] no_gain_comps = state.no_info_gain_comps();
		double best_cost = 999999;
		int best_test = -1;
		Test temp_test;
		boolean temp_flag;
		
		//start process
		for(int t=0; t < tests_pool.size(); t++){
			if (tests_pool.is_test_blocked(t) || state.is_test_done(t))
				continue;
			
			if (!state.is_test_done(t)){ //no point in repeating tests
				temp_test = tests_pool.get_test(t);
				temp_flag = true;
				
				int c = 0;
				while(temp_flag == true && no_gain_comps != null
						&& c < no_gain_comps.length){
					if (temp_test.contains(no_gain_comps[c]))
						temp_flag = false;
					
					c++;
				}//end while (no gain components)
				
				//handle normal situation where a suitable test exists
				if (temp_flag == true && temp_test.get_cost() < best_cost){
					best_test = t;
					best_cost = temp_test.get_cost();
				}
				//handle situations when all suitable tests are done already
				else if (temp_flag == false && best_test < 0){
					best_test = t;
					best_cost = temp_test.get_cost() + 999999;
				}
				else if(temp_flag == false
						&& temp_test.get_cost() + 999999 < best_test){
					best_test = t;
					best_cost = temp_test.get_cost() + 999999;
				}
			}
		}//end for (tests)
		
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
	private int best_test_by_MC(State state, boolean debug){
Logger.log("TDP.best_test_by_MC");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_MC");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

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
	public int best_test_by(TDP_Run.method_types method, State state, boolean debug){
Logger.log("TDP.best_test_by");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

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
			
		case ERP:
			best_test = best_test_by_ERP(state, debug);
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
Logger.log("TDP.best_test_by");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

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
	public State update_state(State state, int test_i, int test_outcome, int l){
Logger.log("TDP.update_state");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.update_state");
if (_bug_switch)
	return null;

		//declare vars
		Test test = tests_pool.get_test(test_i);
		StateKey new_key = state.clone_key();
		State new_state;
		
		//start process
		//handle unbuffered state
		new_key.update_key(test_i, test_outcome);
		
		//avoid over calculations
		if (! states_buffer.containsKey(new_key.toString())){
			counter_unbuffered++; //for debug!!!!!!!!
			
			new_state = state.clone();
			new_state.update_spectrum(test.get_part_comps(), test_outcome);
			new_state.add_test_done(test_i);
			new_state.set_key(new_key);
			
			//cache only states in lookahead
			if (l <= lookahead)
				states_buffer.put(new_key.toString(), new_state);
		}
		
		//handle buffered state
		else{
			counter_buffered++; //for debug!!!!!!!!
			new_state = states_buffer.get(new_key.toString());
		}
		
		return new_state;

	}
	
	
	/*********************************
	 * Jpoins together all tie lists.
	 * @param state - State.
	 * @param debug - Debug flag.
	 * @return joint tie-list.
	 *********************************/
	private HashSet<Integer> fabricate_best_tests(State state, boolean debug){
Logger.log("TDP.fabricate_best_tests");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.fabricate_best_tests");
if (_bug_switch)
	return null;

		//initialize
		HashSet<Integer> result = new HashSet<Integer>();
		
		//apply huristic
		switch(TDP_Run.method_of_choice){
			case MDP_BD: 
				best_test_by_BD(state, debug);
				break;
		
			case MDP_HP: 
				best_test_by_HP(state, debug);
				break;
		
			case MDP_ENTROPY: 
				best_test_by_ENTROPY(state, debug);
				break;
		
			case MDP_ERP: 
				best_test_by_ERP(state, debug);
				break;
			
			default: System.out.println("Error - could not fabricate tests list.");
		}
		
		//combine tie lists
		Link current_link = BD_tie_list.get_anchor().get_next();
		while(current_link != null){
			result.add((int)current_link.get_val());
			current_link = current_link.get_next();
		}
		
		current_link = HP_tie_list.get_anchor().get_next();
		while(current_link != null){
			result.add((int)current_link.get_val());
			current_link = current_link.get_next();
		}
		
		current_link = Entropy_tie_list.get_anchor().get_next();
		while(current_link != null){
			result.add((int)current_link.get_val());
			current_link = current_link.get_next();
		}
		
		current_link = ERP_tie_list.get_anchor().get_next();
		while(current_link != null){
			result.add((int)current_link.get_val());
			current_link = current_link.get_next();
		}
		
		
		//wrap
		return result;
	}
	
	
	/**********************************************
	 * Calculates the best test based on MDP.
	 * @param focus_method - MDP sub focus method.
	 * @return the best test based on MDP.
	 **********************************************/
	public int best_test_by_MDP(TDP_Run.method_types focus_method, boolean debug){
Logger.log("TDP.best_test_by_MDP");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.best_test_by_MDP");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;
		
		//initialize
		HashSet<Integer> tests_list = fabricate_best_tests(current_state, debug);
		Test test;
		best_test = -1;
		tests_pool.init_scores(tests_list); //important!!
		max_penalty = tests_list.size(); //tests_pool.get_total_cost(tests_list);
		best_score = Double.POSITIVE_INFINITY;
		
		//for states statistics
		counter_buffered = 0;
		counter_unbuffered = 0;
		
		/////SCAN ALL (already pruned) BEST TESTS/////
		int t; //test index
		Iterator<Integer> iterator = tests_list.iterator();

		while(iterator.hasNext()){
			t = iterator.next();
			test = tests_pool.get_test(t);
			
			//clear memory
			if (states_buffer.size() >= 100){
				states_buffer.clear();
				System.gc();
			}
			
			if (penAssist.size() >= 100){
				penAssist.clear();
				System.gc();
			}
			
			if (debug == true)
				System.out.println("\n" + "Start sampling test-" + t);
			
			//handle base case
			if (current_state.get_best_diag().get_prob() >= min_prob){
				System.out.println("No need for further tests!");
				return -1;
			}
			
			///STATE SPACE///
			if (samples_num <= Math.pow(2,lookahead))
				sample_state_space(t, focus_method, debug);
			else 
				enum_state_space(t, 0, current_state, focus_method, debug);
			
			//track scores
			if (test.get_score() < best_score){
				best_test = t;
				best_score = test.get_score();
			}
		}//end for (tests scan)
		
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
	private double enum_state_space(int t, int l, State state, TDP_Run.method_types focus_method, boolean debug){
Logger.log("TDP.enum_state_space");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.enum_state_space");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

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
			State state0 = update_state(state, t, 0, l);
			State state1 = update_state(state, t, 1, l);
			
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
	public void sample_state_space(int t, TDP_Run.method_types focus_method, boolean debug){
Logger.log("TDP.sample_state_space");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.sample_state_space");
if (_bug_switch)
	return;

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
				if (l == (lookahead - 1) && penAssist.is_stored(penalty_state_key)){
					score = penAssist.get_penalty(penalty_state_key);
					if (debug == true)
						System.out.println("<<Pre-calculated penalty brake>>"); //for debug
					break; 
				}
				
				//simulate the test effect
				test = tests_pool.get_test(new_test_i);
				if (l <= lookahead ){ //within look ahead boundaries
					if (Math.random() <= new_state.calc_prob_for_test(test))
						test_outcome = 0; //test succeeded
					else test_outcome = 1; //test failed
					
					//update state
					new_state = update_state(new_state, new_test_i, test_outcome, l);
				}
				
				if (l == lookahead){//passed lookahead boundary			
					double ratio = new_state.get_entropy() / new_state.get_max_entropy();
					double penalty = ratio * (max_penalty - score);
					score += penalty;
					
					terminal_node = true; //acts as brake;
				}
				
				//update score						
				score += /*(test.get_cost() + */ 1; //+ iteration cost
						
				//for debug
				if (debug == true)
					System.out.println("diagnosis prob: " + new_state.get_best_diag().get_prob()
							+ " || State's entropy: " + new_state.get_entropy()); //for debug
				
				if (terminal_node == false && new_state.get_best_diag().get_prob() >= min_prob)
					terminal_node = true;
				
				//find new best test (if not finished already)
				if (!terminal_node){
					
					//for debug
					if (debug)
						System.out.println(new_state.get_key());
					
					new_test_i = best_test_by(focus_method, new_state, debug);
					//handle "no test found"
					if (new_test_i < 0){
						score = max_penalty;
						terminal_node = true; //acts as break;
					}	
				}//end if (non-terminal node)
				
				//update lookahead counter
				l++; 
			}//end while (look ahead)
			
			//handle cache
			if (l >= lookahead && terminal_node && ! penAssist.is_stored(penalty_state_key))
					penAssist.insert_penalty(penalty_state_key, score);
			
			//update TEST score
			if (score > 0) //ignoring cases where no suitable test found!
				tests_pool.get_test(t).add_to_score(score); //automatically averages
	
		}//end for (samples)
	}
	
	
	/************************************
	 * Prints current state's diagnoses.
	 ************************************/
	public void diagnose_current(){
Logger.log("TDP.diagnose_current");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.diagnose_current");
if (_bug_switch)
	return;

		current_state.print_diagnoses();
	}
	
	
	/******************************************************************************
	 ********************************** For Debug *********************************
	 ******************************************************************************/
	public static void main(String[] args){
Logger.log("TDP.main");
boolean _bug_switch = Bug_Switcher.has_bug("TDP.main");
if (_bug_switch)
	return;

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
		TDP tdp = new TDP(lookahead, samples, 0.9);
		tdp.set_current_state(M, e);
		tdp.set_tests_pool(pool);
		
		//diagnose
//		tdp.diagnose_current();
		System.out.println();
		
		//plan
		int best_test = tdp.best_test_by_MDP(TDP_Run.method_types.ENTROPY,true);
//		int best_test = tdp.best_test_by_MDP("HP");
		
		tdp.tests_pool.print_scores();
		if (! (best_test < 0 ))
			System.out.println("Best next test is: " + best_test );
		
		//print states statistics
		System.out.println();
		System.out.println("States statistics (access count):");
		System.out.println("buffered: " + tdp.counter_buffered);
		System.out.println("unbuffered: " + tdp.counter_unbuffered);
		System.out.println("GD calls: " + Barinel.GD_calls);
	}
}
