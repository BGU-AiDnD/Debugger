package Planner;
import Implant.*;


import java.io.File;
import java.io.FileNotFoundException;
import java.util.Iterator;
import java.util.TreeSet;

import Diagnoser.Diagnosis;
import Implant.TestsRunner;
import Infrastrcture.Linked_List;
import Infrastrcture.OrderAssist;
import Parsing.TraceToCode;

public class Test {
	private int[] part_comps; //participating components
	private int[] base_comps; //base trace
	
	private double icost;  //intrinsic cost
	private double[] score;
	private boolean sorted;
	private String string_id;
	private String name;
	private boolean updated_after_failure;
	private TreeSet<Integer> fastSearcher;
	
	/************************************
	 * Constructor.
	 * @param comps - components number.
	 ************************************/
	public Test(int[] comps, String name){
		part_comps = comps;
		base_comps = null;
		icost = 1;
		score = new double[2];
		score[0] = 0; score[1] = 0;
		sorted = false;
		string_id = "";
		updated_after_failure = false;
		fastSearcher = null;
		this.name = name;
		
	}
	
	
	/********************************
	 * Name getter.
	 * @return The name of the test.
	 ********************************/
	public String get_name(){
Logger.log("Test.get_name");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_name");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return name;
	}
	
	
	/*****************************************
	 * Refreshes all data except COMPS array.
	 *****************************************/
	public void refresh(){
Logger.log("Test.refresh");
boolean _bug_switch = Bug_Switcher.has_bug("Test.refresh");
if (_bug_switch)
	return;

		score = new double[2];
		score[0] = 0; score[1] = 0;
		sorted = false;
		
		//To base mode
		if (updated_after_failure)
			part_comps = base_comps.clone();
		
		fastSearcher = null;
		updated_after_failure = false;
	}
	
	
	/*************************
	 * String ID getter.
	 * @return the string id.
	 *************************/
	public String get_string_id(){
Logger.log("Test.get_string_id");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_string_id");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return string_id;
	}
	
	
	/*************************
	 * String id setter.
	 * @param id - String ID.
	 *************************/
	public void set_string_id(String id){
Logger.log("Test.set_string_id");
boolean _bug_switch = Bug_Switcher.has_bug("Test.set_string_id");
if (_bug_switch)
	return;

		string_id = id;
	}
	
	
	/*************************************************************
	 * Updates participating components according to actual test.
	 * @param coder - Trace Coder.
	 * @throws FileNotFoundException
	 *************************************************************/
	public void update_after_fail(TraceToCode coder){
Logger.log("Test.update_after_fail");
boolean _bug_switch = Bug_Switcher.has_bug("Test.update_after_fail");
if (_bug_switch)
	return;

		//avoid over calculations
		if (updated_after_failure)
			return;
		
		base_comps = part_comps.clone();
		
		//get fix on file
		File file = new File(TestsRunner.WORKSPACE_PATH+"/traces", name + ".txt");
		//update
		try {
			part_comps = coder.fileToArray(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		//wrap
		updated_after_failure = true;
	}
	
	
	/****************************************************
	 * Checks whether this test passes the BD prune.
	 * @param state - State.
	 * @return True - if tets passes. False - otherwise.
	 ****************************************************/
	public boolean pass_prune_test(State state){
Logger.log("Test.pass_prune_test");
boolean _bug_switch = Bug_Switcher.has_bug("Test.pass_prune_test");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		//initialize
		boolean pass = false;
		Iterator<Diagnosis> iterator = state.get_state_diags().iterator();
		
		//process
		int[] temp_diag;
		while (!pass && iterator.hasNext()){
			temp_diag = iterator.next().get_diag();
			
			for(int i=0; i < temp_diag.length; i++){
				if (this.contains(temp_diag[i])){
					pass = true;
					break;
				}
			}//end for (comps)
		}//end while (diagnoses)
		
		//wrap
		return pass;
	}
	
	
	/*****************************************
	 * Participated components vector getter.
	 * @return participated components.
	 *****************************************/
	public int[] get_part_comps(){
Logger.log("Test.get_part_comps");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_part_comps");
if (_bug_switch)
	return null;
	
		return part_comps;
	}

	/*****************************************
	 * Base components vector getter.
	 * @return base components.
	 *****************************************/
	public int[] get_base_comps(){
Logger.log("Test.get_base_comps");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_base_comps");
if (_bug_switch)
	return null;
	
		return base_comps;
	}
	
	
	/*******************
	 * Cost setter.
	 * @param c - cost.
	 *******************/
	public void set_icost(double c){
Logger.log("Test.set_icost");
boolean _bug_switch = Bug_Switcher.has_bug("Test.set_icost");
if (_bug_switch)
	return;

		icost = c;
	}
	
	
	/*******************************
	 * Cost getter.
	 * @return test intrinsic cost.
	 *******************************/
	public double get_cost(){
Logger.log("Test.get_cost");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_cost");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return icost;
	}
	
	
	/*****************************
	 * Adds given value to score.
	 * @param val - score to add.
	 *****************************/
	public void add_to_score(double val){
Logger.log("Test.add_to_score");
boolean _bug_switch = Bug_Switcher.has_bug("Test.add_to_score");
if (_bug_switch)
	return;

		//LHS - numerator. RHS - actual score
		score[1] = score[1] * score[0];
		score[0]++;
		score[1] = (score[1] + val) / score[0];
		
	}
	
	
	/*************************
	 * initializes the score.
	 *************************/
	public void init_score(){
Logger.log("Test.init_score");
boolean _bug_switch = Bug_Switcher.has_bug("Test.init_score");
if (_bug_switch)
	return;

		score[0] = 0;
		score[1] = 0;
	}
	
	
	/************************
	 * Score getter.
	 * @return test's score.
	 ************************/
	public double get_score(){
Logger.log("Test.get_score");
boolean _bug_switch = Bug_Switcher.has_bug("Test.get_score");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return score[1];
	}
	
	
	/*****************************************************************
	 * Looks for a component in the test.
	 * @param comp - component index.
	 * @return True - if component is in the test. False - otherwise.
	 *****************************************************************/
	public boolean contains(int comp){
Logger.log("Test.contains");
boolean _bug_switch = Bug_Switcher.has_bug("Test.contains");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		if (fastSearcher == null){
			fastSearcher = new TreeSet<Integer>();
			for(int i=0; i < part_comps.length; i++)
				fastSearcher.add(part_comps[i]);
		}
		
		return fastSearcher.contains(comp);
	}
	
	
	/*************************************
	 * String representation of the test.
	 *************************************/
	public String toString(){
Logger.log("Test.toString");
boolean _bug_switch = Bug_Switcher.has_bug("Test.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		String result = "";
		
		if (!sorted){
			part_comps = OrderAssist.quickSort(part_comps);
			sorted = true;
		}
		
		Linked_List list;
		list = new Linked_List(part_comps);
		result = list.toString();

		
		return result;
	}


	public void set_base_comps(int[] base_comps) {
Logger.log("Test.set_base_comps");
boolean _bug_switch = Bug_Switcher.has_bug("Test.set_base_comps");
if (_bug_switch)
	return;

		this.base_comps=base_comps;		
	}
}
