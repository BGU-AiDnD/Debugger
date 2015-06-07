package Experimenter;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.ForkJoinPool;

import Parsing.FilesAssist;
import Parsing.TraceToCode;
import Planner.Tests_Pool;

public class TDP_Run {	
	
	//input parameters
	public static double threshold_prob = 0.7;
	public static int lookahead = 3;
	public static int samples = 5;
	public static int initial_tests_num = 4;
	public static int executions_num = 1;
	public static double random_bugs_ratio = 3.0 / 3000.0;
	
	public static method_types method_of_choice = method_types.MDP_ENTROPY; 
	public static initialize_method initial_tests_method = initialize_method.RANDOM;
	public static bug_sim_mode bug_simulation_mode = bug_sim_mode.TAKE_LAST; 
	public static method_types fuzzy_supports = method_types.ENTROPY;
	
	public static boolean debug_mode = false;
	public static boolean use_entropy_foul = true;
	public static TraceToCode testsCoder;
	
	//mechanism params
	protected static int comps_num = -1; //adjusted in run-tum
	public enum method_types {MDP_ENTROPY, MDP_BD, MDP_HP, MDP_MC, RAFFLE, BD, HP, ENTROPY, ORACLE, FUZZY};
	public enum initialize_method {RANDOM, BENCHMARK};
	public enum bug_sim_mode {RANDOMIZE_NEW, TAKE_LAST};
	
	//run-time determined params
	public static int[] actual_test_result;
	public static int[] bugged_comps;
	public static Tests_Pool tests_pool;
	
	
	/*************************************
	 * Bug simulation mode setter.
	 * @param mode - bug simulation mode.
	 *************************************/
	public static void set_bug_sim_mode(bug_sim_mode mode){
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
		if (threshold_prob != prob){
			threshold_prob = prob;
			System.out.println("\nProbability threshold was set to: " + prob);
		}
	}
	
	
	/*********************************
	 * Sets the number of executions.
	 *********************************/
	public static void set_executions_num(int num){
		if (executions_num != num){
			executions_num = num;
			System.out.println("\nExecutions No. was set to: " + num);
		}
	}
	
	
	/**************************************
	 * Sets the planning technique method.
	 **************************************/
	public static void set_plan_method(method_types method){
		if (method_of_choice != method){
			method_of_choice = method;
			System.out.println("\nPlan technique was changed to: " + method);
		}
	}
	
	
	/*********************************
	 * Sets the initial tests method.
	 *********************************/
	public static void set_init_tests(initialize_method method){
		initial_tests_method = method;
		System.out.println("\nInitialize method was changed to: " + method);
	}
	
	
	/*************************************
	 * Inititial tests number setter.
	 * @param num - Initial tests number.
	 *************************************/
	public static void set_init_tests_num(int num){
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
		comps_num = num;
	}
	
	
	/*****************************
	 * Components number getter.
	 * @return components number.
	 *****************************/
	public static int get_comps_num(){
		return comps_num;
	}
	
	
	/*************************************
	 * Lookahead setter.
	 * @param look - Lookahead parameter.
	 *************************************/
	public static void set_lookahead(int look){
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
		if (samples != samps){
			samples = samps;
			System.out.println("\nSamples No. was set to: " + samps);
		}
	}
	
	
	////////////////////////////////////Main method///////////////////////////////
	public static void main(String[] Args) throws InterruptedException, IOException{
		//initialize
		ForkJoinPool fork = new ForkJoinPool();
		ExpThread exp1 = null;
		
		//setup experiment according to user selection
		switch (initial_tests_method){
			case BENCHMARK:
				//run on all instances
				File[] instances = FilesAssist.get_all_benchmark_files();
				for (File instance : instances){
					exp1 = new ExpThread(instance);
					
					/////Start experiment!!///////
					fork.submit(exp1);
					
					//wait for threads to complete
					exp1.join();	
				}
				break;
			
			case RANDOM:
				exp1 = new ExpThread();
				
				/////Start experiment!!///////
				fork.submit(exp1);
				
				//wait for threads to complete
				exp1.join();
				break;
		}
		

	}//end Main
}//end TDP_Run class