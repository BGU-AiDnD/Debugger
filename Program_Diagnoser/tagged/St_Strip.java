package Diagnoser;
import Implant.*;


import java.util.LinkedList;

import Infrastrcture.Linked_List;

public class St_Strip {
	private boolean[] comps;
	private boolean[] conflicts;
	
	private int[] unstripped_comps_array;
	private int[] unstripped_confs_array;
	
	private int[] last_unstripped_comps;
	private int[] last_unstripped_confs;
	
	private LinkedList<Integer> conflict_list;
	
	protected Ochiai_Rank[] ochiai_ranks;
	
	/****************************
	 * Constructor.
	 * @param M - components No.
	 * @param N - sets No.
	 ****************************/
	public St_Strip(int M, int N){
		comps = new boolean[M];
		conflicts = new boolean[N];
		
		//Initialize 
		for(int m=0; m<M; m++)
			comps[m] = false;
		
		for(int n=0; n<N; n++)
			conflicts[n] = false;
		
		last_unstripped_comps = null;
		last_unstripped_confs = null;
		
		conflict_list = null;
		
		ochiai_ranks = null;
	}
	
	
	/****************************************
	 * Constructor.
	 * @param com - components strip vector.
	 * @param con - conflicts strip vector.
	 ****************************************/
	public St_Strip(boolean[] com, boolean[] con, int[] last_un_comps, int[] last_un_confs){
		//copy knowledge
		comps = com.clone();
		conflicts = con.clone();
		
		if (last_un_comps != null)
			last_unstripped_comps = last_un_comps.clone();
		
		if (last_un_confs != null)
			last_unstripped_confs = last_un_confs.clone();
		
		conflict_list = null;
		ochiai_ranks = null;
	}
	
	
	/****************************************************************
	 * Assambles a list of all true conflicts (e = 1 && unstripped).
	 * @return a list of all true conflicts.
	 ****************************************************************/
	public LinkedList<Integer> get_conflic_list(int[] e){
Logger.log("St_Strip.get_conflic_list");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.get_conflic_list");
if (_bug_switch)
	return null;

		if (conflict_list != null)
			return conflict_list;
			
		else{
			conflict_list = new LinkedList<Integer>();
			for(int i = 0; i < e.length; i++)
				if (e[i] == 1 && conflicts[i] == false)
					conflict_list.add(i);
			
			return conflict_list;
		}
	}
	
	
	/*****************************************
	 * Clones the Ochiai ranks knowledge.
	 * @return Cloned Ochiai ranks knowledge.
	 *****************************************/
	private Ochiai_Rank[] clone_ochiai_ranks(){
Logger.log("St_Strip.clone_ochiai_ranks");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.clone_ochiai_ranks");
if (_bug_switch)
	return null;

		Ochiai_Rank[] clone = new Ochiai_Rank[ochiai_ranks.length];
		
		for(int i=0; i < ochiai_ranks.length; i++)
			clone[i] = ochiai_ranks[i].clone();
		
		return clone;
	}
	
	
	/******************************
	 * Clones the strip knowledge.
	 ******************************/
	public St_Strip clone(){
Logger.log("St_Strip.clone");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.clone");
if (_bug_switch)
	return null;

		St_Strip clone = new St_Strip(comps, conflicts, unstripped_comps_array(), unstripped_confs_array());
		clone.ochiai_ranks = clone_ochiai_ranks();
		
		return clone;
	}
	
	
	/*********************************************
	 * Removes Component from matrix (logically).
	 * @param comp - component to be stripped.
	 *********************************************/
	public void strip_comp(int comp){
Logger.log("St_Strip.strip_comp");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.strip_comp");
if (_bug_switch)
	return;

		comps[comp] = true;
		last_unstripped_comps = unstripped_comps_array;
		unstripped_comps_array = null;
	}
	
	/**********************************************
	 * Removes conflict from matrix (logically).
	 * @param conf - conflict to be stripped.
	 **********************************************/
	public void strip_conf(int conf){
Logger.log("St_Strip.strip_conf");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.strip_conf");
if (_bug_switch)
	return;

		conflicts[conf] = true;
		last_unstripped_confs = unstripped_confs_array;
		unstripped_confs_array = null;
	}
	
	
	/*********************************************************************
	 * checks whether component has been stripped.
	 * @param comp - component to be checked.
	 * @return True - if component has been stripped. False - otherwise.
	 *********************************************************************/
	public boolean is_comp_stripped(int comp){
Logger.log("St_Strip.is_comp_stripped");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.is_comp_stripped");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return comps[comp];
	}
	
	/*********************************************************************
	 * checks whether conflict has been stripped.
	 * @param conf - conflict to be checked.
	 * @return True - if conflict has been stripped. False - otherwise.
	 *********************************************************************/
	public boolean is_conf_stripped(int conf){
Logger.log("St_Strip.is_conf_stripped");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.is_conf_stripped");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return conflicts[conf];
	}
	
	
	/***************************************************
	 * Updates Ochiai ranks.
	 * @param M_matrix - M matrix.
	 * @param e_vector - error vector.
	 * @param removed_confs - Newly stripped conflicts.
	 * @param removed_comp - Newly stripped components.
	 ***************************************************/
	private void update_ochiai_ranks(int[][] M_matrix, int[] e_vector, int[] removed_confs, int removed_comp){
Logger.log("St_Strip.update_ochiai_ranks");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.update_ochiai_ranks");
if (_bug_switch)
	return;

		//declare vars
		int comp = -1;
		int conf = -1;
		
		//if ranks are initial, no need to update
		if (ochiai_ranks == null)
			return;
		
		//make sure unstripped arrays are not null
		unstripped_comps_array();
		unstripped_confs_array();
		
		//handle conflicts
		if (removed_confs != null){
			for (int j=0; j < removed_confs.length; j++){
				conf = removed_confs[j];
				
				//scan comps
				for (int i=0; i < unstripped_comps_array.length; i++){
					comp = unstripped_comps_array[i];
					if (comp == removed_comp)
						continue;
					
					if (M_matrix[conf][comp] == 1 && e_vector[conf] == 1)
						ochiai_ranks[comp].reduce_counter(1, 1);
					
					else if (M_matrix[conf][comp] == 0 && e_vector[conf] == 1)
						ochiai_ranks[comp].reduce_counter(0, 1);
					
					else if (M_matrix[conf][comp] == 1 && e_vector[conf] == 0)
						ochiai_ranks[comp].reduce_counter(1, 0);
				}//end for (comps)
			}//end for(removed conflicts)	
		}//end if

		//handle removed comp
		comp = removed_comp;
		for(int i=0; i < unstripped_confs_array.length; i++){
			conf = unstripped_confs_array[i];
			
			if (M_matrix[conf][comp] == 1 && e_vector[conf] == 1)
				ochiai_ranks[comp].reduce_counter(1, 1);
			
			else if (M_matrix[conf][comp] == 0 && e_vector[conf] == 1)
				ochiai_ranks[comp].reduce_counter(0, 1);
			
			else if (M_matrix[conf][comp] == 1 && e_vector[conf] == 0)
				ochiai_ranks[comp].reduce_counter(1, 0);
			
		}//end for
	}
	
	
	/**********************************************
	 * Calculates Ochiai ranks for the components.
	 * @param M_matrix
	 * @param e_vector
	 **********************************************/
	public void calc_ochiai_ranks(int[][] M_matrix, int[] e_vector){
Logger.log("St_Strip.calc_ochiai_ranks");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.calc_ochiai_ranks");
if (_bug_switch)
	return;

		//initialize
		ochiai_ranks = new Ochiai_Rank[M_matrix[0].length];
		for (int i=0; i < M_matrix[0].length; i++)
			ochiai_ranks[i] = new Ochiai_Rank();
		
		//save work
		int[] unstripped_confs = unstripped_confs_array();
		int[] unstripped_comps = unstripped_comps_array();
		int conf,comp;
		
		for(int i=0; i < unstripped_confs.length; i++){
			conf = unstripped_confs[i];
			
			for(int j=0; j < unstripped_comps.length; j++){
				comp = unstripped_comps[j];
				
				if (M_matrix[conf][comp] == 1 && e_vector[conf] == 1)
					ochiai_ranks[comp].advance_counter(1, 1);
				
				else if (M_matrix[conf][comp] == 0 && e_vector[conf] == 1)
					ochiai_ranks[comp].advance_counter(0, 1);
				
				else if (M_matrix[conf][comp] == 1 && e_vector[conf] == 0)
					ochiai_ranks[comp].advance_counter(1, 0);
			}//end for (components)
		}//end for (conflicts)
	}
	
	
	/**************************************************
	 * Calculates the Ochiai rank for given component.
	 * @param M_matrix - M matrix.
	 * @param e_vector - Error vector.
	 * @param comp - Comonent index.
	 * @return - The component's Ochiai rank.
	 **************************************************/
	public double get_ochiai_rank(int[][] M_matrix, int[] e_vector, int comp){
Logger.log("St_Strip.get_ochiai_rank");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.get_ochiai_rank");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		if (ochiai_ranks == null)
			calc_ochiai_ranks(M_matrix, e_vector);
		
		return ochiai_ranks[comp].get_rank();
	}
	
	
	/******************************************
	 * Fully strip of given component.
	 * @param M_matrix - M matrix.
	 * @param e_vector - error vector.
	 * @param comp - component to be stripped.
	 ******************************************/
	public void strip(int[][] M_matrix, int[] e_vector, int comp){
Logger.log("St_Strip.strip");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.strip");
if (_bug_switch)
	return;

		int[] unstripped_confs = unstripped_confs_array();
		Linked_List removed_confs = new Linked_List();
		int conf = -1;
		
		//make sure unstripped arrays are not null
		unstripped_comps_array();
		unstripped_confs_array();
		
		for (int i=0; i < unstripped_confs.length; i++){
			conf = unstripped_confs[i];
			if (M_matrix[conf][comp] == 1 && e_vector[conf] == 1){
				strip_conf(conf);
				removed_confs.add_val(conf);
			}
		}//end for (stripped conflicts)
		
		strip_comp(comp);
		
		//update ochiai counyters
		int[] removed_confs_array = removed_confs.to_int_array();
		update_ochiai_ranks(M_matrix, e_vector, removed_confs_array, comp);
		
		//refreh unstripped cache
		last_unstripped_comps = unstripped_comps_array;
		last_unstripped_confs = unstripped_confs_array;
		unstripped_comps_array = null;
		unstripped_confs_array = null;
	}
	
	
	/*************************************************
	 * Creates an array of all unstripped components.
	 * @return array of all stripped components.
	 *************************************************/
	public int[] unstripped_comps_array(){
Logger.log("St_Strip.unstripped_comps_array");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.unstripped_comps_array");
if (_bug_switch)
	return null;

		Linked_List list = new Linked_List();
		
		//avoid extra job
		if (unstripped_comps_array == null && last_unstripped_comps != null){
			for(int i=0; i < last_unstripped_comps.length; i++)
				if (comps[last_unstripped_comps[i]] != true)
					list.add_val(last_unstripped_comps[i]);
			
			last_unstripped_comps = unstripped_comps_array;
			unstripped_comps_array = list.to_int_array();
		}
		
		//avoid extra job
		else if (unstripped_comps_array == null){
			
			//process
			for(int i=0; i < comps.length; i++){
				if (comps[i] != true)
					list.add_val(i);
			}//end for
					
			unstripped_comps_array = list.to_int_array();
		}//end if
			
		return unstripped_comps_array;
	}
	
	
	/************************************************
	 * Creates an array of all unstripped conflicts.
	 * @return array of all stripped conflicts.
	 ************************************************/
	public int[] unstripped_confs_array(){
Logger.log("St_Strip.unstripped_confs_array");
boolean _bug_switch = Bug_Switcher.has_bug("St_Strip.unstripped_confs_array");
if (_bug_switch)
	return null;

		Linked_List list = new Linked_List();
		
		//avoid extra job
		if (unstripped_confs_array == null && last_unstripped_confs != null){
			for(int i=0; i < last_unstripped_confs.length; i++)
				if (conflicts[last_unstripped_confs[i]] != true)
					list.add_val(last_unstripped_confs[i]);
			
			last_unstripped_confs = unstripped_confs_array;
			unstripped_confs_array = list.to_int_array();
		}
		
		else if (unstripped_confs_array == null){	
			//process
			for(int i=0; i < conflicts.length; i++){
				if (conflicts[i] != true)
					list.add_val(i);
			}//end for
				
			unstripped_confs_array = list.to_int_array();
		}//end if
			
		return unstripped_confs_array;
	}
}
