package Diagnoser;

import java.util.HashMap;
import java.util.TreeSet;
import java.util.regex.Pattern;

import Infrastrcture.Linked_List;
import Infrastrcture.OrderAssist;

public class Diagnosis implements Comparable<Diagnosis>{
	private int[] diagnosis;
	private double probability;
	private HashMap<Integer,Double> h_list;
	private boolean sorted;
	private TreeSet<Integer> fastSearcher;
	
	/***************
	 * Constructor.
	 ***************/
	public Diagnosis(){
		diagnosis = null;
		probability = 0.0;
		h_list = new HashMap<Integer, Double>();
		sorted = false;
		fastSearcher = new TreeSet<Integer>();
	}
	
	
	/*****************************
	 * Compare to implementation.
	 *****************************/
	public int compareTo(Diagnosis diag){
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
		h_list = new HashMap<Integer,Double>();
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
		probability = prob;
	}
	
	
	/************************
	 * Raw diagnosis getter.
	 * @return diagnosis.
	 ************************/
	public int[] get_diag(){
		return diagnosis;
	}
	
	
	/*********************************
	 * Probability getter.
	 * @return diagnosis probability.
	 *********************************/
	public double get_prob(){
		return probability;
	}
	
	
	/*****************************************************
	 * Sets the h list of the diagnosis.
	 * @param raw_params - PSO solution space parameters.
	 *****************************************************/
	public void set_h_list(double[] raw_params){
//		//declare vars
//		double[] h_vector = new double[diagnosis.length];
//		h_list = new Linked_List(); //obselete!
//		
//		
//		for(int i=0; i < h_vector.length; i++){
//			//sinusalize the parameters
//			h_vector[i] = (Math.sin(raw_params[i]) + 1 ) / 2;   //was relevant to old PSO!! 
//			
//			//build the list
//			h_list.add_by_order(diagnosis[i], h_vector[i]);
//		}//end for
		
		for(int i=0; i < raw_params.length; i++)
			h_list.put(diagnosis[i], raw_params[i]);
	}
	
	
	/*****************
	 * h-list getter.
	 * @return h list.
	 *****************/
	public HashMap<Integer,Double> get_h_list(){
		return h_list;
	}
	
	
	/**********************************************************************
	 * checks whether the diagnosis includes a given component.
	 * @param comp - component index.
	 * @return True - if diagnosis includes component. False - otherwise.
	 **********************************************************************/
	public boolean contains(int comp){	
		return fastSearcher.contains(comp); 
	}
	
	
	/********************
	 * Produces pattern.
	 * @return pattern.
	 ********************/
	public Pattern produce_pattern(){
		//initialize
		String pattern = ".*";
		
		//sort
		if (!sorted){
			diagnosis = OrderAssist.quickSort(diagnosis);
			sorted = true;
		}
		
		//process
		for(int comp : diagnosis)
			pattern += "," + comp + ",";
		
		//wrap
		pattern += ".*"; //pattern.replaceFirst("|", ".");
		return Pattern.compile(pattern);
	}
	
	
	/******************************************
	 * String representation of the diagnosis.
	 ******************************************/
	public String toString(){
		if (!sorted){
			diagnosis = OrderAssist.quickSort(diagnosis);
			sorted = true;
		}
		
		return (new Linked_List(diagnosis).toString());
	}
}
