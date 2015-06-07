package Planner;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Map.Entry;
import java.util.Set;

import Infrastrcture.Lexer;

public class Tests_Pool {
	private HashMap<Integer,Test> tests;
	private int indexer;
	private Lexer lexer;
	private int total_cost;
	private Object lock = new Object();
	
	//blocking support
	private HashSet<Integer> blocked;
	private HashSet<Integer> unblocked;
	
	//cache
	HashMap<String,Boolean> cache;

	
	/***************
	 * Constructor.
	 ***************/
	public Tests_Pool(){
		tests = new HashMap<Integer,Test>();
		blocked = new HashSet<Integer>();
		unblocked = new HashSet<Integer>();
		cache = new HashMap<String,Boolean>();
		total_cost = -1;
		indexer = 0;
		
		synchronized(lock){
			lexer = new Lexer();
		}
	}
	
	
	/***********************************
	 * Gets a list of unblocked tests.
	 * @return List of unblocked tests.
	 ***********************************/
	public Set<Integer> get_unblocked(){
		return unblocked;
	}
	
	
	/**************************************************************
	 * Refreshes the tests pool, preserving the tests basic trace.
	 **************************************************************/
	public synchronized void refresh(){	
		//process
		unblocked.clear();
		
		for(Test test : tests.values()){
			test.refresh();
			unblocked.add(test.get_index());
		}//end for
		
		blocked.clear();
		cache.clear();
	}
	
	
	/**********************************
	 * Adds a test to the pool.
	 * @param test - test to be added.
	 **********************************/
	public void add_test(Test test){
		int key = indexer;
		test.set_index(key);
		tests.put(key,test);
		unblocked.add(key);
		
		//insert test index to lexer
		synchronized(lexer){
			lexer.add(test.get_base_comps(), key);
		}
			
		//increment indexer
		indexer++;
	}
	
	
	/***********************************************************
	 * Gets all the tests that contain the specified component.
	 * @param comp - Component index.
	 * @return a set of all the indeces of the found tests. 
	 ***********************************************************/
	public Set<Integer> get_all_tests_with_comp(int comp){
		synchronized(lexer){
			return lexer.get_all_that_contain(comp);
		}
	}
	
	
	/*************************************************
	 * Adds a test to the pool.
	 * @param comps - components of test to be added.
	 * @param name - Test's name.
	 *************************************************/
	public void add_test(int[] comps, String name){
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
		return tests.get(test_i);
	}
	
	
	/*********************
	 * Pool size getter.
	 * @return pool size.
	 *********************/
	public int size(){
		return tests.size();
	}
	
	
	/***********************************************************
	 * Calculates the average cost of all tests (integer part).
	 * @return average cost of all tests (integer part).
	 ***********************************************************/
	public int get_avg_cost(){
		return (get_total_cost() / tests.size());
	}
	
	
	/******************************************
	 * Calculates the total cost of all tests.
	 * @return total cost of all tests.
	 ******************************************/
	public int get_total_cost(){
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
		Iterator<Entry<Integer,Test>> iterator = tests.entrySet().iterator();
		Test current_test = null;
		
		while(iterator.hasNext())
			current_test = iterator.next().getValue();
			current_test.init_score();
	}
	
	
	/*****************************
	 * Initializes tests' scores.
	 * @param list - Tests set.
	 ****************************/
	public void init_scores(LinkedList<Integer> list){
		if (list.size() > 0)
			for(int index : list)
				get_test(index).init_score();
		
		
		else
			for(Test test : tests.values())
				test.init_score();	
	}
	
	
	/***************************
	 * Prints all tests scores.
	 ***************************/
	public void print_scores(){
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
		int key = i;
		blocked.add(key);
		unblocked.remove(key);
	}
	
	
	public int[] blocked_tests_comps(){
		int[] ans;
		Set<Integer> comps=new HashSet<Integer>();
		for(int i : blocked){
			Test t=this.tests.get(i);
			for( int c :t.get_part_comps()){
				comps.add(c);
			}
		}
		Object[] compsArr=comps.toArray();
		
		ans=new int[compsArr.length];
		for (int i=0;i<compsArr.length;i++){
			ans[i]=((Integer)compsArr[i]).intValue();
		}
		Arrays.sort(ans);
		return ans;
	}
	
	/********************************************************
	 * Checks whether a test is blocked.
	 * @param i - Test index
	 * @return True - if test is blocked. False - otherwise.
	 ********************************************************/
	public boolean is_test_blocked(int i){	
		return blocked.contains(i);
	}
	
	
	/********************************
	 * Raffles a (not blocked) test.
	 * @return random test.
	 ********************************/
	public int raffle_a_test(){
		//declare vars
		Set<Integer> unblocked_list = get_unblocked();
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

		return test;

	}
	
	
	/********************************
	 * Raffles a (not blocked) test.
	 * @param State - state.
	 * @return random test.
	 ********************************/
	public int raffle_a_test(State state){
		//declare vars
		Set<Integer> unblocked_list = get_unblocked();
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
		
//		System.out.println("Random test: " + test); //for debug

		return test;
	}
	
	
	/**************************
	 * Clears the lexer cache.
	 **************************/
	public void clear_lexer_cache(){
		synchronized(lexer){
			lexer.clear_cache();
		}
	}
	
	
	/**********************************************************************
	 * Checks whether the specified test contains the specified component.
	 * @param test_index - Test's index.
	 * @param comp - Component's index.
	 * @return True - if test contains the component. False - otherwise.
	 **********************************************************************/
	public boolean test_contains(int test_index, int comp){
		//initialize
		boolean result = false;
		String key = "T:" + test_index + "|C:" + comp;
		
		if (!cache.containsKey(key))
			result = true;
		
		else result = tests.get(test_index).contains(test_index);
		
		return result;

	}
}
