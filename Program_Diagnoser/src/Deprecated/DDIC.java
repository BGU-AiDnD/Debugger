package Deprecated;

import java.util.Hashtable;

//Data Dictionary!!!
public class DDIC {
	
	private static Hashtable<String,String> op_events = new Hashtable<String, String>();
	private static Lexer lexer;
	
	
	/*******************************
	 * Loads lexical data to lexer. 
	 * @param lxr - lexer.
	 *******************************/
	public static void load_data(Lexer lxr){
		//be given lexer
		lexer = lxr;
		
		//////////////Declare operators//////////////////
		op_events.put(".", "");
		op_events.put("{", "");
		op_events.put("}", "");
		op_events.put("/", "");
		op_events.put("(", "");
		op_events.put(")", "");
		op_events.put(";", "");
		op_events.put("+", "");
		op_events.put("-", "");
		op_events.put("%", "");
		op_events.put(":", "");
		op_events.put("=", "");
		op_events.put(">", "");
		op_events.put("<", "");
		op_events.put("!", "");
		op_events.put(",", "");
		op_events.put("&", "");
		op_events.put("|", "");
		op_events.put(""+'"', "");
		op_events.put("space", "");
		op_events.put("newline", "");
		
		
		
		//////////////////Load reserved words to lexer////////////////////
		//load common operators
		lexer.branch_new_line("", new Event("EVENT_NEW_LINE","","RETURN_TO_ROOT"));
		lexer.insert(";", new Event("EVENT_END_STATEMENT","","END_STATEMENT"));
		lexer.insert("/", new Event("EVENT_SLASH"));
		lexer.insert(".", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("+", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("-", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("%", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert(":", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("=", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert(">", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("<", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("!", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert(",", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("&", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		lexer.insert("|", new Event("EVENT_OPERATOR","","RETURN_TO_ROOT"));
		
		//load comments and string literals syntax
		lexer.insert("//", new Event("EVENT_LOCK_LEXER","","LOCK_LEXER"));
		lexer.branch_new_line("//", new Event("EVENT_UNLOCK_LEXER","","UNLOCK_LEXER"));
		lexer.insert("/*", new Event("EVENT_LOCK_LEXER","","LOCK_LEXER"));
		lexer.insert("/**/", new Event("EVENT_CHEK_UNLCK_LXR","","CHECK_UNLOCK_LEXER"));
		lexer.insert(""+'"', new Event("EVENT_LOCK_LEXER","","LOCK_LEXER"));
		lexer.insert(""+'"'+'"', new Event("EVENT_UNLOCK_LEXER","","UNLOCK_LEXER"));
		lexer.insert("'", new Event("EVENT_LOCK_LEXER","","LOCK_LEXER"));
		lexer.insert("''", new Event("EVENT_UNLOCK_LEXER","","UNLOCK_LEXER"));
		
		//load BRACKETS syntax
		lexer.insert("{", new Event("EVENT_OPEN_BLOCK","","OPEN_BLOCK"));
		lexer.insert("}", new Event("EVENT_CLOSE_BLOCK","","CLOSE_BLOCK"));
		lexer.insert("(", new Event("EVENT_OPEN_BRACKET","","OPEN_BRACKET"));
		lexer.insert(")", new Event("EVENT_CLOSE_BRACKET","","CLOSE_BRACKET"));
		lexer.insert("{}", new Event("EVENT_CLOSE_BLOCK","","RETURN_TO_ROOT"));
		lexer.insert("()", new Event("EVENT_CLOSE_BRACKET","","RETURN_TO_ROOT"));

		//load IF syntax
		lexer.insert("if ", null);
		lexer.ignore_space("if ");
		lexer.insert("if(",new Event("EVENT_IF","","IF_OPEN_CRITERIA"));
		lexer.link_to_existing("if ", "if(");
		lexer.insert("if()", new Event("EVENT_CLOSE_IF_C","","IF_CLOSE_CRITERIA"));
		lexer.insert("if();", new Event("EVENT_IF_WRAP","","IF_WRAP"));
		lexer.insert("if(){", new Event("EVENT_OPEN_IF_BLOCK","","OPEN_BRACKET"));
		lexer.insert("if(){}", new Event("EVENT_IF_BLOCK_WRAP","","IF_WRAP"));
		
		//load ELSE syntax
		lexer.ignore_space("if();");
		lexer.insert("if();else ", new Event("EVENT_ELSE","","ELSE_STATEMENT"));
		lexer.ignore_space("if();else ");
		
		lexer.insert("if();else;", new Event("EVENT_ELSE_WRAP","","ELSE_WRAP"));
		lexer.insert("if();else}", new Event("EVENT_ELSE_WRAP","}","ELSE_WRAP")); //special end-block handling
		lexer.link_to_existing("if();else ", "if();else;");
		lexer.link_to_existing("if();else ", "if();else}");
		
		lexer.insert("if();else{", new Event("EVENT_ELSE_BLOCK","","OPEN_BLOCK"));
		lexer.link_to_existing("if();else ", "if();else{");
		lexer.insert("if();else{}", new Event("EVENT_ELSE_WRAP","","ELSE_WRAP"));
		
		lexer.ignore_space("if(){}");
		lexer.insert("if(){}els", null);
		lexer.link_to_existing("if(){}els", "if();else");
		
		//load SWITCH (case) syntax
		lexer.insert("switch ", null);
		lexer.ignore_space("switch ");
		lexer.insert("switch(", new Event("EVENT_SWITCH","","SWITCH_OPEN_CRITERION"));
		lexer.link_to_existing("switch ", "switch(");
		lexer.insert("switch()", new Event("EVENT_SWITCH_CLOSE_C","","SWITCH_CLOSE_CRITERION"));
		lexer.insert("switch() ", null);
		lexer.ignore_space("switch() ");
		lexer.insert("switch(){", new Event("EVENT_SWITCH_BLOCK","","SWITCH_BLOCK"));
		lexer.link_to_existing("switch() ", "switch(){");
		lexer.insert("switch(){}", new Event("EVENT_SWITCH_WRAP","","SWITCH_WRAP"));
		
		lexer.insert("case ", new Event("EVENT_CASE_JUNCTION","","CASE_JUNCTION"));
		lexer.insert("case:", new Event("EVENT_CASE_JUNCTION","","CASE_JUNCTION"));
		
		
	}
	
	/*********************************************
	 * Checks whether a given key is an operator.
	 * @param key - key char.
	 * @return
	 *********************************************/
	public static boolean is_operator(String key){
		return op_events.containsKey(key);
	}
	
	
	
	////////////////////// Actions definitions!!! ///////////////////////////////////
	/************************************************************
	 * Performs specific action.
	 * @param action_code - action code.
	 * @param event - current_event.
	 * @param last_event - last event.
	 ************************************************************/
	public static void do_action(String action_code, Event event, Event last_event){
		//declare vars
		Process_Node node;
		Event temp_event;
		String buffer_word;
		
		switch (action_code){
		case "END_STATEMENT":
			event.mark_as_finished();
			
			temp_event = lexer.end_statement();
			if (temp_event != null)
				Event_Handler.raise_event(temp_event);
			
			break;
		
		case "METHOD_CALL":
			//handle creation of opening parameters node
			node = new Process_Node(event.get_param(), "method_open_inputs");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
		case "METHOD_WRAP":
			//handle closing parameters node
			node = new Process_Node(event.get_param(), "method_close_inputs");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//handle method node itself
			node = new Process_Node(event.get_param(), "method");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			lexer.send_pointer_to_root();
			event.mark_as_finished();
			break;
			
		case "OPEN_BRACKET":
			event.mark_as_finished();
			lexer.new_pointer();
			break;
		
		case "OPEN_BLOCK":
			event.mark_as_finished();
			temp_event = lexer.open_block();
			if (temp_event != null)
				Event_Handler.raise_event(temp_event);
			
			break;
			
		case "CLOSE_BRACKET":
			event.mark_as_finished();
			event = lexer.kill_pointer(")");
			if (event != null)
				Event_Handler.raise_event(event);
			break;
			
		case "CLOSE_BLOCK":
			event.mark_as_finished();
			event = lexer.kill_pointer("}");
			if (event != null)
				Event_Handler.raise_event(event);
			break;
		
		case "IF_OPEN_CRITERIA":
			node = new Process_Node("", "if open criteria");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
		case "IF_CLOSE_CRITERIA":
			node = new Process_Node("", "if close criteria");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//prepare IF fork
			node = new Process_Node("","if fork");
			Event_Handler.push_to_up_stack(node);
			Event_Handler.push_to_down_stack(new Process_Node("","if drain"));
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
			
		case "IF_WRAP":
			//connect main stream to drain and fix drain as current
			node = Event_Handler.get_current();
			Event_Handler.forward_link_down(node);
			Event_Handler.update_current_node(Event_Handler.peek_down_stack());
			
			//wrap
			lexer.get_buffer_word(); //empty buffer word
			event.mark_as_finished();
			
			//raise event "wait_for_else"
			Event_Handler.raise_event(new Event("EVENT_WAIT_FOR_ELSE","","WAIT_FOR_ELSE"));
			break;
			
		case "WAIT_FOR_ELSE":	
			//handle no else
			if (last_event.get_name().equals("EVENT_UNRECOGNIZED_LEXEME")
					|| last_event.get_name().equals("EVENT_CLOSE_BLOCK")){
				node = Event_Handler.peek_up_stack(); //get joint point
				Event_Handler.forward_link_down(node); //direct connection from top down
				Event_Handler.pop_stacks(); //no more need for saving forking nodes.
				event.mark_as_finished();
				
				//get buffer word
				buffer_word = lexer.get_buffer_word();
				
				if (last_event.get_name().equals("EVENT_UNRECOGNIZED_LEXEME"))
					//reduce nesting and end any higher IF
					//also, re-enter buffer word at new state of lexer
					Event_Handler.raise_event(new Event("EVENT_NO_ELSE1",buffer_word,"HANDLE_NO_ELSE01"));
				
				else if (last_event.get_name().equals("EVENT_CLOSE_BLOCK")){
					//in this scenario, we can skip on nesting reduction because it already happened
					//we do need to re-enter buffer word at new state of lexer
					Event_Handler.raise_event(new Event("EVENT_NO_ELSE2",buffer_word,"HANDLE_NO_ELSE02"));
				}
			}
			
			//handle else
			else if (last_event.get_name().equals("EVENT_ELSE") 
					|| last_event.get_name().equals("EVENT_ELSE_BLOCK")){
				node = Event_Handler.peek_up_stack(); //get joint point
				Event_Handler.update_current_node(node);
				event.mark_as_finished();
				//we need to save the forking nodes for else wrap
			}
			
			break;
			
		case "HANDLE_NO_ELSE01":
			//reduce nesting and end any higher IF
			temp_event = lexer.end_statement();
			if (temp_event != null)
				Event_Handler.raise_event(temp_event);
			
			//wrap
			event.mark_as_finished();

			//re-enter buffer word at new state of lexer
			//must do this in separate event to allow IF-WRAP events to end successfully
			buffer_word = event.get_param();
			Event_Handler.raise_event(new Event("EVENT_NO_ELSE2",buffer_word,"HANDLE_NO_ELSE02"));
			break;
			
		case "HANDLE_NO_ELSE02":
			//re-enter buffer word at new state of lexer
			event.mark_as_finished();
			buffer_word = event.get_param();
			
			//be aware of over-nesting-reduction
			//since '}' has an intrinsic close block event
			if (! buffer_word.equals("}"))
				Event_Handler.process_word(lexer, buffer_word);
			break;
	
			
		case "ELSE_STATEMENT":
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
			
		case "ELSE_WRAP":
			//join to drain
			node = Event_Handler.get_current(); //get joint point
			Event_Handler.forward_link_down(node);
			
			node = Event_Handler.peek_down_stack();
			Event_Handler.update_current_node(node); 
			
			
			//wrap event
			Event_Handler.pop_stacks(); //no more need for saving forking nodes.
			event.mark_as_finished();
			
			//reduce nesting and end any higher IF
			temp_event = lexer.end_statement();
			if (temp_event != null)
				Event_Handler.raise_event(temp_event);
			
			//handle special case of block ending
			if (event.get_param().equals("}"))
				Event_Handler.raise_event(new Event("EVENT_CLOSE_BLOCK","","CLOSE_BLOCK"));
			break;
			
		case "SWITCH_OPEN_CRITERION":
			
			node = new Process_Node("", "switch open criteria");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
		case "SWITCH_CLOSE_CRITERION":
			node = new Process_Node("", "switch close criteria");
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//build switch fork
			node = new Process_Node("","switch fork");
			Event_Handler.push_to_up_stack(node);
			Event_Handler.push_to_down_stack(new Process_Node("","switch drain"));
			Event_Handler.link_to_current(node);
			Event_Handler.update_current_node(node);
			
			//wrap
			event.mark_as_finished();
			break;
			
		case "SWITCH_BLOCK":
			lexer.new_pointer();
			event.mark_as_finished();
			break;
			
		case "SWITCH_WRAP":
			node = Event_Handler.get_current();
			Event_Handler.forward_link_down(node);
			Event_Handler.update_current_node(Event_Handler.peek_down_stack());
			Event_Handler.pop_stacks();
			
			//wrap
			lexer.send_pointer_to_root();
			event.mark_as_finished();
			break;
			
		case "CASE_JUNCTION":
			if (Event_Handler.get_current() != Event_Handler.peek_up_stack()){
				node = Event_Handler.get_current();
				Event_Handler.forward_link_down(node);
			}
			
			Event_Handler.update_current_node(Event_Handler.peek_up_stack());
			
			//wrap
			lexer.send_pointer_to_root();
			event.mark_as_finished();
			break;
			
		case "CLASS_NAME":
			event.mark_as_finished();
			lexer.send_pointer_to_root();
			Event_Handler.raise_event
			(new Event("EVENT_CHECK_CLASS_INSTANCE",event.get_param(),"CHECK_CLASS_INSTANCE"));
			break;
			
		case "CHECK_CLASS_INSTANCE":
			//handle false call
			if (! last_event.get_name().equals("EVENT_END_STATEMENT")
					&& ! last_event.get_name().equals("EVENT_OPERATOR")
					&& ! last_event.get_name().equals("EVENT_UNRECOGNIZED_LEXEME")
					&& ! last_event.get_name().equals("EVENT_CLOSE_BRACKET")
					&& ! last_event.get_name().equals(""))
				event.mark_as_finished();
			
			//handle (probably) justified call
			else if (last_event.get_name().equals("EVENT_END_STATEMENT")
					|| last_event.get_name().equals("EVENT_OPERATOR")
					|| last_event.get_name().equals("EVENT_CLOSE_BRACKET")){
				
				buffer_word = lexer.last_word();
				if (event.get_param().equals(buffer_word))
					event.mark_as_finished(); //false call after all
				
				else{ //justified call
					event.mark_as_finished();
					lexer.insert_class_instance(event.get_param(), buffer_word);
				}
			}//end super if
			break;
		
		case "RETURN_TO_ROOT":
			lexer.send_pointer_to_root();
			event.mark_as_finished();
			break;
			
		case "LOCK_LEXER":
			lexer.lock_lexer();
			event.mark_as_finished();
			break;
			
		case "UNLOCK_LEXER":
			lexer.unlock_lexer();
			event.mark_as_finished();
			break;
			
		case "CHECK_UNLOCK_LEXER":
			String last = lexer.last_word();
			int length = last.length();
			if (length >= 2 && last.charAt(length - 2) == '*' 
					&& last.charAt(length - 1) == '/'){
				Event_Handler.raise_event(new Event("EVENT_UNLOCK_LEXER","","UNLOCK_LEXER"));
				event.mark_as_finished();
			}	
			break;
			
		}//end switch
	}//end do_action
	
	/*************************************************************
	 * For debug.
	 *************************************************************/
	public static void main(String[] args){

		
	}//end main
}
