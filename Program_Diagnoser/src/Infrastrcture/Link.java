package Infrastrcture;

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
		p_prev = new_prev;
	}
	
	
	/**************************************************
	 * Updates pointer to next link.
	 * @param new_next - new pointer for next link.
	 **************************************************/
	public void set_next(Link new_next){
		p_next = new_next;
	}
	
	/*************************
	 * Updates value of link
	 * @param val - new value
	 *************************/
	public void set_val(double val){
		value = val;
	}
	
	
	/**********************************
	 * Updates secondary value of link
	 * @param sec - secondary value
	 **********************************/
	public void set_secondary(double sec){
		secondary = sec;
	}
	
	
	/************************************************
	 * Parameters setter.
	 * @param parameters - parameters (coordinates).
	 ************************************************/
	public void set_params(double[] parameters){
		params = parameters;
	}
	
	
	/**********************************
	 * Returns particle's parameters.
	 * @return particle's parameters.
	 **********************************/
	public double[] get_params(){
		return params;
	}
	
	
	/*************************************
	 * Returns pointer to previous link.
	 * @return - pointer to previous link
	 *************************************/
	public Link get_prev(){
		return p_prev;
	}
	
	
	/*********************************
	 * Returns pointer to next link.
	 * @return - pointer to next link
	 *********************************/
	public Link get_next(){
		return p_next;
	}
	
	
	/****************************
	 * Returns value held by link.
	 * @return - value of link.
	 ****************************/
	public double get_val(){
		return value;
	}
	
	
	/**************************************
	 * Return secondary value held by link.
	 * @return - secondary value of link.
	 **************************************/
	public double get_sec(){
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
