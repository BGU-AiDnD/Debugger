package Deprecated;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;

public class Event_Handler {
	private static Process_Node current_node, root_node;
	private static Queue<Event> active_events = new LinkedList<Event>();
	private static Queue<Event> new_events = new LinkedList<Event>();
	private static Stack<Process_Node> up_stack = new Stack<Process_Node>();
	private static Stack<Process_Node> down_stack = new Stack<Process_Node>();
	
	
	/*****************************************************
	 * Loading the handler with a graph seed (only root).
	 * Also resets the handler!!
	 * @param graph - new graph object.
	 *****************************************************/
	public static void load_graph_seed(Process_Graph graph){
		root_node = graph.get_root();
		current_node = root_node;
		active_events = new LinkedList<Event>();
		new_events = new LinkedList<Event>();
		up_stack = new Stack<Process_Node>();
		down_stack = new Stack<Process_Node>();
	}
	
	
	/************************************************
	 * Current node setter.
	 * @param node - node to be called current node.
	 ************************************************/
	public static void update_current_node(Process_Node node){
		current_node = node;
	}
	
	
	/************************
	 * current node getter.
	 * @return current node.
	 ************************/
	public static Process_Node get_current(){
		return current_node;
	}
	
	
	/********************************************
	 * Seals the graph by inserting ending node.
	 ********************************************/
	public static void seal_graph(String method_name){
		Process_Node end_node = new Process_Node(method_name, "end method");
		link_to_current(end_node);
		update_current_node(end_node);
	}
	
	
	/*************************************************
	 * Pushes a node to "up stack".
	 * @param node - node to be pushed to "up stack".
	 *************************************************/
	public static void push_to_up_stack(Process_Node node){
		up_stack.push(node);
	}
	
	
	/***************************************************
	 * Pushes a node to "down stack".
	 * @param node - node to be pushed to "down stack".
	 ***************************************************/
	public static void push_to_down_stack(Process_Node node){
		down_stack.push(node);
	}
	
	
	/*********************************************
	 * Returns pointer to top node in "up stack".
	 * @return pointer to top node in "up stack".
	 *********************************************/
	public static Process_Node peek_up_stack(){
		return up_stack.peek();
	}
	
	
	/***********************************************
	 * Returns pointer to top node in "down stack".
	 * @return pointer to top node in "down stack".
	 ***********************************************/
	public static Process_Node peek_down_stack(){
		return down_stack.peek();
	}
	
	
	/***************************************************
	 * Links a given node to current node.
	 * @param node - node to be linked to current node.
	 ***************************************************/
	public static void link_to_current(Process_Node node){
		current_node.add_out(node);
		node.add_in(current_node);
	}
	
	
	/*********************************************************
	 * Links a given node to node in top of "up stack".
	 * @param node - node to be linked to node in "up stack".
	 *********************************************************/
	public static void backward_link_up(Process_Node node){
		Process_Node junction = up_stack.peek();
		junction.add_out(node);
		node.add_in(junction);
	}
	
	
	/***********************************************************
	 * Links a given node to node in top of "down stack".
	 * @param node - node to be linked to node in "down stack".
	 ***********************************************************/
	public static void forward_link_down(Process_Node node){
		Process_Node drain = down_stack.peek();
		node.add_out(drain);
		drain.add_in(node);
	}
	
	
	/******************************
	 * Links node1 down to node2.
	 * @param node1 - (up)node.
	 * @param node2 - (down) node.
	 ******************************/
	public static void forward_link_down(Process_Node node1, Process_Node node2){
		node1.add_out(node2);
		node2.add_in(node1);
	}
	
	
	/***********************************
	 * Pops the "up" and "down" stacks.
	 ***********************************/
	public static void pop_stacks(){
		up_stack.pop();
		down_stack.pop();
	}
	
	
	/**********************************************
	 * Process whole word.
	 * @param lexer - lexer (including its state).
	 * @param word - word to be processed.
	 **********************************************/
	public static void process_word(Lexer lexer, String word){
		//declare vars
		char[] keys = word.toCharArray();
		Event event;
		
		//process
		for(int i=0; i<keys.length; i++){
			event = lexer.next(keys[i] + "");
			if (event != null)
				raise_event(event);
		}//end for
	}
	
	
	/**********************************************
	 * Process whole word.
	 * @param lexer - lexer (including its state).
	 * @param word - word to be processed.
	 **********************************************/
	public static void process_word(Lexer lexer, LinkedList<String> word){
		//declare vars
		String key = "";
		Iterator<String> iterator = word.iterator();
		Event event;
		
		//process
		while(iterator.hasNext()){
			key = iterator.next();
			event = lexer.next(key);
			if (event != null)
				raise_event(event);
		}//end for
	}
	
	
	/***********************************
	 * Raises event and handles it.
	 * @param new_event - raised event.
	 ***********************************/
	public static void raise_event(Event new_event){
		//declare vars
		Event current_active_event;
		Queue<Event> temp_Q = new LinkedList<Event>();
		
		//enter new event to queue. if there's already an event in the process
		//then the new event will not be processed in current session but in the original call!
		new_events.add(new_event);
		if(new_events.size() == 1){
			while(new_events.isEmpty() == false){
				//Acquire earliest event in line
				new_event = new_events.peek();
				System.out.println("--->" + new_event.get_name()); //for debug
				
				//elders come first!
				//scan all other (already) active events
				while(active_events.isEmpty() == false){
					current_active_event = active_events.remove();
					//handle event termination
					if (! current_active_event.check_finished()
							&& ! current_active_event.get_action().equals("")){
						System.out.println("--->RE: " + current_active_event.get_name()); //for debug
						current_active_event.call_for_action(new_event);
						temp_Q.add(current_active_event);
					}//end if
				}//end active_events while
				
				//update active Q
				active_events = temp_Q;
				temp_Q = new LinkedList<Event>();
				
				//activate new younger event
				new_event.call_for_action(new Event(""));
				
				//wrap
				if (new_event.check_finished() == false
						&& ! new_event.get_action().equals(""))
					active_events.add(new_event);
				
				new_events.remove();
			}//end new_events while
		}//end if
	}//end raise event
}
