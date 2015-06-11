package Planner;
import Implant.*;


import java.util.Hashtable;

public class PenaltyAssist {
	private Hashtable <String, double[]> penalty_buffer = new Hashtable <String, double[]>();
	
	/******************************************
	 * Stores the penalty for the given state.
	 * @param state_key - state key.
	 * @param pnlty - penalty.
	 ******************************************/
	public void insert_penalty(String state_key, double pnlty){
Logger.log("PenaltyAssist.insert_penalty");
boolean _bug_switch = Bug_Switcher.has_bug("PenaltyAssist.insert_penalty");
if (_bug_switch)
	return;

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
Logger.log("PenaltyAssist.size");
boolean _bug_switch = Bug_Switcher.has_bug("PenaltyAssist.size");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return penalty_buffer.size();
	}
	
	
	/*********************
	 * Clears the buffer.
	 *********************/
	public void clear(){
Logger.log("PenaltyAssist.clear");
boolean _bug_switch = Bug_Switcher.has_bug("PenaltyAssist.clear");
if (_bug_switch)
	return;

		penalty_buffer.clear();
	}
	
	
	/************************************************************************
	 * Checks if penalty is stored for given state key.
	 * @param state_key - state key.
	 * @return True - if penalty is stored for state key. False - otherwise.
	 ************************************************************************/
	public boolean is_stored(String state_key){
Logger.log("PenaltyAssist.is_stored");
boolean _bug_switch = Bug_Switcher.has_bug("PenaltyAssist.is_stored");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return penalty_buffer.containsKey(state_key);
	}
	
	
	/***********************************************
	 * Retrieves the penalty for a given state key.
	 * @param state_key - state key.
	 * @return penalty for a given state key.
	 ***********************************************/
	public double get_penalty(String state_key){
Logger.log("PenaltyAssist.get_penalty");
boolean _bug_switch = Bug_Switcher.has_bug("PenaltyAssist.get_penalty");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return penalty_buffer.get(state_key)[0];
	}
}
