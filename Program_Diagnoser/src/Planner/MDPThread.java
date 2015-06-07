package Planner;

import java.util.LinkedList;
import java.util.concurrent.ForkJoinTask;

import Experimenter.TDP_Run;

public class MDPThread extends ForkJoinTask<Object>{
	private static final long serialVersionUID = 1L;
	
	//local vars
	private final boolean debug_mode = TDP_Run.debug_mode;
	private LinkedList<Integer> tests_list;
	private TDP_Run.method_types focus_method;
	
	private Test test;
	public double best_score;
	public int best_test;
	private int result;
	
	
	/********************************************
	 * Constructor.
	 * @param tests_list - List of test indices.
	 * @param focus_method - Focus method.
	 ********************************************/
	public MDPThread(LinkedList<Integer> tests_list, TDP_Run.method_types focus_method){
		this.tests_list = tests_list;
		this.focus_method = focus_method;
		
		best_score = Double.POSITIVE_INFINITY;
		best_test = -1;
	}
	
	/********************
	 * Execution method.
	 ********************/
	public boolean exec(){
		for(int t : tests_list){
			test = TDP.tests_pool.get_test(t);
			
			//handle base case
			if (TDP.current_state.get_best_diag().get_prob() >= TDP.min_prob){
				result = -1;
				this.complete(0);
			}
			
			///STATE SPACE///
			if (TDP.samples_num <= Math.pow(2,TDP.lookahead))
				TDP.sample_state_space(t, focus_method, debug_mode);
			else 
				TDP.enum_state_space(t, 0, TDP.current_state, focus_method, debug_mode);
			
			//track scores
			if (test.get_score() < best_score){
				best_test = t;
				best_score = test.get_score();
			}
		}//end for (tests scan)
		
		//wrap
		result = best_test;
		return true;
	}
	
	
	/***********************************
	 * Result getter.
	 * @return the resulted test index.
	 ***********************************/
	public int get_result(){
		return result;
	}
	
	
	@Override
	public Object getRawResult() {
		//unimplemented
		return null;
	}


	@Override
	protected void setRawResult(Object arg0) {
		//unimplemented
		
	}
}
