package Diagnoser;
import Implant.*;


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
Logger.log("Confs_Iterator.hasNext");
boolean _bug_switch = Bug_Switcher.has_bug("Confs_Iterator.hasNext");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		if (next < 0 || next > (strip_data.length - 1))
			return false;
		else return true;
	}

	@Override
	public Integer next() {
Logger.log("Confs_Iterator.next");
boolean _bug_switch = Bug_Switcher.has_bug("Confs_Iterator.next");
Integer _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		int result = next;
		advance();
		
		return result;
	}
	
	
	private void advance(){
Logger.log("Confs_Iterator.advance");
boolean _bug_switch = Bug_Switcher.has_bug("Confs_Iterator.advance");
if (_bug_switch)
	return;

		do{
			index++;
		}while(strip_data[index] == true && index < strip_data.length);
		
		next = index;
	}

	@Override
	public void remove() {
Logger.log("Confs_Iterator.remove");
boolean _bug_switch = Bug_Switcher.has_bug("Confs_Iterator.remove");
if (_bug_switch)
	return;

		//unimplemented
	}

}
