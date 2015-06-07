package Deprecated;

import java.util.Scanner;
import java.util.Stack;


public class Lexer {
	
	//pointers handling
	private Lexi_Node anchor;
	private Lexi_Node pointer, residual_pointer;
	private Stack<Lexi_Node> pointerstack;
	private int nest_level;
	
	//pointer flags
	private boolean pointer_lock, lexer_lock;
	
	//last word handling
	private String last_word, buffer_word;
	
	
	/***************
	 * Constructor.
	 ***************/
	public Lexer(){
		//anchor handling
		anchor = new Lexi_Node();
		anchor.ignore_space();
		lexer_lock = false;
		
		//pointer handling
		pointer = anchor; //points to root at first
		residual_pointer = anchor;
		pointerstack = new Stack<Lexi_Node>(); //empty at first
		nest_level = 0;
		pointer_lock = false;
		
		//last word handling
		last_word = "";
		buffer_word = "";
	}
	
	
	/******************************************************************************
	 * Checks whether current pointer can branch on to given key.
	 * @param key - key.
	 * @return True - if current pointer can branch on to key. False - otherwise.
	 ******************************************************************************/
	public boolean has_branch(String key){
		return pointer.has_branch(key);
	}
	
	
	/*********************************************************
	 * Kills a pointer.
	 * Replaces the given pointer with next in stack pointer.
	 * @param pointer - pointer to be killed.
	 *********************************************************/
	public Event kill_pointer(String key){
		//dispose of current pointer and return to older one
		pointer = pointerstack.pop();
		nest_level --;
		
		//check nesting consistency
		if (nest_level < 0)
			System.out.println("Warning! Nesting inconsistency.");
		
		//for debug
		System.out.println("nest level: " + nest_level);
		
		return next(key);
	}
	
	
//	/*******************************************************
//	 * Kills several pointers in one action.
//	 * @param num - number of pointers to be killed.
//	 * @param key - the key to process in the new location.
//	 *******************************************************/
//	public Event kill_several_pointers(int num, String key){
//		for(int i=0; i<num; i++){
//			pointer = pointerstack.pop();
//			nest_level --;
//		}
//		
//		//check nesting consistency
//		if (nest_level < 0)
//			System.out.println("Warning! Nesting inconsistency.");
//		
//		//for debug
//		System.out.println("nest level: " + nest_level);
//		
//		return next(key);
//	}
	
	
	/******************************************
	 * Creates new pointer.
	 * Enters old pointer into pointers stack.
	 ******************************************/
	public void new_pointer(){
		//create new pointer
		pointerstack.push(pointer);
		pointer = anchor;
		
		//update nesting level
		nest_level ++;
		
		//for debug
		System.out.println("nest level: " + nest_level);
	}
	
	
	/*************************
	 * Sends pointer to root.
	 *************************/
	public void send_pointer_to_root(){
		residual_pointer = pointer; //for comments needs
		pointer = anchor;
	}
	
	
	/***********************************************
	 * nesting level getter.
	 * @return the level of nesting. 0 -base level.
	 ***********************************************/
	public int get_nest_level(){
		return nest_level;
	}
	
	
	/******************************
	 * Locks lexer (for comments).
	 ******************************/
	public void lock_lexer(){
		lexer_lock = true;
		
		buffer_word = "";
		last_word = "";
	}
	
	
	/********************************
	 * Unlocks lexer (for comments).
	 ********************************/
	public void unlock_lexer(){
		//do the obvious
		lexer_lock = false;
		
		//handle continuity of normal code
		pointer = residual_pointer; 
		Event event = next("space");
		if (event != null)
			Event_Handler.raise_event(event);
		
		//handle last word tracking
		buffer_word = "";
		last_word = "";
	}
	
	
	/******************************
	 * Lexeme insertion into tree.
	 * @param lexeme - lexeme.
	 * @param event - event name.
	 ******************************/
	public void insert(String lexeme, Event event){
		//declare vars
		Lexi_Node current_node = anchor;
		char[] chars = lexeme.toCharArray();
		String temp_key;
		
		//process
		for(int i=0; i<chars.length; i++){
			temp_key = (chars[i] + "");
			//handle space
			if (temp_key.equals(" "))
				temp_key = "space";
			//add nodes as necessary
			if (current_node.get_next(temp_key) == null)
				current_node.branch(temp_key);
			current_node = current_node.get_next(temp_key);
		}//end for
		
		//set event
		current_node.set_event(event);
	}
	
	
	/******************************************
	 * Inserts a method events into the lexer.
	 * Current class owns the method.
	 * @param meth_name - method name.
	 ******************************************/
	public void insert_method(String method_name){
		insert_method("",method_name);
	}
	
	
	/******************************************
	 * Inserts a method events into the lexer.
	 * @param meth_name - method name.
	 ******************************************/
	public void insert_method(String class_name, String method_name){
		String lexeme = "";
		
		//construct lexeme
		if (! class_name.equals(""))
			lexeme = class_name + '.' + method_name;
		else lexeme = method_name;
		
		//insert lexeme
		insert(lexeme, null);
		ignore_space(lexeme);
		insert(lexeme + '(', new Event("EVENT_METHOD_CALL",lexeme,"METHOD_CALL"));
		
		//handle actual method call event
		insert(lexeme + "()", new Event("EVENT_METHOD_WRAP",lexeme,"METHOD_WRAP"));
	}
	
	
	/**********************************
	 * Inserts a class.
	 * @param class_name - class name.
	 **********************************/
	public void insert_class(String class_name){
		String lexeme = "";
		
		//insert lexeme for class itself
		insert(class_name + ' ', new Event("EVENT_CLASS_NAME",class_name,"CLASS_NAME"));
		
		//insert lexeme for "new" operation
		insert("new " + class_name, null);
		ignore_space("new ");
		ignore_space("new " + class_name);
		
		lexeme = class_name + '.' + class_name;
		insert("new " + class_name + '(', new Event("EVENT_CONSTRUCTOR_CALL",lexeme,"METHOD_CALL")); //constructor call
		insert("new " + class_name + "()", new Event("EVENT_CONSTRUCTOR_WRAP",lexeme,"METHOD_WRAP")); //constructor wrap
		
		link_to_existing("new " + class_name + "()", class_name + '.');
	}
	
	
	/****************************************
	 * Inserts class instance.
	 * @param class_name - class name.
	 * @param instance_name - instance name.
	 ****************************************/
	public void insert_class_instance(String class_name, String instance_name){
		insert(instance_name, null);
		link_to_existing(instance_name, class_name + '.');
	}
	
	
	/*****************************************************
	 * Make lexeme ignorant to space key. 
	 * @param lexeme - lexeme that will ignore space key.
	 *****************************************************/
	public void ignore_space(String lexeme){
		//declare vars
		Lexi_Node current_node = anchor;
		char[] chars = lexeme.toCharArray();
		String temp_key;
		
		//traverse tree
		for(int i=0; i<chars.length; i++){
			temp_key = (chars[i] + "");
			//handle space
			if (temp_key.equals(" "))
				temp_key = "space";
			//advance nodes as necessary
			current_node = current_node.get_next(temp_key);
		}//end for
		
		//make node space ignorant
		current_node.ignore_space();
	}
	
	
	/**********************************************
	 * Branches a given lexeme with "newline" key.
	 * @param lexeme - lexeme to be branched.
	 * @param event - event.
	 **********************************************/
	public void branch_new_line(String lexeme, Event event){
		//declare vars
		Lexi_Node current_node = anchor;
		char[] chars = lexeme.toCharArray();
		String temp_key;
		
		//traverse tree
		for(int i=0; i<chars.length; i++){
			temp_key = (chars[i] + "");
			//handle space
			if (temp_key.equals(" "))
				temp_key = "space";
			//advance nodes as necessary
			current_node = current_node.get_next(temp_key);
		}//end for
		
		//plant event
		current_node.branch("newline");
		current_node = current_node.get_next("newline");
		current_node.set_event(event);
	}
	
	
	/************************************
	 * Links a lexeme to another lexeme.
	 * @param lexeme1 - lexeme.
	 * @param lexeme2 - lexeme.
	 ************************************/
	public void link_to_existing(String lexeme1, String lexeme2){
		//declare vars
		Lexi_Node current_node1 = anchor;
		Lexi_Node current_node2 = anchor;
		char[] chars1 = lexeme1.toCharArray();
		char[] chars2 = lexeme2.toCharArray();
		String temp_key= "";
		
		//traverse lexeme 1
		for(int i=0; i<chars1.length; i++){
			temp_key = (chars1[i] + "");
			//handle space
			if (temp_key.equals(" "))
				temp_key = "space";
			//add nodes as necessary
			current_node1 = current_node1.get_next(temp_key);
		}//end for
		
		//traverse lexeme 2
		for(int i=0; i<chars2.length; i++){
			temp_key = (chars2[i] + "");
			//handle space
			if (temp_key.equals(" "))
				temp_key = "space";
			//add nodes as necessary
			current_node2 = current_node2.get_next(temp_key);
		}//end for
		
		//make the link
		current_node1.branch_to_existing(temp_key, current_node2);
	}
	
	
	/**************************************
	 * Last word getter.
	 * Only works after an operator event!
	 * @return last word.
	 **************************************/
	public String last_word(){
		return last_word;
	}
	
	
	/****************************************
	 * Last buffer (incomplete) word getter.
	 * Also cleans the buffer.
	 * @return last buffer word.
	 ****************************************/
	public String get_buffer_word(){
		String buffer = buffer_word;
		buffer_word = "";
		return buffer;
	}
	
	
	/**************************************
	 * Statement ending special treatment.
	 **************************************/
	public Event end_statement(){
		//declare vars
		Lexi_Node prev_pointer = null;
		
		//unlock pointer, since ';' is operator
		pointer_lock = false;
		
		//check previous pointer
		if (pointerstack.isEmpty() == false)
			prev_pointer = pointerstack.peek();
		
		//handle over nesting
		if (prev_pointer != null && prev_pointer != anchor 
				&& prev_pointer.get_next(";") != null){
			kill_pointer(";");
			return pointer.get_event();
		}
		
		else{
			send_pointer_to_root();
			return null;
		}
	}
	
	
	/********************************
	 * Block open special treatment.
	 ********************************/
	public Event open_block(){
		//declare vars
		Lexi_Node prev_pointer = null;
		
		//unlock pointer, since '{' is operator
		pointer_lock = false;
		
		//check previous pointer
		if (pointerstack.isEmpty() == false)
			prev_pointer = pointerstack.peek();
		
		//handle over nesting
		if (prev_pointer != null && prev_pointer != anchor 
				&& prev_pointer.get_next("{") != null){
			kill_pointer("{");
			return pointer.get_event();
		}
		
		else{
			new_pointer();
			return null;
		}
	}
	
	
	
	/*******************************************************
	 * Advances the current pointer according to given key.
	 * @param key - key.
	 * @return event (null if there isn't any).
	 *******************************************************/
	public Event next(String key){
		//handle lexer locking (for comments)
		if (lexer_lock == true){
			last_word += key;
			if (pointer.get_next(key) == null)
				return null;
			
			else{
				pointer = pointer.get_next(key);
				return pointer.get_event();
			}//end if
		}//end super if (lexer is locked)
		
		//handle pointer unlock (only operators can unlock pointer)
		else if ((pointer_lock == true || pointer.get_next(key) == null)
				&& DDIC.is_operator(key)){
			pointer_lock = false;
			send_pointer_to_root(); //return pointer to root
			
			//handle last word
			last_word = buffer_word;
			buffer_word = "";
			
			return next(key);
		}
		
		//handle unlocked pointer but unrecognized lexeme
		else if (pointer_lock == false && pointer.get_next(key) == null){
			pointer_lock = true; //lock pointer
			buffer_word += key; //maintain last_word
				
			return new Event("EVENT_UNRECOGNIZED_LEXEME"); //no event has occurred
		}
		
		//handle (partially) recognized lexeme
		else if (pointer_lock == false && pointer.get_next(key) != null){
			pointer = pointer.get_next(key);
			
			//handle last word
			if (DDIC.is_operator(key) && ! buffer_word.equals("")){ //handles operators sequence 
				last_word = buffer_word;
				buffer_word = ""; 
			}
			else if (! key.equals("space"))
				buffer_word += key; //maintain last_word
			
			//wrap
			return pointer.get_event();
		}
		
		//handle locked pointer
		else{
			buffer_word += key; //maintain last_word
			return null; 
		}
		
	}


	/********************************************************************************
	 * For debug.
	 ********************************************************************************/
	public static void main(String[] args){
		//Initialize objects
		Lexer lexer = new Lexer();
		Event_Handler.load_graph_seed(new Process_Graph("some method"));
		Scanner scan = new Scanner(System.in);
		Event event;
		
		//load lexer
		DDIC.load_data(lexer);
		lexer.insert("Tom", new Event("my name!"));
		lexer.insert_method("run");
		lexer.insert_method("class", "run");
		lexer.insert_class("class");
		
		//process
		String key = scan.next();
		while(!key.equals("q")){
			//handle space
			event = lexer.next(key);
			if (event != null)
				Event_Handler.raise_event(event);
			key = scan.next();
		}//end while
		
		scan.close();
	}
}
