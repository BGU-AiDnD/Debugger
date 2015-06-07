package Planner;

import java.util.Hashtable;

public class PenaltyAssist {
	private Hashtable <String, double[]> penalty_buffer = new Hashtable <String, double[]>();
	
	/******************************************
	 * Stores the penalty for the given state.
	 * @param state_key - state key.
	 * @param pnlty - penalty.
	 ******************************************/
	public void insert_penalty(String state_key, double pnlty){
		//convert penalty
		double[] penalty = new double[1];
		penalty[0] = pnlty;
		
		//add into buffer
		penalty_buffer.put(state_key, penalty);
	}
	
	
	/*************************
	 * Size getter.
	 * @return buffer's size.
	 *************************/
	public int size(){
		return penalty_buffer.size();
	}
	
	
	/*********************
	 * Clears the buffer.
	 *********************/
	public void clear(){
		penalty_buffer.clear();
	}
	
	
	/************************************************************************
	 * Checks if penalty is stored for given state key.
	 * @param state_key - state key.
	 * @return True - if penalty is stored for state key. False - otherwise.
	 ************************************************************************/
	public boolean is_stored(String state_key){
		return penalty_buffer.containsKey(state_key);
	}
	
	
	/***********************************************
	 * Retrieves the penalty for a given state key.
	 * @param state_key - state key.
	 * @return penalty for a given state key.
	 ***********************************************/
	public double get_penalty(String state_key){
		double result = penalty_buffer.get(state_key)[0];
		
		//clear memory
		if (penalty_buffer.size() >= 1000){
			penalty_buffer.clear();
			System.out.println("/n>>>penalty buffer was cleaned."); //for debug
		}

		return result;
	}
}
