package Experimenter;
import Implant.*;


import java.io.IOException;
import java.util.concurrent.ForkJoinPool;

public class TDP_Run {	
	
	//constants
	public static double threshold_prob = 0.9;
	public static int lookahead = 3;
	public static int samples = 20;
	public static int initial_tests_num = 4;
	public static int executions_num = 1;
	public static double random_bugs_ratio = 0.001;
	
	public static method_types method_of_choice = method_types.MDP_ENTROPY; 
	public static initialize_method initial_tests_method = initialize_method.RANDOM;
	public static bug_sim_mode bug_simulation_mode = bug_sim_mode.TAKE_LAST; 
	
	public static boolean debug_mode = false;
	
	//other params
	protected static int comps_num = -1; //adjusted in run-tum
	public enum method_types {MDP_ENTROPY, MDP_BD, MDP_HP, MDP_MC, MDP_ERP, RAFFLE, BD, HP, ENTROPY, ERP};
	public enum initialize_method {RANDOM, PREDEFINED};
	public enum bug_sim_mode {RANDOMIZE_NEW, TAKE_LAST};
	
	//actual (pre-known) tests results will be stored in this:
	public static int[] actual_test_result;
	
	
	/*************************************
	 * Bug simulation mode setter.
	 * @param mode - bug simulation mode.
	 *************************************/
	public static void set_bug_sim_mode(bug_sim_mode mode){
Logger.log("TDP_Run.set_bug_sim_mode");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_bug_sim_mode");
if (_bug_switch)
	return;

		if (bug_simulation_mode != mode){
			bug_simulation_mode = mode;
			System.out.println("\nBug simulation mode was changed to: " + mode);
		}	
	}
	
	
	/***************************************
	 * Probability threshold setter.
	 * @param prob - Threshold probability.
	 ***************************************/
	public static void set_threshold_prob(double prob){
Logger.log("TDP_Run.set_threshold_prob");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_threshold_prob");
if (_bug_switch)
	return;

		if (threshold_prob != prob){
			threshold_prob = prob;
			System.out.println("\nProbability threshold was set to: " + prob);
		}
	}
	
	
	/*********************************
	 * Sets the number of executions.
	 *********************************/
	public static void set_executions_num(int num){
Logger.log("TDP_Run.set_executions_num");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_executions_num");
if (_bug_switch)
	return;

		if (executions_num != num){
			executions_num = num;
			System.out.println("\nExecutions No. was set to: " + num);
		}
	}
	
	
	/**************************************
	 * Sets the planning technique method.
	 **************************************/
	public static void set_plan_method(method_types method){
Logger.log("TDP_Run.set_plan_method");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_plan_method");
if (_bug_switch)
	return;

		if (method_of_choice != method){
			method_of_choice = method;
			System.out.println("\nPlan technique was changed to: " + method);
		}
	}
	
	
	/*********************************
	 * Sets the initial tests method.
	 *********************************/
	public static void set_init_tests(initialize_method method){
Logger.log("TDP_Run.set_init_tests");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_init_tests");
if (_bug_switch)
	return;

		initial_tests_method = method;
		System.out.println("\nInitialize method was changed to: " + method);
	}
	
	
	/*************************************
	 * Inititial tests number setter.
	 * @param num - Initial tests number.
	 *************************************/
	public static void set_init_tests_num(int num){
Logger.log("TDP_Run.set_init_tests_num");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_init_tests_num");
if (_bug_switch)
	return;

		if (initial_tests_num != num){
			initial_tests_num = num;
			System.out.println("\nInitial tests No. was set to: " + num);
		}
	}
	
	
	/*************************************************
	 * Components Number setter.
	 * Should be accessed only by the program itself!
	 * @param num - Componets number parameter.
	 *************************************************/
	public static void set_comps_num(int num){
Logger.log("TDP_Run.set_comps_num");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_comps_num");
if (_bug_switch)
	return;

		comps_num = num;
	}
	
	
	/*****************************
	 * Components number getter.
	 * @return components number.
	 *****************************/
	public static int get_comps_num(){
Logger.log("TDP_Run.get_comps_num");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.get_comps_num");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return comps_num;
	}
	
	
	/*************************************
	 * Lookahead setter.
	 * @param look - Lookahead parameter.
	 *************************************/
	public static void set_lookahead(int look){
Logger.log("TDP_Run.set_lookahead");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_lookahead");
if (_bug_switch)
	return;

		if (lookahead != look){
			lookahead = look;
			System.out.println("\nLookahead was set to: " + look);
		}
	}
	
	
	/************************************
	 * Samples parameter setter.
	 * @param samps - samples parameter.
	 ************************************/
	public static void set_samples(int samps){
Logger.log("TDP_Run.set_samples");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.set_samples");
if (_bug_switch)
	return;

		if (samples != samps){
			samples = samps;
			System.out.println("\nSamples No. was set to: " + samps);
		}
	}
	
	
	////////////////////////////////////Main method///////////////////////////////
	public static void main(String[] Args) throws InterruptedException, IOException{
Logger.log("TDP_Run.main");
boolean _bug_switch = Bug_Switcher.has_bug("TDP_Run.main");
if (_bug_switch)
	return;

		ForkJoinPool fork = new ForkJoinPool();
		
		//build threads
		ExpThread exp1 = new ExpThread();
		
		/////Start experiment!!///////
		fork.submit(exp1);
		
		//wait for threads to complete
		exp1.join();
	}//end Main
}//end TDP_Run class
