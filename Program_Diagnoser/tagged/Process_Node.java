package Deprecated;
import Implant.*;


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
Logger.log("Process_Node.get_name");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.get_name");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return name;
	}
	
	
	/****************************
	 * Type getter.
	 * @return component's type.
	 ****************************/
	public String get_type(){
Logger.log("Process_Node.get_type");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.get_type");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return type;
	}
	
	
	/************************************************
	 * Adds a component to incoming components list.
	 * @param name - name of component to be added.
	 ************************************************/
	public void add_in(Process_Node node){
Logger.log("Process_Node.add_in");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.add_in");
if (_bug_switch)
	return;

		in_list.add(node);
	}
	
	
	/************************************************
	 * Adds a component to outgoing components list.
	 * @param name - name of component to be added.
	 ************************************************/
	public void add_out(Process_Node node){
Logger.log("Process_Node.add_out");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.add_out");
if (_bug_switch)
	return;

		out_list.add(node);
	}
	
	
	/**************************
	 * Out nodes list getter.
	 * @return out nodes list.
	 **************************/
	public LinkedList<Process_Node> get_out_list(){
Logger.log("Process_Node.get_out_list");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.get_out_list");
if (_bug_switch)
	return null;

		return out_list;
	}
	
	
	/*********************************
	 * Turns on recursive indication.
	 *********************************/
	public void turn_on_rec_ind(){
Logger.log("Process_Node.turn_on_rec_ind");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.turn_on_rec_ind");
if (_bug_switch)
	return;

		is_recursive = true;
	}
	
	
	/**************************************************
	 * Checks if node is recursive.
	 * @return True - if recursive. False - otherwise.
	 **************************************************/
	public boolean is_recursive(){
Logger.log("Process_Node.is_recursive");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.is_recursive");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return is_recursive;
	}
	
	
	/*************************************
	 * String representation of the node.
	 *************************************/
	public String toString(){
Logger.log("Process_Node.toString");
boolean _bug_switch = Bug_Switcher.has_bug("Process_Node.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return(name + ", type: " + type);
	}
}
