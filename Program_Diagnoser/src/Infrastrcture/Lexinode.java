package Infrastrcture;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Lexinode {
	private Set<Integer> payload;
	private Map<Integer, Lexinode> branches;
	private Integer own_value;
	
	
	/***********************************
	 * Constructor.
	 * @param own_value - node's value.
	 ***********************************/
	public Lexinode(int own_value){
		this.own_value = own_value;
		payload = new HashSet<Integer>();
		branches = new HashMap<Integer, Lexinode>();
	}
	
	
	/**************************************
	 * Own value getter.
	 * @return the value of this lexinode.
	 **************************************/
	public int get_val(){
		return own_value;
	}
	
	
	/***************************************************
	 * Adds a payload to this node.
	 * @param payload - Integer to be added to payload.
	 ***************************************************/
	public void add_to_payload(int payload){
		this.payload.add(payload);
	}
	
	
	/************************************
	 * Payload getter.
	 * @return the payload of this node.
	 ************************************/
	public Set<Integer> get_payload(){
		return payload;
	}
	
	
	/************************************************************************
	 * Gets all the subsequent payloads, including the payload of this node.
	 * @return all the subsequent payloads.
	 ************************************************************************/
	public Set<Integer> get_all_payloads(){
		//get ready
		HashSet<Integer> result = new HashSet<Integer>();
		
		//add own payload to the list
		for(int pl : payload)
			result.add(pl);
		
		//add all subsequent payloads to the list
		for(Lexinode node : branches.values())
			result.addAll(node.get_all_payloads());
		
		//wrap
		return result;
	}
	
	
	/*****************************************
	 * Branches getter.
	 * @return all the branches of this node.
	 *****************************************/
	public Map<Integer, Lexinode> get_benches(){
		return branches;
	}
	
	
	/*****************************************************************************
	 * Checks whether this node branches to a certain value.
	 * @param val - The value to be checked.
	 * @return True - if the node branches to the given value. False - otherwise.
	 *****************************************************************************/
	public boolean has_branch_to(int val){
		return branches.containsKey(val);
	}
	
	
	/*************************************************************************
	 * Returns the node with the specified vlue that branches from this node.
	 * If no such node exists, null will be returned.
	 * @param val - The value of the desired node.
	 * @return  the node with the specified vlue.
	 **************************************************************************/
	public Lexinode get_branch(int val){
		return branches.get(val);
	}
	
	
	/****************************************************
	 * Branches this node to a certain value.
	 * Existing node with same value will be overidden!
	 * @param val - Value of the node to be branched to.
	 * @return the newly created node.
	 ****************************************************/
	public Lexinode branch_to(int val){
		Lexinode new_node = new Lexinode(val);
		branches.put(val, new_node);
	
		return new_node;
	}
}
