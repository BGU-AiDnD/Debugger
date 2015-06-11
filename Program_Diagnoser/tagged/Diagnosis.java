package Diagnoser;
import Implant.*;


import java.util.TreeSet;

import Infrastrcture.Linked_List;
import Infrastrcture.OrderAssist;

public class Diagnosis implements Comparable<Diagnosis>{
	private int[] diagnosis;
	private double probability;
	private Linked_List h_list;
	private boolean sorted;
	private TreeSet<Integer> fastSearcher;
	
	/***************
	 * Constructor.
	 ***************/
	public Diagnosis(){
		diagnosis = null;
		probability = 0.0;
		h_list = null;
		sorted = false;
		fastSearcher = new TreeSet<Integer>();
	}
	
	
	/*****************************
	 * Compare to implementation.
	 *****************************/
	public int compareTo(Diagnosis diag){
Logger.log("Diagnosis.compareTo");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.compareTo");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		if (diag == this)
			return 0;
		
		else if (this.probability > diag.probability)
			return 1;
		
		else if (this.probability < diag.probability)
			return -1;
		
		else return this.toString().compareTo(diag.toString());
	}
	
	
	/***************************
	 * Enhanced constructor.
	 * @param diag - diagnosis.
	 ***************************/
	public Diagnosis(int[] diag){
		diagnosis = diag.clone();
		probability = 0.0;
		h_list = null;
		sorted = false;
		
		//load components to tree-set
		fastSearcher = new TreeSet<Integer>();
		for(int i = 0; i < diag.length; i++)
			fastSearcher.add(diag[i]);
	}
	
	
	/***************************
	 * Sets diagnosis.
	 * @param diag - diagnosis.
	 ***************************/
	public void set_diag(int[] diag){
Logger.log("Diagnosis.set_diag");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.set_diag");
if (_bug_switch)
	return;

		diagnosis = diag.clone();
		
		//update fastSearcher
		fastSearcher = new TreeSet<Integer>();
		for(int i = 0; i < diag.length; i++)
			fastSearcher.add(diag[i]);
	}
	
	
	/******************************
	 * Sets diagnosis probability.
	 * @param prob - probability.
	 ******************************/
	public void set_prob(double prob){
Logger.log("Diagnosis.set_prob");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.set_prob");
if (_bug_switch)
	return;

		probability = prob;
	}
	
	
	/************************
	 * Raw diagnosis getter.
	 * @return diagnosis.
	 ************************/
	public int[] get_diag(){
Logger.log("Diagnosis.get_diag");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.get_diag");
if (_bug_switch)
	return null;

		return diagnosis;
	}
	
	
	/*********************************
	 * Probability getter.
	 * @return diagnosis probability.
	 *********************************/
	public double get_prob(){
Logger.log("Diagnosis.get_prob");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.get_prob");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return probability;
	}
	
	
	/*****************************************************
	 * Sets the h list of the diagnosis.
	 * @param raw_params - PSO solution space parameters.
	 *****************************************************/
	public void set_h_list(double[] raw_params){
Logger.log("Diagnosis.set_h_list");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.set_h_list");
if (_bug_switch)
	return;

		//declare vars
		double[] h_vector = new double[diagnosis.length];
		h_list = new Linked_List(); 
		
		for(int i=0; i < h_vector.length; i++){
			//sinusalize the parameters
			h_vector[i] = (Math.sin(raw_params[i]) + 1 ) / 2;
			
			//build the list
			h_list.add_by_order(diagnosis[i], h_vector[i]);
		}//end for
	}
	
	
	/*****************
	 * h-list getter.
	 * @return h list.
	 *****************/
	public Linked_List get_h_list(){
Logger.log("Diagnosis.get_h_list");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.get_h_list");
if (_bug_switch)
	return null;

		return h_list;
	}
	
	
	/**********************************************************************
	 * checks whether the diagnosis includes a given component.
	 * @param comp - component index.
	 * @return True - if diagnosis includes component. False - otherwise.
	 **********************************************************************/
	public boolean contains(int comp){
Logger.log("Diagnosis.contains");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.contains");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;
	
		return fastSearcher.contains(comp); 
	}
	
	
	/******************************************
	 * String representation of the diagnosis.
	 ******************************************/
	public String toString(){
Logger.log("Diagnosis.toString");
boolean _bug_switch = Bug_Switcher.has_bug("Diagnosis.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		if (!sorted){
			diagnosis = OrderAssist.quickSort(diagnosis);
			sorted = true;
		}
		
		return (new Linked_List(diagnosis).toString());
	}
}
