package Planner;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.regex.Pattern;

import Diagnoser.Diagnosis;
import Experimenter.TDP_Run;
import Infrastrcture.OrderAssist;
import Parsing.TraceToCode;

public class Test {
	public static enum comps_states {ACTUAL_COMPS, BASE_COMPS};
	
	private comps_states comps_state;
	private int[] part_comps; //participating components
	private int[] base_comps; //base trace
	
	private double icost;  //intrinsic cost
	private double[] score;
	private boolean sorted;
	private int index;
	private String name;
	private String comps_string;
	private HashSet<Integer> fastSearcher;
	
	
	/********************************************
	 * Constructor.
	 * @param comps - (sorted) components array.
	 * @param name - Test's name.
	 ********************************************/
	public Test(int[] comps, String name){
		part_comps = null;
		base_comps = comps;
		comps_state = comps_states.BASE_COMPS;
		comps_string = toString();
		fastSearcher = new HashSet<Integer>();
		
		icost = 1;
		score = new double[2];
		score[0] = 0; score[1] = 0;
		
		sorted = false;
		index = -1;
		
		this.name = name;
		
	}
	
	
	/********************************
	 * Name getter.
	 * @return The name of the test.
	 ********************************/
	public String get_name(){
		return name;
	}
	
	
	/*****************************************
	 * Refreshes all data except COMPS arrays.
	 *****************************************/
	public void refresh(){
		synchronized (this){
			score = new double[2];
			score[0] = 0; score[1] = 0;
			sorted = false;
			
			//To base mode
			comps_state = comps_states.BASE_COMPS;
			
			fastSearcher.clear();
		}
	}
	
	
	/*************************
	 * String ID getter.
	 * @return the string id.
	 *************************/
	public int get_index(){
		return index;
	}
	
	
	/*************************
	 * String id setter.
	 * @param id - String ID.
	 *************************/
	public void set_index(int id){
		index = id;
	}
	
	
	/**************************************************************
	 * Updates participating components according to actual test.
	 * @param coder - Trace Coder.
	 * @param force - Set to TRUE if updating should ignore cache. 
	 * (in case trace-files themeselves have been altered).
	 * @throws FileNotFoundException
	 **************************************************************/
	public void update_after_fail(TraceToCode coder, boolean force){
		//avoid over calculations
		if (base_comps != null && part_comps != null && !force){
			fastSearcher.clear();
			comps_state = comps_states.ACTUAL_COMPS;
			return;
		}
		
		//get fix on files
		File base_file 	= new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces/base", name + ".txt");
		File trace_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces", name + ".txt");
		
		//update
		try {
			base_comps = coder.fileToArray(base_file);
			part_comps = coder.fileToArray(trace_file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		//wrap
		fastSearcher.clear();
		comps_state = comps_states.ACTUAL_COMPS;
	}
	
	
	/*****************************************************************************************
	 * Checks whether this test contains any components in common with the state's diagnoses.
	 * @param state - State.
	 * @return True - if tet passes. False - otherwise.
	 *****************************************************************************************/
	public boolean prune_by_diags_test(State state){
		//initialize
		boolean pass = false;
		Iterator<Diagnosis> iterator = state.get_state_diags().iterator();
		
		//process
		int[] temp_diag;
		while (!pass && iterator.hasNext()){
			temp_diag = iterator.next().get_diag();
			
			for(int i=0; i < temp_diag.length; i++){
//				if (this.contains(temp_diag[i])){
				if (TDP.tests_pool.test_contains(this.index, temp_diag[i])){
					pass = true;
					break;
				}
			}//end for (comps)
		}//end while (diagnoses)
		
		//wrap
		return pass;
	}
	
	
	/************************************************
	 * ACTUAL Participated components vector getter.
	 * @return participated components.
	 ************************************************/
	public int[] get_part_comps(){	
		//handle null
		if (part_comps == null){
			//get fix on file
			File trace_file = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces", name + ".txt");
			
			//update
			try {
				part_comps = TDP_Run.testsCoder.fileToArray(trace_file);
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}//end if
		
		return part_comps;
	}
	
	
	/*****************************************
	 * Participating comps setter.
	 * @param comps - Components codes array.
	 *****************************************/
	public void set_part_comps(int[] comps){
		part_comps = comps;
	}
	
	
	/*******************
	 * Cost setter.
	 * @param c - cost.
	 *******************/
	public void set_icost(double c){
		icost = c;
	}
	
	
	/*******************************
	 * Cost getter.
	 * @return test intrinsic cost.
	 *******************************/
	public double get_cost(){
		return icost;
	}
	
	
	/*****************************
	 * Adds given value to score.
	 * @param val - score to add.
	 *****************************/
	public void add_to_score(double val){
		//LHS - numerator. RHS - actual score
		score[1] = score[1] * score[0];
		score[0]++;
		score[1] = (score[1] + val) / score[0];
		
	}
	
	
	/*************************
	 * initializes the score.
	 *************************/
	public void init_score(){
		score[0] = 0;
		score[1] = 0;
	}
	
	
	/************************
	 * Score getter.
	 * @return test's score.
	 ************************/
	public double get_score(){
		return score[1];
	}
	
	
	/******************************************************************************************
	 * Checks wether this test contains any of the given components.
	 * @param comps - components indexes array.
	 * @return True - if the tests contains at least one of the components. False - otherwise.
	 ******************************************************************************************/
	public boolean contains_any(int[] comps){
		//initialize
		boolean contains = false;
		
		//process
		for(int i=0; i < comps.length; i++){
			contains = contains(comps[i]);
			
			if (contains)
				break;
		}
		
		//wrap
		return contains;
	}
	
	
	/*****************************************************************
	 * Looks for a component in the test.
	 * @param comp - component index.
	 * @return True - if component is in the test. False - otherwise.
	 *****************************************************************/
	public boolean contains(int comp){
		synchronized (this){
			//take advantage of the fact that the test-trace is sorted
			int[] comps = get_active_comps();
			if ((comp > comps[comps.length - 1]) || (comp < comps[0]))
				return false;
			
			for(int i=0; i < comps.length; i++){
				if (comps[i] == comp)
					return true;
			}
			
			return false;
		}
			
//			if (fastSearcher.size() == 0){
//				fastSearcher = new HashSet<Integer>();
//				
//				for(int i=0; i < comps.length; i++)
//					fastSearcher.add(comps[i]);
//			}
//			
//			return fastSearcher.contains(comp);
//		}
	}
	
	
	/************************************************************************
	 * Looks for a pattern in the test's (sorted) trace.
	 * @param p - Pattern.
	 * @return True - if the specified pattern was found. False - otherwise.
	 ************************************************************************/
	public boolean contains(Pattern p){
		return p.matcher(this.toString()).matches();
	}
	
	
	/**************************************************************************
	 * Active components getter.
	 * Result depends on the component state switch.
	 * @return array of trace components indices, according to the test state.
	 **************************************************************************/
	private int[] get_active_comps(){
		switch(comps_state){
			case ACTUAL_COMPS:
				return part_comps;
			
			case BASE_COMPS:
				return base_comps;
			
			default: return null;
		}
	}
	
	
	/*************************************
	 * String representation of the test.
	 *************************************/
	public String toString(){
		//avoid over-calculation
		if (comps_string != null && !comps_string.equals(""))
			return comps_string;
		
		String result = "";
		
		if (!sorted){
			base_comps = OrderAssist.quickSort(base_comps);
			sorted = true;
		}
		
		for(int comp : base_comps)
			result += "," + comp;
		
		//wrap
		result += ",";
		return result;
	}
	

	/*****************************************
	 * Base components vector getter.
	 * @return base components.
	 *****************************************/
	public int[] get_base_comps(){	
		return base_comps;
	}
	
	
	/*********************************************
	 * Base components setter.
	 * @param base_comps - Base components array.
	 *********************************************/
	public void set_base_comps(int[] base_comps) {
		this.base_comps = base_comps;		
	}
}
