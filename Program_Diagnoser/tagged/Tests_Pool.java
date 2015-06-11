package Planner;
import Implant.*;


import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Map.Entry;
import java.util.Set;

public class Tests_Pool {
	private HashMap<Integer,Test> tests;
	private int indexer;
	private int total_cost;
	
	//blocking support
	private HashSet<Integer> blocked;
	private HashSet<Integer> unblocked;

	
	/***************
	 * Constructor.
	 ***************/
	public Tests_Pool(){
		tests = new HashMap<Integer,Test>();
		blocked = new HashSet<Integer>();
		unblocked = new HashSet<Integer>();
		total_cost = -1;
		indexer = 0;
	}
	
	
	/***********************************
	 * Gets a list of unblocked tests.
	 * @return List of unblocked tests.
	 ***********************************/
	public HashSet<Integer> get_unblocked_list(){
Logger.log("Tests_Pool.get_unblocked_list");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_unblocked_list");
if (_bug_switch)
	return null;

		return unblocked;
	}
	
	
	/**************************************************************
	 * Refreshes the tests pool, preserving the tests basic trace.
	 **************************************************************/
	public void refresh(){
Logger.log("Tests_Pool.refresh");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.refresh");
if (_bug_switch)
	return;

		//declare vars
		Iterator<Entry<Integer,Test>> iterator = tests.entrySet().iterator();
		Entry<Integer,Test> entry;
		Test current_test;
		
		//process
		unblocked = new HashSet<Integer>();
		
		while(iterator.hasNext()){
			entry = iterator.next();
			current_test = entry.getValue();
			current_test.refresh();
			
			unblocked.add(entry.getKey());
		}//end while
		
		blocked = new HashSet<Integer>();
	}
	
	
	/**********************************
	 * Adds a test to the pool.
	 * @param test - test to be added.
	 **********************************/
	public void add_test(Test test){
Logger.log("Tests_Pool.add_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.add_test");
if (_bug_switch)
	return;

		int key = indexer;
		test.set_string_id(""+key);
		tests.put(key,test);
		unblocked.add(key);
		
		indexer++;
	}
	
	
	/*************************************************
	 * Adds a test to the pool.
	 * @param comps - components of test to be added.
	 * @param name - Test's name.
	 *************************************************/
	public void add_test(int[] comps, String name){
Logger.log("Tests_Pool.add_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.add_test");
if (_bug_switch)
	return;

		Test test = new Test(comps, name);
		test.set_icost(comps.length);
		add_test(test);
	}
	
	
	
	/*********************************
	 * Test getter.
	 * @param test_i - test index.
	 * @return test with given index.
	 *********************************/
	public Test get_test(int test_i){
Logger.log("Tests_Pool.get_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_test");
if (_bug_switch)
	return null;

		return tests.get(test_i);
	}

	
	/*********************************
	 * Test getter.
	 * @param test_name - test name.
	 * @return index of a test with the given name (caution: if many names with the same test, then we're screwed).
	 *********************************/
	public int get_index(String test_name){
Logger.log("Tests_Pool.get_index");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_index");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		for (Integer key : tests.keySet()){
			if (tests.get(key).equals(test_name)){
				return key;
			}
		}
		return -1;
	}
	
	
	/*********************
	 * Pool size getter.
	 * @return pool size.
	 *********************/
	public int size(){
Logger.log("Tests_Pool.size");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.size");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return tests.size();
	}
	
	
	/***********************************************************
	 * Calculates the average cost of all tests (integer part).
	 * @return average cost of all tests (integer part).
	 ***********************************************************/
	public int get_avg_cost(){
Logger.log("Tests_Pool.get_avg_cost");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_avg_cost");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return (get_total_cost() / tests.size());
	}
	
	
	/******************************************
	 * Calculates the total cost of all tests.
	 * @return total cost of all tests.
	 ******************************************/
	public int get_total_cost(){
Logger.log("Tests_Pool.get_total_cost");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_total_cost");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//use cache
		if (total_cost < 0){
			//declare vars
			total_cost = 0;
			Iterator<Entry<Integer,Test>> iterator = tests.entrySet().iterator();
			Test current_test = null;
			
			//start calculation
			while(iterator.hasNext()){
				current_test = iterator.next().getValue();
				total_cost += (1 + current_test.get_cost()); //including iterations cost	
			}
		}//end if
		
		return total_cost;
	}
	
	
	/******************************************
	 * Calculates the total cost of all tests.
	 * @return total cost of all tests.
	 ******************************************/
	public int get_total_cost(Set<Integer> test_list){
Logger.log("Tests_Pool.get_total_cost");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.get_total_cost");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//use cache
		if (total_cost < 0){
			//declare vars
			total_cost = 0;
			Iterator<Integer> iterator = test_list.iterator();
			Test current_test = null;
			
			//start calculation
			while(iterator.hasNext()){
				current_test = get_test(iterator.next());
				total_cost += current_test.get_cost();	
			}
		}//end if
		
		return total_cost;
	}
	
	
	/*****************************
	 * Initializes tests' scores.
	 *****************************/
	public void init_scores(){
Logger.log("Tests_Pool.init_scores");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.init_scores");
if (_bug_switch)
	return;

		Iterator<Entry<Integer,Test>> iterator = tests.entrySet().iterator();
		Test current_test = null;
		
		while(iterator.hasNext())
			current_test = iterator.next().getValue();
			current_test.init_score();
	}
	
	
	/*****************************
	 * Initializes tests' scores.
	 * @param set - Tests set.
	 ****************************/
	public void init_scores(Set<Integer> set){
Logger.log("Tests_Pool.init_scores");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.init_scores");
if (_bug_switch)
	return;

		Iterator<Integer> iterator = set.iterator();
		Test test;
		while(iterator.hasNext()){
			test = get_test(iterator.next());
			test.init_score();
		}
	}
	
	
	/***************************
	 * Prints all tests scores.
	 ***************************/
	public void print_scores(){
Logger.log("Tests_Pool.print_scores");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.print_scores");
if (_bug_switch)
	return;

		Iterator<Entry<Integer,Test>> iterator = tests.entrySet().iterator();
		Entry<Integer,Test> entry;
		Test current_test = null;
		
		//process
		System.out.println("Scores:");	
		while(iterator.hasNext()){
			entry = iterator.next();
			current_test = entry.getValue();
			System.out.print(" |" + entry.getKey() + ": ");
			System.out.print(current_test.get_score());
		}
		
		System.out.println("");
	}
	
	
	/*************************
	 * Blocks a test.
	 * @param i - Test index.
	 *************************/
	public void block_test(int i){
Logger.log("Tests_Pool.block_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.block_test");
if (_bug_switch)
	return;

		int key = i;
		blocked.add(key);
		unblocked.remove(key);
	}
	
	
	/********************************************************
	 * Checks whether a test is blocked.
	 * @param i - Test index
	 * @return True - if test is blocked. False - otherwise.
	 ********************************************************/
	public boolean is_test_blocked(int i){
Logger.log("Tests_Pool.is_test_blocked");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.is_test_blocked");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;
	
		return blocked.contains(i);
	}
	
	
	/********************************
	 * Raffles a (not blocked) test.
	 * @return random test.
	 ********************************/
	public int raffle_a_test(){
Logger.log("Tests_Pool.raffle_a_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.raffle_a_test");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		HashSet<Integer> unblocked_list = get_unblocked_list();
		Iterator<Integer> iterator = unblocked_list.iterator();
		int test = -1;
						
		//detect "all tests blocked" scenario
		if (unblocked_list.size() <= 0)
			return -1;
	
		//raffle
		int index = (int)(Math.random() * (unblocked_list.size()))+1;
		for(int i=1; i < index; i++)
			iterator.next();
		test = iterator.next();
		
//		System.out.println("Random test: " + test);

		return test;

	}
	
	
	/********************************
	 * Raffles a (not blocked) test.
	 * @param State - state.
	 * @return random test.
	 ********************************/
	public int raffle_a_test(State state){
Logger.log("Tests_Pool.raffle_a_test");
boolean _bug_switch = Bug_Switcher.has_bug("Tests_Pool.raffle_a_test");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//declare vars
		HashSet<Integer> unblocked_list = get_unblocked_list();
		Iterator<Integer> iterator = unblocked_list.iterator();
		int test = -1;
						
		//get all valid tests
		int t;
		LinkedList<Integer> valid_list = new LinkedList<Integer>();
		while(iterator.hasNext()){
			t = iterator.next();
			if (!state.is_test_done(t))
				valid_list.add(t);
		}//end while
		
		//detect "all tests blocked" scenario
		if (valid_list.size() <= 0)
			return -1;
		
		//raffle
		int index = (int)(Math.random() * (valid_list.size()));
		test = valid_list.get(index);
		
//		System.out.println("Random test: " + test);

		return test;
	}
}
