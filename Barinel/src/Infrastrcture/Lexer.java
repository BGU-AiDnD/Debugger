package Infrastrcture;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Lexer {
	private Map<Integer, Lexinode> top_nodes;
	private Map<Integer, HashSet<Lexinode>> nodes_by_val;
	
	//cache related
	private Map<Integer, HashSet<Integer>> cache;
	private HashSet<Integer> last_set;
	private int last_set_key;
	
	//constants
	private final int cache_size = 4000;
	
	/***************
	 * Constructor.
	 ***************/
	public Lexer(){
		top_nodes = new HashMap<Integer, Lexinode>();
		nodes_by_val = new HashMap<Integer, HashSet<Lexinode>>();
		cache = new HashMap<Integer, HashSet<Integer>>();
		
	}
	
	
	/***************************************
	 * Adds a value with the specified key.
	 * @param key - a sorted(!) key.
	 * @param val - Value.
	 ***************************************/
	public void add(int[] key, int val){
		//declare vars
		Lexinode current_node;
		
		//handle base case
		current_node = top_nodes.get(key[0]);
		if (current_node == null){
			current_node = new Lexinode(key[0]);
			top_nodes.put(key[0], current_node);
			add_to_nodes_by_val(current_node, key[0]);
		}
		
		//scan rest of the key
		for(int i=1; i < key.length; i++){
			if (current_node.has_branch_to(key[i]))
				current_node.get_branch(key[i]);
			else {
				current_node = current_node.branch_to(key[i]);
				add_to_nodes_by_val(current_node, key[i]);
			}
		}//end for
		
		//wrap
		current_node.add_to_payload(val);
	}
	
	
	/***********************************************
	 * Adds a node to the 'nodes-by-value' tracker.
	 * @param node - Lexinode.
	 * @param val - Value of the node.
	 ***********************************************/
	private void add_to_nodes_by_val(Lexinode node, int val){
		HashSet<Lexinode> nodes_set = nodes_by_val.get(val);
		
		if (nodes_set == null){
			nodes_set = new HashSet<Lexinode>();
			nodes_by_val.put(val, nodes_set);
		}
		
		nodes_set.add(node);
	}
	
	
	/*****************************************************************
	 * Gets all the payloads that contain the specified key fragment.
	 * @param key_frag - Key fragment.
	 * @return all the payloads that contain the key fragment.
	 *****************************************************************/
	public Set<Integer> get_all_that_contain(int key_frag){
		//get ready
		HashSet<Integer> result =  new HashSet<Integer>();
		HashSet<Lexinode> nodes_set = nodes_by_val.get(key_frag);
		
		//there can be cases where there are no such tests in the pool 
		//(component only appear in the initial tests)
		if (nodes_set == null)
			return result;
		
		//handle cache
		if (cache.containsKey(key_frag))
			return cache.get(key_frag);
			
		//process
		for(Lexinode node : nodes_set)
			result.addAll(node.get_all_payloads());
		
		last_set = result;
		last_set_key = key_frag;
		
		//handle cache too big
		if (cache.size() < cache_size)	
			cache.put(key_frag, result);	

		return result;
	}
	
	
	/**************************************
	 * Clears the cache.
	 * Doesn't clear the last entered set!
	 **************************************/
	public void clear_cache(){
		cache.clear();
		cache.put(last_set_key, last_set);
	}
}
