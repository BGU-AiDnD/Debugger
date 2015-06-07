package Diagnoser;

import java.util.Iterator;

public class Confs_Iterator implements Iterator<Integer>{
	private Integer next;
	private int index;
	private boolean[] strip_data;
	
	public Confs_Iterator(boolean[] strip_data){
		index = -1;
		this.strip_data = strip_data;
		next = next();
	}
	
	@Override
	public boolean hasNext() {
		if (next < 0 || next > (strip_data.length - 1))
			return false;
		else return true;
	}

	@Override
	public Integer next() {
		int result = next;
		advance();
		
		return result;
	}
	
	
	private void advance(){
		do{
			index++;
		}while(strip_data[index] == true && index < strip_data.length);
		
		next = index;
	}

	@Override
	public void remove() {
		//unimplemented
	}

}
