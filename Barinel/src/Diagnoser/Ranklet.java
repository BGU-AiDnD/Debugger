package Diagnoser;

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
		return comp;
	}
	
	
	/********************
	 * Rank getter.
	 * @return the rank.
	 ********************/
	public double get_rank(){
		return rank;
	}
	
	
	/****************************************
	 * String representation of the ranklet.
	 ****************************************/
	public String toString(){
		String result = ("C:" + comp + "|R:" + rank);
		return result;
	}
	
	
	/******************************************
	 * Compares this ranklet to other ranklet.
	 ******************************************/
	public int compareTo(Ranklet other){
		if (this == other)
			return 0;
		
		else if (this.rank > other.get_rank())
			return 1;
		
		else return -1; //New comer has the honor.
	}
}
