package Infrastrcture;
import Implant.*;


public class OrderAssist {
	
	/************************************************
	 * Ordering an array of integers.
	 * @param i_array - input array of integers.
	 * @return  Ordered array.
	 ************************************************/
	public static int[] quickSort(int[] i_array){
Logger.log("OrderAssist.quickSort");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.quickSort");
if (_bug_switch)
	return null;

		//handle base case
		if (i_array == null || i_array.length <= 1)
			return i_array;
		
		//decide pivot
		int pivot = i_array.length/2; 
		
		//begin sorting
		Linked_List left = new Linked_List();
		Linked_List right = new Linked_List();
		for(int i=0; i < i_array.length; i++){
			if (i_array[i] <= i_array[pivot] && i != pivot)
				left.add_val(i_array[i]);
			else if(i_array[i] > i_array[pivot] && i != pivot)
				right.add_val(i_array[i]);
		}
		
		//recursive action
		if (left.get_length() > 0)
			left = new Linked_List(quickSort(left.to_int_array()));
		if (right.get_length() > 0)
			right = new Linked_List(quickSort(right.to_int_array()));
		
		//compile result
		Linked_List result = new Linked_List();
		Link current_link = left.get_anchor().get_next();
		while(current_link != null){
			result.add_val(current_link.get_val());
			current_link = current_link.get_next();
		}
		
		result.add_val(i_array[pivot]);
		
		current_link = right.get_anchor().get_next();
		while(current_link != null){
			result.add_val(current_link.get_val());
			current_link = current_link.get_next();
		}
		
		return result.to_int_array();
	
	}
	
	
	/************************************************
	 * Ordering an array of doubles.
	 * @param i_array - input array of doubles.
	 * @return  Ordered array.
	 ************************************************/
	public static double[] quickSort(double[] i_array){
Logger.log("OrderAssist.quickSort");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.quickSort");
if (_bug_switch)
	return null;

		//handle base case
		if (i_array == null || i_array.length <= 1)
			return i_array;
		
		//decide pivot
		int pivot = i_array.length/2; 
		
		//begin sorting
		Linked_List left = new Linked_List();
		Linked_List right = new Linked_List();
		for(int i=0; i < i_array.length; i++){
			if (i_array[i] <= i_array[pivot] && i != pivot)
				left.add_val(i_array[i]);
			else if(i_array[i] > i_array[pivot] && i != pivot)
				right.add_val(i_array[i]);
		}
		
		//recursive action
		if (left.get_length() > 0)
			left = new Linked_List(quickSort(left.to_array()));
		if (right.get_length() > 0)
			right = new Linked_List(quickSort(right.to_array()));
		
		//compile result
		Linked_List result = new Linked_List();
		Link current_link = left.get_anchor().get_next();
		while(current_link != null){
			result.add_val(current_link.get_val());
			current_link = current_link.get_next();
		}
		
		result.add_val(i_array[pivot]);
		
		current_link = right.get_anchor().get_next();
		while(current_link != null){
			result.add_val(current_link.get_val());
			current_link = current_link.get_next();
		}
		
		return result.to_array();
	
	}
	
	
	/********************************************************
	 * Searches for a key in an array.
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @return - FALSE - if key not fount, TRUE - otherwise.
	 ********************************************************/
	public static boolean binarySearch(int[] i_array, int key){
Logger.log("OrderAssist.binarySearch");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.binarySearch");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		//initialize vars
		int i_min = 0;
		int i_max = i_array.length - 1;
		
		//begin search
		return (binarySearch(i_array, key, i_min, i_max) >= 0);
	}
	
	
	/********************************************************
	 * Searches for a key in an array.
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @return - FALSE - if key not fount, TRUE - otherwise.
	 ********************************************************/
	public static boolean binarySearch(double[] i_array, double key){
Logger.log("OrderAssist.binarySearch");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.binarySearch");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		//initialize vars
		int i_min = 0;
		int i_max = i_array.length - 1;
		
		//begin search
		return (binarySearch(i_array, key, i_min, i_max) >= 0);
	}
	
	
	/*********************************************************
	 * Searches for a string key in a string array.
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @param i_min - minimum index.
	 * @param i_max - maximum index.
	 * @return - FALSE - if key not found, TRUE - otherwise.
	 *********************************************************/
	public static int binarySearch(int[] i_array, int key, int i_min, int i_max){
Logger.log("OrderAssist.binarySearch");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.binarySearch");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//handle "not found" case
		if (i_max < i_min)
			return -1;
		
		//calculate middle 
		int i_mid = (i_max + i_min)/2;
		
		//begin search
		if (i_array[i_mid] > key)
			//key in lower subset
			return binarySearch(i_array, key, i_min, i_mid-1);
		
		else if (i_array[i_mid] < key)
			//key is in upper subset
			return binarySearch(i_array, key, i_mid+1, i_max);
		
		else return i_mid;
		
	}
	
	
	/*********************************************************
	 * Searches for a string key in a string array.
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @param i_min - minimum index.
	 * @param i_max - maximum index.
	 * @return - FALSE - if key not found, TRUE - otherwise.
	 *********************************************************/
	public static int binarySearch(double[] i_array, double key, int i_min, int i_max){
Logger.log("OrderAssist.binarySearch");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.binarySearch");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//handle "not found" case
		if (i_max < i_min)
			return -1;
		
		//calculate middle 
		int i_mid = (i_max + i_min)/2;
		
		//begin search
		if (i_array[i_mid] > key)
			//key in lower subset
			return binarySearch(i_array, key, i_min, i_mid-1);
		
		else if (i_array[i_mid] < key)
			//key is in upper subset
			return binarySearch(i_array, key, i_mid+1, i_max);
		
		else return i_mid;
		
	}
	
	
	/**************************************************
	 * Finds a key in an array (Binary Search).
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @return the index of the key (-1 if not found).
	 ***************************************************/
	public static int findKey(int[] i_array, int key){
Logger.log("OrderAssist.findKey");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.findKey");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize vars
		int i_min = 0;
		int i_max = i_array.length - 1;
		
		//begin search
		return binarySearch(i_array, key, i_min, i_max);
	}
	
	
	/**************************************************
	 * Finds a key in an array (Binary Search).
	 * @param i_array - input array of strings.
	 * @param key - key string to be found.
	 * @return the index of the key (-1 if not found).
	 ***************************************************/
	public static int findKey(double[] i_array, double key){
Logger.log("OrderAssist.findKey");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.findKey");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		//initialize vars
		int i_min = 0;
		int i_max = i_array.length - 1;
		
		//begin search
		return binarySearch(i_array, key, i_min, i_max);
	}
	
	
	/*********************************************************************************
	 * *********************************** Debug *************************************
	 *********************************************************************************/
	public static void main(String[] args){
Logger.log("OrderAssist.main");
boolean _bug_switch = Bug_Switcher.has_bug("OrderAssist.main");
if (_bug_switch)
	return;


	}

}
