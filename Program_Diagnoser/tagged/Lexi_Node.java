package Deprecated;
import Implant.*;

import java.util.Hashtable;


public class Lexi_Node {
	private Hashtable<String, Lexi_Node> branches;
	private Event event;
	private boolean ignore_space;
	
	/*********************************
	 * Constructor.
	 *********************************/
	public Lexi_Node(){
		branches = new Hashtable<String, Lexi_Node>();
		event = null;
		ignore_space = false;
	}
	
	
	/*****************************************************************
	 * Check whether node branches on to given key.
	 * @param key - key.
	 * @return True - if node branches on to key. False - otherwise.
	 *****************************************************************/
	public boolean has_branch(String key){
Logger.log("Lexi_Node.has_branch");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.has_branch");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return branches.containsKey(key);
	}
	
	
	/*****************************************
	 * Private Constructor.
	 * @param brnch - 1st order branching.
	 * @param evnt - event.
	 * @param igspace - space ignorance flag.
	 *****************************************/
	private Lexi_Node(Hashtable<String, Lexi_Node> brnch, Event evnt, boolean igspace){
		branches = brnch;
		event = evnt;
		ignore_space = igspace;
	}
	
	
	/***********************************
	 * Make node ignorant to space key.
	 * Node is made to return itself.
	 ***********************************/
	public void ignore_space(){
Logger.log("Lexi_Node.ignore_space");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.ignore_space");
if (_bug_switch)
	return;

		ignore_space = true;
	}
	
	
	/***************************************
	 * Branch from a given branching point.
	 * @param key - branch key point.
	 **************************************/
	public void branch(String key){
Logger.log("Lexi_Node.branch");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.branch");
if (_bug_switch)
	return;

			Lexi_Node temp_node = new Lexi_Node();
			branches.put(key, temp_node);	
	}
	
	
	/******************************
	 * Branch to an existing node.
	 * @param key - branch key.
	 * @param node - existed node.
	 ******************************/
	public void branch_to_existing(String key, Lexi_Node node){
Logger.log("Lexi_Node.branch_to_existing");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.branch_to_existing");
if (_bug_switch)
	return;

		branches.put(key, node);
	}
	
	
	/*********************************
	 * Next node getter.
	 * @param key - branch point key.
	 * @return next node.
	 *********************************/
	public Lexi_Node get_next(String key){
Logger.log("Lexi_Node.get_next");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.get_next");
if (_bug_switch)
	return null;

		//process
		 //handle space key
		if ((key.equals("space") || key.equals("newline")) && ignore_space == true)
			return new Lexi_Node(branches, null, ignore_space);
		//handle rest
		else return branches.get(key);
	}
	
	
	/**************************
	 * Event setter.
	 * @param ev - event name.
	 **************************/
	public void set_event(Event ev){
Logger.log("Lexi_Node.set_event");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.set_event");
if (_bug_switch)
	return;

		event = ev;
	}
	
	
	/***********************************
	 * Event getter.
	 * @return event held by lexi-node.
	 ***********************************/
	public Event get_event(){
Logger.log("Lexi_Node.get_event");
boolean _bug_switch = Bug_Switcher.has_bug("Lexi_Node.get_event");
if (_bug_switch)
	return null;

		return event;
	}
}
