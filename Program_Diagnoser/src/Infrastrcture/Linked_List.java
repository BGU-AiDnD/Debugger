package Infrastrcture;

public class Linked_List {
	private Link anchor;
	private Link p_last;
	private int length;
	
	
	/**************
	 * Constructor
	 **************/
	public Linked_List(){
		anchor = new Link();
		p_last = anchor;
		length = 0;
	}
	
	
	/****************************************************
	 * Special Constructor.
	 * @param array - list is created out of this array.
	 ****************************************************/
	public Linked_List(int[] array){
		anchor = new Link();
		p_last = anchor;
		length = 0;
		
		for(int i=0; i<array.length; i++)
			add_val(array[i]);
	}
	
	
	/****************************************************
	 * Special Constructor.
	 * @param array - list is created out of this array.
	 ****************************************************/
	public Linked_List(double[] array){
		anchor = new Link();
		p_last = anchor;
		length = 0;
		
		for(int i=0; i<array.length; i++)
			add_val(array[i]);
	}
	
	
	/***************************************************
	 * Adds new link to list that will hold given value.
	 * @param val - new number to be inserted into list.
	 ***************************************************/
	public void add_val(double val){
		Link new_link = new Link(val,p_last,null);
		
		//update last link
		p_last.set_next(new_link); 
		p_last = new_link;
		
		length++;
	}
	
	
	/***************************************************
	 * Adds new link to list that will hold given value.
	 * @param val - new number to be inserted into list.
	 ***************************************************/
	public void add_val(double val, double sec){
		Link new_link = new Link(val,p_last,null);
		new_link.set_secondary(sec);
		
		//update last link
		p_last.set_next(new_link); 
		p_last = new_link;
		
		length++;
	}
	
	
	/****************************************************
	 * Inserts new number by order.
	 * @param val - new number to be inserted into list.
	 * @param sec - secondary number of new link.
	 ****************************************************/
	public void add_by_order(double val, double sec){
		Link new_link = new Link(val,null,null);
		new_link.set_secondary(sec);
		
		add_by_order(new_link);
	}
	
	
	/****************************************************
	 * Inserts new number by order.
	 * @param val - new number to be inserted into list.
	 ****************************************************/
	public void add_by_order(double val){
		Link new_link = new Link(val,null,null);
		
		add_by_order(new_link);
	}
	
	/****************************************************
	 * Inserts new number by order.
	 * @param val - new number to be inserted into list.
	 ****************************************************/
	public void add_by_order(Link new_link){
		double val = new_link.get_val();
		Link current_link = anchor;
		
		//find where to put new val
		while(current_link.get_next() != null && current_link.get_next().get_val() < val)
			current_link = current_link.get_next();
		
		//update connections
		if(current_link == anchor){ //handle anchor
			new_link.set_next(anchor.get_next());
			new_link.set_prev(anchor);
			if(anchor.get_next() == null) //handle empty list
				p_last = new_link;
			else anchor.get_next().set_prev(new_link);
			anchor.set_next(new_link);
		}
		else if(current_link == p_last){ //handle last link
			p_last.set_next(new_link);
			new_link.set_prev(p_last);
			p_last = new_link;
		}
		else{
			//handle right side connections
			new_link.set_next(current_link.get_next());
			current_link.get_next().set_prev(new_link);
			
			//handle left side connections
			new_link.set_prev(current_link);
			current_link.set_next(new_link);
		}
		
		length++;
	}
	
	
	/*****************************************
	 * Removes the ith link from list.
	 * @param index - ith link to be removed.
	 *****************************************/
	public void delete_link(int index){
		Link current_link = anchor;
		Link prev,next = null;
		
		//go to the ith link
		for(int i=1; i<=index; i++){
			current_link = current_link.get_next();
		}
		
		//adjust previous and next links
		prev = current_link.get_prev();
		next = current_link.get_next();
		prev.set_next(next);
		
		//handle last link
		if (next == null)
			p_last = prev;
		else next.set_prev(prev);
		
		length--; 
	}
	
	
	/*************************************************
	 * Returns the value of the ith link.
	 * @param index - index of link to get its value.
	 * @return - the value of the ith link.
	 *************************************************/
	public double get_val(int index){
		Link current_link = anchor;
		
		//go to the ith link
		for(int i=1; i<=index; i++){
			current_link = current_link.get_next();
		}
		
		return current_link.get_val();
	}
	
	
	/***********************************************************
	 * Returns the secondary value of the ith link.
	 * @param index - index of link to get its secondary value.
	 * @return - the secondary value of the ith link.
	 ***********************************************************/
	public double get_sec(int index){
		Link current_link = anchor;
		
		//go to the ith link
		for(int i=1; i<=index; i++){
			current_link = current_link.get_next();
		}
		
		return current_link.get_sec();
	}
	
	
	/********************************
	 * Returns maximum value in list.
	 * @return maximum value in list.
	 ********************************/
	public double find_max_val(){
		//ready vars
		double max = anchor.get_val();
		Link current_link = anchor.get_next();
		
		//begin search
		while(current_link != null){
			if(current_link.get_val() > max)
				max = current_link.get_val();
			current_link = current_link.get_next();
		}
		
		return max;
	}
	
	
	/******************************************
	 * Returns maximum secondary value in list.
	 * @return maximum secondary value in list.
	 ******************************************/
	public double find_max_sec(){
		//ready vars
		double max = anchor.get_sec();
		Link current_link = anchor.get_next();
		
		//begin search
		while(current_link != null){
			if(current_link.get_sec() > max)
				max = current_link.get_sec();
			current_link = current_link.get_next();
		}
		
		return max;
	}
	
	
	/************************************************
	 * Converts the list into an array.
	 * @return Double[] array representing the list.
	 ************************************************/
	public double[] to_array(){
		double[] result = null;
		if (length == 0)
			return result;
		
		else{
			result = new double[length];
			int i = 0;
			Link current_link = anchor.get_next();
			while(current_link != null){
				result[i] = current_link.get_val();
				current_link = current_link.get_next();
				i++;
			}//end while
			
			return result;
		}//end if
	}
	
	
	/************************************************
	 * Converts the list into an int[] array.
	 * @return Double[] array representing the list.
	 ************************************************/
	public int[] to_int_array(){
		//declare vars
		double[] temp = this.to_array();
		int[] result = null;
		
		//start process
		if (temp != null){
			result = new int[temp.length];
			for(int i=0; i<temp.length; i++)
				result[i] = (int) temp[i];	
		}
		
		return result;
	}
	
	
	/**********************************************************
	 * Returns new list with swapped values, in original order.
	 * @return new list with swapped values, in original order.
	 **********************************************************/
	public Linked_List invert_vals(){
		//ready vars
		Linked_List new_list = new Linked_List();
		Link current_link = anchor.get_next();
		double val, sec;
		
		//swap the vals
		while(current_link != null){
			val = current_link.get_val();
			sec = current_link.get_sec();
			new_list.add_val(sec, val);
			current_link = current_link.get_next();
		}
		
		return new_list;
		
	}
	
	
	/********************************************************
	 * Checks whether list contains given value.
	 * @param val - value to be searched.
	 * @return True - if value was found. False - otherwise.
	 ********************************************************/
	public boolean contains(double val){
		//declare vars
		boolean result = false;
		
		//handle base case
		if (length == 0)
			result = false;
		
		else{
			Link current_link = anchor.get_next();
			while(result == false && current_link != null){
				if (current_link.get_val() == val)
					result = true;
				current_link = current_link.get_next();
			}//end while
		}
		return result;
	}
	
	
	/***************************
	 * Gets length of list.
	 * @return - length of list.
	 ***************************/
	public int get_length(){
		return length;
	}
	
	
	/****************************
	 * Returns pointer to anchor
	 * @return pointer to anchor
	 ****************************/
	public Link get_anchor(){
		return anchor;
	}
	
	
	/*******************************
	 * Returns pointer to last link.
	 * @return pointer to last link.
	 *******************************/
	public Link get_p_last(){
		return p_last;
	}
	
	
	/*********************
	 * Sets length
	 * @param l - length.
	 *********************/
	public void set_length(int l){
		length = l;
	}
	

	/*************************************
	 * String representation of the list.
	 *************************************/
	public String toString(){
		String string = "";
		Link current_link = anchor.get_next();
		for(int i=1; i <= length; i++){
			string += ("-->" + (int)current_link.get_val());
			current_link = current_link.get_next();
		}
		return string;
	}
	
	
	/***************************************************************
	 * String representation of the list, including secondary value.
	 ***************************************************************/
	public String full_string(){
		//ready vars
		String string = "";
		Link current_link = anchor.get_next();
		double val, sec;
		
		//concatenate
		for(int i=1; i<=length; i++){
			val = current_link.get_val();
			sec = current_link.get_sec();
			string += ("-->" + (int)val + "(" + (int)sec + ") ");
			current_link = current_link.get_next();
		}
		return string;
	}
	
	
	/*******************
	 * Clones the list.
	 *******************/
	public Linked_List clone(){
		//declare vars
		Linked_List new_list = new Linked_List();
		Link current_link = anchor.get_next();
		
		//start process
		while(current_link != null){
			new_list.add_val(current_link.get_val(), current_link.get_sec());
			current_link = current_link.get_next();
		}
		
		return new_list;
		
	}
}
