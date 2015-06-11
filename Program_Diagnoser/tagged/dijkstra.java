package Deprecated;
import Implant.*;


import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Stack;

import Infrastrcture.Linked_List;
import Parsing.Method_Parser;

public class dijkstra {
	private static Hashtable<String, Linked_List> path_cache = new Hashtable<String, Linked_List>();
	
	
	/***********************************************************
	 * Calculates the shortest path to a method within a graph.
	 * @param graph - Process Graph.
	 * @param target - Target method's name or 'method end'.
	 * @return shortest path to a method within a graph.
	 ***********************************************************/
	public static Linked_List find_min_path(Process_Graph graph, String target){
Logger.log("dijkstra.find_min_path");
boolean _bug_switch = Bug_Switcher.has_bug("dijkstra.find_min_path");
if (_bug_switch)
	return null;

		//declare vars
		Linked_List min_path = new Linked_List();
		Process_Node root = graph.get_root();
		Hashtable<Process_Node, int[]> dist = new Hashtable<Process_Node, int[]>(); //distance
		HashSet<Process_Node> visited = new HashSet<Process_Node>(); //visited
		LinkedList<Process_Node> Q = new LinkedList<Process_Node>(); //Q set
		Hashtable<Process_Node, Process_Node> previous = new Hashtable<Process_Node, Process_Node>(); //previous
		
		//buffer vars
		int[] temp_dist = null;
		@SuppressWarnings("unused")
		Process_Node target_node = null;
		String dynamic_target = "" + target; //target can be changed in order to compensate for nested graphs.
		
		//use cache if already calculated
		String key = graph.get_root().get_name() + "->" + target;
		if (path_cache.containsKey(key))
			return path_cache.get(key);
		
		//handle root node
		temp_dist = new int[1];
		temp_dist[0] = 0;
		dist.put(root, temp_dist);
		Q.add(root);
		
		//scan open list
		Process_Node node;
		LinkedList<Process_Node> out_list;
		Iterator<Process_Node> iterator;
		while(! Q.isEmpty()){
			node = find_min_dist(Q, dist, visited);
			
			//break when target has been reached
			if (node.get_name().equals(dynamic_target) || node.get_type().equals(dynamic_target))
				break;
			
			Q.remove(node);
			visited.add(node);
			
			out_list = node.get_out_list();
			iterator = out_list.iterator();
			Process_Node child_node;
			while(iterator.hasNext()){
				child_node = iterator.next();
				
				//calculate distance
				temp_dist = new int[1];
				temp_dist[0] = dist.get(node)[0];
				if (child_node.get_type().equals("method")){
					temp_dist[0]++; //only edges to methods have weight.
					
					//handle graph nesting
					//apply algorithm to sub-graph. If target not found, make target the finish node of the sub-graph.
					if (! child_node.get_name().equals(dynamic_target)){
						Linked_List sub_list = new Linked_List();
						sub_list = find_min_path(Method_Parser.get_graph(child_node.get_name()), target); //seek original target!
						
						if (sub_list.get_length() == 0)
							sub_list = find_min_path(Method_Parser.get_graph(child_node.get_name()), "end method");
						else dynamic_target = "" + child_node.get_name(); //acts as break. target was found in a nested graph.
						
						temp_dist[0] += sub_list.get_length();
						
					}//end if (handle nesting)
				}//end if (handle method node)
					
				
				//update distance as needed
				if (!visited.contains(child_node) && (!dist.contains(child_node) || dist.get(child_node)[0] < temp_dist[0])){
					dist.put(child_node, temp_dist);
					previous.put(child_node, node); 
					Q.add(child_node);
					
					//handle target node pointer
					if (child_node.get_name().equals(dynamic_target) || child_node.get_type().equals(dynamic_target))
						target_node = child_node;
				}
			}//end while (out list)
		}//end while (Q scan)
		
		return min_path;
	}
	
	
	/***********************************************************************
	 * Finds node in Q with minimal distance, that hasn't been visited yet.
	 * @param Q - Open set of nodes.
	 * @param dist - Distance table.
	 * @param visited - Visit table.
	 * @return Unvisited node with minimal distance.
	 ************************************************************************/
	private static Process_Node find_min_dist(LinkedList<Process_Node> Q, Hashtable<Process_Node, int[]> dist, HashSet<Process_Node> visited){
Logger.log("dijkstra.find_min_dist");
boolean _bug_switch = Bug_Switcher.has_bug("dijkstra.find_min_dist");
if (_bug_switch)
	return null;

		//declare vars
		Process_Node result = null;
		Iterator<Process_Node> iterator = Q.iterator();
		Process_Node node;
		int min_dist = -1;
		int distance;
		
		//process
		while (iterator.hasNext()){
			node = iterator.next();
			distance = dist.get(node)[0];
			if (!visited.contains(node) && distance > 0 && distance < min_dist){
				min_dist = distance;
				result = node;
			}//end if
		}//end while
		
		return result;
	}
	
	
	@SuppressWarnings("unused")
	private Linked_List construct_path(Hashtable<Process_Node, Process_Node> previous, Process_Node last_node, String target_name){
Logger.log("dijkstra.construct_path");
boolean _bug_switch = Bug_Switcher.has_bug("dijkstra.construct_path");
if (_bug_switch)
	return null;

		//declare vars
		Linked_List path = new Linked_List();
		Stack<String> stack = new Stack<String>();
		Process_Node node = last_node;
		Hashtable<String, Linked_List> chunks = new Hashtable<String, Linked_List>();
		int indexer = 0;
		
		//if target was never found, return empty list
		if (last_node == null)
			return path;
		
		//process
		while(node != null){
			//not interested in non-method nodes
			if (node.get_type().equals("method")){
				stack.push(Method_Parser.translate_comp(node.get_name())); //translate to index
				
				//handle chunks (result of nested graphs)
				if (! node.get_name().equals(target_name)){
					indexer++;
					String chunk_key = "chunk" + indexer;
					String cache_key = node.get_name() + "->" + target_name;
					chunks.put(chunk_key, path_cache.get(cache_key)); //!!!!!!!!!!!!!
				}
			}

			
			node = previous.get(node);
		}//end while (stack building)
		
		return path;
	}
}
