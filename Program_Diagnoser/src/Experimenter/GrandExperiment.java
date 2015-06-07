package Experimenter;

import java.io.IOException;

import Experimenter.TDP_Run.initialize_method;
import Experimenter.TDP_Run.method_types;

public class GrandExperiment {

	public static void main(String[] args) throws InterruptedException, IOException{
		//set parameters
		TDP_Run.initial_tests_method = initialize_method.BENCHMARK;
		TDP_Run.executions_num = 1;
		TDP_Run.threshold_prob = 0.7;
		TDP_Run.lookahead = 3;
		TDP_Run.samples = 1;
		TDP_Run.initial_tests_num = 4;
		
		///////
		TDP_Run.method_of_choice = method_types.MDP_HP;
		TDP_Run.main(null);
//		
//		///////
//		TDP_Run.method_of_choice = method_types.MDP_BD;
//		TDP_Run.main(null);
//		
//		///////
//		TDP_Run.method_of_choice = method_types.MDP_ENTROPY;
//		TDP_Run.main(null);
		
//		///////
//		TDP_Run.method_of_choice = method_types.MDP_MC;
//		TDP_Run.main(null);
		
//		///////
//		TDP_Run.method_of_choice = method_types.HP;
//		TDP_Run.main(null);
//		
//		///////
//		TDP_Run.method_of_choice = method_types.BD;
//		TDP_Run.main(null);
//		
//		///////
//		TDP_Run.method_of_choice = method_types.ENTROPY;
//		TDP_Run.main(null);
//		
//		///////
//		TDP_Run.method_of_choice = method_types.RAFFLE;
//		TDP_Run.main(null);

	}
}
