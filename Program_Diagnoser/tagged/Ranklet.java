package Diagnoser;
import Implant.*;


public class Ranklet implements Comparable<Ranklet>{
	private int comp;
	private double rank;
	
	/*********************************
	 * Constructor.
	 * @param comp - Component index.
	 * @param rank - Rank.
	 *********************************/
	public Ranklet(int comp, double rank){
		this.comp = comp;
		this.rank = rank;
	}
	
	
	/*************************
	 * Component getter.
	 * @return the component.
	 *************************/
	public int get_comp(){
Logger.log("Ranklet.get_comp");
boolean _bug_switch = Bug_Switcher.has_bug("Ranklet.get_comp");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return comp;
	}
	
	
	/********************
	 * Rank getter.
	 * @return the rank.
	 ********************/
	public double get_rank(){
Logger.log("Ranklet.get_rank");
boolean _bug_switch = Bug_Switcher.has_bug("Ranklet.get_rank");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return rank;
	}
	
	
	/****************************************
	 * String representation of the ranklet.
	 ****************************************/
	public String toString(){
Logger.log("Ranklet.toString");
boolean _bug_switch = Bug_Switcher.has_bug("Ranklet.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		String result = ("C:" + comp + "|R:" + rank);
		return result;
	}
	
	
	/******************************************
	 * Compares this ranklet to other ranklet.
	 ******************************************/
	public int compareTo(Ranklet other){
Logger.log("Ranklet.compareTo");
boolean _bug_switch = Bug_Switcher.has_bug("Ranklet.compareTo");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		if (this == other)
			return 0;
		
		else if (this.rank > other.get_rank())
			return 1;
		
		else return -1; //New comer has the honor.
	}
}
