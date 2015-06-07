package Deprecated;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;

public class Process_Graph {
	private Process_Node root;
	
	
	/***************
	 * Constructor.
	 ***************/
	public Process_Graph(String method_name){
		root = new Process_Node(method_name, "Start method");
	}
	
	
	/*************************
	 * Root getter.
	 * @return graph's root.
	 *************************/
	public Process_Node get_root(){
		return root;
	}
	
	
	/***********************************
	 * Prints the graph in BFS fashion.
	 ***********************************/
	public void print_graph(){
		//ready vars
		Queue<Process_Node> queue = new LinkedList<Process_Node>();
		Process_Node current_node;
		Iterator<Process_Node> iterator;
		
		//insert root to queue and acquire iterator
		queue.add(root);
		
		//traverse tree
		while(queue.isEmpty() == false){
			current_node = queue.remove();
			System.out.println(current_node);
			
			//add children to queue
			iterator = current_node.get_out_list().iterator();
			while(iterator.hasNext() == true){
				current_node = iterator.next();
				queue.add(current_node);
			}//end while
		}//end while
	}
	
	
	/*********************************
	 * Samples a route and prints it.
	 *********************************/
	public void sample_route(){
		//ready vars
		Queue<Process_Node> queue = new LinkedList<Process_Node>();
		Process_Node current_node;
		Iterator<Process_Node> iterator;
		
		//insert root to queue and acquire iterator
		queue.add(root);
		
		//traverse tree
		while(queue.isEmpty() == false){
			current_node = queue.remove();
			System.out.println(current_node);
			
			//add only 1st child to queue
			iterator = current_node.get_out_list().iterator();
			if (iterator.hasNext()){
				current_node = iterator.next();
				queue.add(current_node);
			}
		}//end while
	}
}
