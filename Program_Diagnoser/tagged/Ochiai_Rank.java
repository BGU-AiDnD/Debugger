package Diagnoser;
import Implant.*;


public class Ochiai_Rank {
	protected int[][] counters;
	private double rank;
	
	/***************
	 * Constructor.
	 ***************/
	public Ochiai_Rank(){
		counters = new int[2][2];
		
		counters[1][1] = 0;
		counters[1][0] = 0;
		counters[0][1] = 0;
		counters[0][0] = -1;
		
		rank = -1;
	}
	
	
	/*******************
	 * Clones the rank.
	 *******************/
	public Ochiai_Rank clone(){
Logger.log("Ochiai_Rank.clone");
boolean _bug_switch = Bug_Switcher.has_bug("Ochiai_Rank.clone");
if (_bug_switch)
	return null;

		Ochiai_Rank clone = new Ochiai_Rank();
		clone.counters[1][1] = this.counters[1][1];
		clone.counters[0][1] = this.counters[0][1];
		clone.counters[1][0] = this.counters[1][0];
		
		return clone;
	}
	
	
	/***************************
	 * Rank getter.
	 * @return The Ochiai rank.
	 ***************************/
	public double get_rank(){
Logger.log("Ochiai_Rank.get_rank");
boolean _bug_switch = Bug_Switcher.has_bug("Ochiai_Rank.get_rank");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//save work
		if (rank < 0){
			int n11 = counters[1][1];
			int n10 = counters[1][0];
			int n01 = counters[0][1];
			
			if ((n11 + n01) * (n11 + n10) != 0)
				rank = n11 / Math.sqrt((n11 + n01) * (n11 + n10));
			
			else rank = 0;
		}
		
		return rank;
	}
	
	
	/****************************************
	 * Reduces the specified counter.
	 * @param i - Components existance flag.
	 * @param j - Error existance flag.
	 ****************************************/
	public void reduce_counter(int i, int j){
Logger.log("Ochiai_Rank.reduce_counter");
boolean _bug_switch = Bug_Switcher.has_bug("Ochiai_Rank.reduce_counter");
if (_bug_switch)
	return;

		counters[i][j]--;
		
		//refresh cache
		rank = -1;
	}
	
	
	/****************************************
	 * Advances the specified counter.
	 * @param i - Components existance flag.
	 * @param j - Error existance flag.
	 ****************************************/
	public void advance_counter(int i, int j){
Logger.log("Ochiai_Rank.advance_counter");
boolean _bug_switch = Bug_Switcher.has_bug("Ochiai_Rank.advance_counter");
if (_bug_switch)
	return;

		counters[i][j]++;
		
		//refresh cache
		rank = -1;
	}
}
