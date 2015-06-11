package Infrastrcture;
import Implant.*;


public class Link {
	private Link p_prev; //pointer to next link
	private Link p_next; //pointer to previous link
	private double value;
	private double secondary;
	private double[] params;
	
	
	/***************************************************
	 * Updates pointer to previous link.
	 * @param new_prev - new pointer for previous link.
	 ****************************************************/
	public void set_prev(Link new_prev){
Logger.log("Link.set_prev");
boolean _bug_switch = Bug_Switcher.has_bug("Link.set_prev");
if (_bug_switch)
	return;

		p_prev = new_prev;
	}
	
	
	/**************************************************
	 * Updates pointer to next link.
	 * @param new_next - new pointer for next link.
	 **************************************************/
	public void set_next(Link new_next){
Logger.log("Link.set_next");
boolean _bug_switch = Bug_Switcher.has_bug("Link.set_next");
if (_bug_switch)
	return;

		p_next = new_next;
	}
	
	/*************************
	 * Updates value of link
	 * @param val - new value
	 *************************/
	public void set_val(double val){
Logger.log("Link.set_val");
boolean _bug_switch = Bug_Switcher.has_bug("Link.set_val");
if (_bug_switch)
	return;

		value = val;
	}
	
	
	/**********************************
	 * Updates secondary value of link
	 * @param sec - secondary value
	 **********************************/
	public void set_secondary(double sec){
Logger.log("Link.set_secondary");
boolean _bug_switch = Bug_Switcher.has_bug("Link.set_secondary");
if (_bug_switch)
	return;

		secondary = sec;
	}
	
	
	/************************************************
	 * Parameters setter.
	 * @param parameters - parameters (coordinates).
	 ************************************************/
	public void set_params(double[] parameters){
Logger.log("Link.set_params");
boolean _bug_switch = Bug_Switcher.has_bug("Link.set_params");
if (_bug_switch)
	return;

		params = parameters;
	}
	
	
	/**********************************
	 * Returns particle's parameters.
	 * @return particle's parameters.
	 **********************************/
	public double[] get_params(){
Logger.log("Link.get_params");
boolean _bug_switch = Bug_Switcher.has_bug("Link.get_params");
if (_bug_switch)
	return null;

		return params;
	}
	
	
	/*************************************
	 * Returns pointer to previous link.
	 * @return - pointer to previous link
	 *************************************/
	public Link get_prev(){
Logger.log("Link.get_prev");
boolean _bug_switch = Bug_Switcher.has_bug("Link.get_prev");
if (_bug_switch)
	return null;

		return p_prev;
	}
	
	
	/*********************************
	 * Returns pointer to next link.
	 * @return - pointer to next link
	 *********************************/
	public Link get_next(){
Logger.log("Link.get_next");
boolean _bug_switch = Bug_Switcher.has_bug("Link.get_next");
if (_bug_switch)
	return null;

		return p_next;
	}
	
	
	/****************************
	 * Returns value held by link.
	 * @return - value of link.
	 ****************************/
	public double get_val(){
Logger.log("Link.get_val");
boolean _bug_switch = Bug_Switcher.has_bug("Link.get_val");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return value;
	}
	
	
	/**************************************
	 * Return secondary value held by link.
	 * @return - secondary value of link.
	 **************************************/
	public double get_sec(){
Logger.log("Link.get_sec");
boolean _bug_switch = Bug_Switcher.has_bug("Link.get_sec");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return secondary;
	}
	
	
	/****************
	 * Constructor.
	 ****************/
	public Link(){
		p_prev = null;
		p_next = null;
		value = 0;
		secondary = 0;
		params = null;
	}
	
	
	/******************************************
	 * Constructor.
	 * @param val - value that link will hold.
	 * @param prev - pointer to previous link.
	 * @param next - pointer to next link.
	 ******************************************/
	public Link(double val, Link prev, Link next){
		p_prev = prev;
		p_next = next;
		value = val;
		secondary = 0;
		params = null;
	}
}
