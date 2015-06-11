package Planner;
import Implant.*;


import java.util.Hashtable;
import Infrastrcture.Linked_List;
import Infrastrcture.OrderAssist;

public class StateKey {
	//declare vars
	private Linked_List tests_performed;
	private Linked_List outcomes_list; //for easy cloning
	private Hashtable<Integer,Integer> outcomes_hash; //for easy retrieval
	
	
	/*********************
	 * Light Constructor.
	 *********************/
	public StateKey(){
		tests_performed = new Linked_List();
		outcomes_list = new Linked_List();
		outcomes_hash = new Hashtable<Integer,Integer>();
	}
	
	
	/***************
	 * Constructor.
	 ***************/
	public StateKey(Linked_List tests, Linked_List outcomes){
		tests_performed = tests;
		outcomes_list = outcomes;
		outcomes_hash = new Hashtable<Integer,Integer>();
	}
	
	
	/***************
	 * Constructor.
	 ***************/
	public StateKey(StateKey base_key){
		tests_performed = base_key.tests_performed;
		outcomes_list = base_key.outcomes_list;
		outcomes_hash = new Hashtable<Integer,Integer>();	
	}
	
	
	/******************************
	 * Regenerates the hash table.
	 * For cloning purposes.
	 ******************************/
	private void regenerate_hash(){
Logger.log("StateKey.regenerate_hash");
boolean _bug_switch = Bug_Switcher.has_bug("StateKey.regenerate_hash");
if (_bug_switch)
	return;

		//declare vars
		int[] tests = tests_performed.to_int_array();
		int[] outcomes = outcomes_list.to_int_array();
		
		//initialize hash table
		outcomes_hash = new Hashtable<Integer,Integer>();
		
		//handle base case
		if (tests == null)
			return;
		
		//process
		for(int i=0; i<tests.length; i++){	
			//update hash table
			outcomes_hash.put(tests[i], outcomes[i]);
		}
	}
	
	
	/************************
	 * Clones the state key.
	 ************************/
	public StateKey clone(){
Logger.log("StateKey.clone");
boolean _bug_switch = Bug_Switcher.has_bug("StateKey.clone");
if (_bug_switch)
	return null;

		StateKey new_key = new StateKey(tests_performed.clone(), outcomes_list.clone());
		new_key.regenerate_hash();
		
		return new_key;
	}
	
	
	/***************************************************
	 * Updates the state key with new test and outcome.
	 * @param test - test index.
	 * @param outcome - test's outcome.
	 ***************************************************/
	public void update_key(int test, int outcome){
Logger.log("StateKey.update_key");
boolean _bug_switch = Bug_Switcher.has_bug("StateKey.update_key");
if (_bug_switch)
	return;

		//add test index
		tests_performed.add_val(test);
		
		//update outcome list
		outcomes_list.add_val(outcome);
		
		//update hash table of tests outcomes
		outcomes_hash.put(test, outcome);
	}
	
	
	/**************************************************
	 * Generates a String key.
	 * @return String representation of the state key.
	 **************************************************/
	public String toString(){
Logger.log("StateKey.toString");
boolean _bug_switch = Bug_Switcher.has_bug("StateKey.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		//declare var
		String key = "initial";
		int[] tests = tests_performed.to_int_array();

		//process
		if(tests != null){
			tests = OrderAssist.quickSort(tests);
			
			for(int i=0; i<tests.length; i++){
				key += ("|T:" + tests[i] + ",O:" + outcomes_hash.get(tests[i]));
			}//end for
		}//end if
		
		return key;
	}
}
