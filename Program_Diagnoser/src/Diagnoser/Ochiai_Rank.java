package Diagnoser;

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
		counters[i][j]++;
		
		//refresh cache
		rank = -1;
	}
}
