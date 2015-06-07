package Deprecated;

import java.util.LinkedList;

public class Process_Node {
	private String name; //component name
	private String type;
	private LinkedList<Process_Node> in_list;
	private LinkedList<Process_Node> out_list;
	private boolean is_recursive;
	
	
	/********************************
	 * Constructor.
	 * @param na - component's name.
	 * @param ty - component's type.
	 ********************************/
	public Process_Node(String na, String ty){
		name = na;
		type = ty;
		in_list = new LinkedList<Process_Node>();
		out_list = new LinkedList<Process_Node>();
	}
	
	
	/****************************
	 * Name getter.
	 * @return component's name.
	 ****************************/
	public String get_name(){
		return name;
	}
	
	
	/****************************
	 * Type getter.
	 * @return component's type.
	 ****************************/
	public String get_type(){
		return type;
	}
	
	
	/************************************************
	 * Adds a component to incoming components list.
	 * @param name - name of component to be added.
	 ************************************************/
	public void add_in(Process_Node node){
		in_list.add(node);
	}
	
	
	/************************************************
	 * Adds a component to outgoing components list.
	 * @param name - name of component to be added.
	 ************************************************/
	public void add_out(Process_Node node){
		out_list.add(node);
	}
	
	
	/**************************
	 * Out nodes list getter.
	 * @return out nodes list.
	 **************************/
	public LinkedList<Process_Node> get_out_list(){
		return out_list;
	}
	
	
	/*********************************
	 * Turns on recursive indication.
	 *********************************/
	public void turn_on_rec_ind(){
		is_recursive = true;
	}
	
	
	/**************************************************
	 * Checks if node is recursive.
	 * @return True - if recursive. False - otherwise.
	 **************************************************/
	public boolean is_recursive(){
		return is_recursive;
	}
	
	
	/*************************************
	 * String representation of the node.
	 *************************************/
	public String toString(){
		return(name + ", type: " + type);
	}
}
