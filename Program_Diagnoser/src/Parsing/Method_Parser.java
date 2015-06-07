package Parsing;

import static java.nio.file.StandardCopyOption.REPLACE_EXISTING;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

import Deprecated.DDIC;
import Deprecated.Event;
import Deprecated.Event_Handler;
import Deprecated.Lexer;
import Deprecated.Process_Graph;

public class Method_Parser {
	private static Hashtable<String, LinkedList<String>> classes = new Hashtable<String, LinkedList<String>>();
	private static Hashtable<String,String> comp_map = new Hashtable<String, String>();
	private static Hashtable<String, Process_Graph> methods_graph = new Hashtable<String, Process_Graph>();
	private static int indexer = -1;
	
	
	/*********************************************
	 * Inserts a new class name.
	 * @param class_name - name of the new class.
	 *********************************************/
	public static void insert_class(String class_name){
		classes.put(class_name, new LinkedList<String>());
	}
	
	
	/**********************************************************
	 * Inserts new method name.
	 * Not supports overloading!!
	 * @param class_name - name of the class.
	 * @param method_name - name of the method to be inserted.
	 **********************************************************/
	public static void insert_method(String class_name, String method_name){
		if (! classes.get(class_name).contains(method_name)){
			indexer++;
			String index = "" + indexer; //casting
		
			classes.get(class_name).add(method_name);
			comp_map.put(index, class_name + '.' + method_name);	
			comp_map.put(class_name + '.' + method_name, index); //map also the opposite side.
		}
	}
	
	
	/*****************************************
	 * Methods getter (of a specific class).
	 * @param class_name - name of the class.
	 * @return list of the class's methods.
	 *****************************************/
	public static LinkedList<String> get_methods_of(String class_name){
		return classes.get(class_name);
	}
	
	
	/******************************
	 * Classes getter.
	 * @return all classes' names.
	 ******************************/
	public static LinkedList<String> get_all_classes(){
		//declare vars
		LinkedList<String> list = new LinkedList<String>();
		Enumeration<String> enumerator =  classes.keys();
		
		//cast to linked list
		while(enumerator.hasMoreElements()){
			list.add(enumerator.nextElement());
		}//end while
		
		return list;
	}
	
	
	/**************************************
	 * Methods getter (all of them).
	 * @return list of all methods' names.
	 **************************************/
	public static LinkedList<String> get_all_methods(){
		//declare vars
		LinkedList<String> list = new LinkedList<String>();
		Enumeration<String> enumerator =  methods_graph.keys();
		
		//cast to linked list
		while(enumerator.hasMoreElements()){
			list.add(enumerator.nextElement());
		}//end while
		
		return list;
	}
	
	
	/***************************
	 * Prints the methods list.
	 ***************************/
	public static void print_all_methods(){
		//get methods
		LinkedList<String> methods_list = get_all_methods();
		
		//print
		System.out.println("\nFound these methods:");
		
		Iterator<String> iterator = methods_list.iterator();
		while(iterator.hasNext()){
			System.out.println(iterator.next());
		}//end while
	}
	
	
	/*****************************************
	 * Returns name of given component index.
	 * @param index - index of component.
	 * @return the component name.
	 *****************************************/
	public static String translate_comp(int index){
		String temp = "" + index;
		return comp_map.get(temp);
	}
	
	/*****************************************
	 * Returns index of given component name.
	 * @param method - method name.
	 * @return the method's index.
	 *****************************************/
	public static String translate_comp(String method){
		return comp_map.get(method);
	}
	
	
	/*******************************************************
	 * Inserts a graph.
	 * @param method - method official name (class.method).
	 * @param graph - method process graph.
	 *******************************************************/
	public static void insert_graph(String method, Process_Graph graph){
		methods_graph.put(method, graph);
	}
	
	
	/*******************************************************
	 * Graph getter.
	 * @param method - method official name (class.method).
	 * @return method process graph.
	 *******************************************************/
	public static Process_Graph get_graph(String method){
		return methods_graph.get(method);
	}
	
	
	/********************************************************
	 * Finds and tags methods in classes files.
	 * @param file_names - classes file names.
	 * @throws IOException
	 ********************************************************/
	public static void tag_methods(File[] files) throws IOException{
		methods_parser(files, true, true, false);
		System.out.println("\nFiles were created in: " + FilesAssist.get_tagged_path().toRealPath());
	}
	
	
	/******************************************
	 * Generates methods graphs.
	 * @param file_names - classes file names.
	 * @throws IOException
	 ******************************************/
	public static void generate_methods_graphs(File[] files) throws IOException{
		methods_parser(files, false, true, true);
	}

	
	/********************************************************
	 * Finds and tags methods in classes files.
	 * @param file_names - classes file names.
	 * @param tag - is to tag methods?
	 * @param hook - is to hook methods?
	 * @param gen_graph - is to generate graph for methods?
	 * @throws IOException
	 ********************************************************/
	private static void methods_parser(File[] files, boolean tag, boolean hook, 
			boolean gen_graph) throws IOException{
		

		
		//make sure 'tagged' folder exists
		FilesAssist.create_tagged_dir();
		
		/////start process files////////
		for(int i=0; i < files.length; i++){
			File current_file = files[i];
			
			//declare vars
			String class_name 		= "";
			String method_name 		= "";
			String method_modifier 	= "";
			String last_word 		= "";
			String last_word_2		= "";
	        String temp 			= "";
			Scanner scanner = null;
			
			//declare flags
			boolean first_bracket 		= false; 
			boolean short_comment_flag  = false;
			boolean long_comment_flag   = false;
			boolean string_literal_flag = false;
			boolean char_literal_flag   = false;
			boolean suspect 			= false;
			boolean found_method 		= false;
			@SuppressWarnings("unused")
			boolean in_a_method 		= false;
			boolean shtroodle_flag 		= false;
			boolean imported_logger 	= false;
			
			//declare counters
			int brackets_c01 = 0; //'(' counter
			int brackets_c02 = 0; //'{' counter
			
			//declare graph related objects
			LinkedList<String> signature_buffer = new LinkedList<String>();
			Process_Graph graph = null;
			Lexer lexer = null;
			Event event = null;

			//get class name (handles Java files ONLY!!)
			class_name = current_file.getName().replace(".java","");
			//tag
			if (tag == true)
				Method_Parser.insert_class(class_name);
			
			//construct writer
			PrintWriter writer = null;
			File class_file = new File("tagged/" + class_name + ".java");
			writer = new PrintWriter(class_file);

            //construct scanner
			scanner = new Scanner(new BufferedReader(new FileReader(current_file)));
            scanner.useDelimiter("");

            //start scanning chars
            while (scanner.hasNext()) {
            	temp = scanner.next();
            	writer.write(temp);
            	
            	switch(temp){
            		case "\n":
            			temp = "newline";
            			break;
            		
            		case " ":
            			temp = "space";
            			break;
            		
            		case "\r":
            			temp = "space";
            			break;
            		
            		case "\f":
            			temp = "space";
            			break;
            		
            		case "\t":
            			temp = "space";
            			break; 
            		
            	}//end switch
            	
            	//maintain last word
    			switch(temp){
    			case ""+'"':
    				if (!shtroodle_flag && !long_comment_flag && !short_comment_flag 
    						&& !char_literal_flag){
    					string_literal_flag = ! string_literal_flag;
	    				
    					if (brackets_c01 == 0)
    						last_word += '"';
    				} 
    				break; 
    				
    			case "'":
    				if (!shtroodle_flag && !long_comment_flag && !short_comment_flag && !string_literal_flag){
    					char_literal_flag = ! char_literal_flag;
    					
    					if (brackets_c01 == 0)
    						last_word += "'";
    				} 
    				break; 
    			
    			case "/":
    				if (last_word.length() > 0 
    						&& last_word.charAt(last_word.length() - 1) == '/'
    						&& !string_literal_flag
    						&& !shtroodle_flag){
    					short_comment_flag = true;
    					last_word += '/';
    				}
    				else if (last_word.length() > 0
    						&& last_word.charAt(last_word.length() - 1) == '*'
    						&& !string_literal_flag
    						&& !shtroodle_flag){
    					long_comment_flag = false;
    					last_word_2 = "";
    					last_word = "";
    				}
    				
    				else last_word += "/";
    				break;
    			
    			case "newline": 
    				if(short_comment_flag == true){
    					short_comment_flag = false;
    					last_word_2 = last_word.toString();
    					last_word = "";
    				}
    				
    				else if(shtroodle_flag == true){
    					shtroodle_flag = false;
    					if (!last_word.equals("")) //don't loose buffered second word for blanks sequence
    						last_word_2 = last_word.toString();

    					last_word = "";
    				}
    				break;
    			
    			case "@": if (!shtroodle_flag && !short_comment_flag && !long_comment_flag
    							&& !char_literal_flag && !string_literal_flag)
    						shtroodle_flag = true;
    				break;
    				
    			case "space":
    				if (!shtroodle_flag /*&& !short_comment_flag && !long_comment_flag*/ 
    						&& !char_literal_flag && !string_literal_flag 
    						&& brackets_c01 == 0 && !suspect){
    					
    					if (!last_word.equals("")) //don't loose buffered second word for blanks sequence
    						last_word_2 = last_word.toString();
    					
    					last_word = "";
    				}
    				break;
    				
    			case "*":
    				if (last_word.length() > 0
    						&& last_word.charAt(last_word.length() - 1) == '/'
    						&& !string_literal_flag
    						&& !shtroodle_flag
    						&& !long_comment_flag
    						&& !short_comment_flag)
    					long_comment_flag = true;
    				
    				last_word += '*';
    				break;
    				
    			case "(":
    				if (!shtroodle_flag && !short_comment_flag && !long_comment_flag 
    						&& !char_literal_flag && !string_literal_flag){
    					brackets_c01 ++;
    					if (brackets_c01 == 1)
    						last_word += '(';
    				}
    				break;
    				
    			case "{":
    				if (!shtroodle_flag && !short_comment_flag && !long_comment_flag 
    						&& !char_literal_flag && !string_literal_flag){
    					suspect = false;
    					if (first_bracket == false)
    						brackets_c02 = 1;
    					else brackets_c02++;
    					
    						last_word += '{';
    				}	
    			
    				break;
    				
    			case ")":
    				if (!shtroodle_flag && !short_comment_flag && !long_comment_flag 
    						&& !char_literal_flag && !string_literal_flag){
    					brackets_c01 --;
    					if(brackets_c01 == 0){
    						last_word += ')';
    						suspect = true;
    					}
    				}
    				break;
    				
    			case "}":
    				if (!shtroodle_flag && !short_comment_flag && !long_comment_flag 
    						&& !char_literal_flag && !string_literal_flag){
    					brackets_c02 --;
    					
    					if (brackets_c02 == 0){
    						last_word_2 = "";
    						last_word = "";
    						in_a_method = false;		
    					}//end if (brackets_c02 == 0)
    				}//end super if	
    				break;
    				
    			case ";":
    				if (!shtroodle_flag && !short_comment_flag && !long_comment_flag 
    						&& !char_literal_flag && !string_literal_flag){
    					
    					last_word_2 = "";
    					last_word = "";
    					suspect = false;
    					
        				if (imported_logger == false){
        					writer.println("");
        					writer.println("import Implant.*;");
        					imported_logger = true;
        				}
    				}
    				break;

    			default:
    				if (!shtroodle_flag && brackets_c01 == 0 && !suspect && !char_literal_flag 
    				&& !short_comment_flag && !long_comment_flag)
    					last_word += temp;
    			}//end switch
    			
    			
    			///maintain signature buffer///
    			if (temp.equals("(") && brackets_c01 == 1){
					signature_buffer.clear();
    				signature_buffer.add("(");	
    			}
    			else if (! temp.equals("{") && ! temp.equals("}"))
    				signature_buffer.add(temp);
	            
    			///check for method///
    			if (!short_comment_flag && !long_comment_flag 
    					&& !string_literal_flag && brackets_c01 == 0 
    					&& brackets_c02 == 1 && last_word.length() > 3) {
    				//get 3 last chars
    				String end_seq = last_word.substring(last_word.length() - 3);
    				if (end_seq.equals("(){")){
    					
    					/////////////////METHOD FOUND!//////////////////
    					last_word = last_word.substring(0,last_word.length() - 3); //trim
    					method_name = "" + last_word; 
    					method_modifier = "" + last_word_2;
    					
    					//identify constructors
    					if (method_modifier.equals("") || method_name.equals(class_name) || method_modifier.equals("public") 
    							|| method_modifier.equals("protected") || method_modifier.equals("private"))
    						method_modifier = "constructor";
    					
    					in_a_method = true;
    					
    					if (tag == true)
    						System.out.println("found method: " + class_name + '.' + method_name);
    					first_bracket = true; //first bracket was found
    					
    					//update organizer (tag)
    					if (tag == true)
    						insert_method(class_name,method_name);
    					
    					//hook method
    					if (hook == true && !method_modifier.equals("constructor")){
        					writer.println();
        					writer.println("Logger.log(" + '"' + class_name + '.'
        							+ method_name + '"' + ");");
        					
        					//also, plant bug switcher
        					plant_bug_switch(writer, method_modifier, class_name, method_name);
        					plant_bug_return(writer, method_modifier);
    					}//end if (hook method)
    					
    					//generate graphs
    					if (gen_graph == true){
    						found_method = true; //for next method
    						
    						//initialize
    						graph = new Process_Graph(last_word);
    						lexer = new Lexer();
    						Event_Handler.load_graph_seed(graph); //resets the handler
    											
    						//load lexer
    						DDIC.load_data(lexer);
    						load_classes_to_lexer(lexer, class_name);
    						
    						//insert graph to organizer
    						insert_graph(class_name + '.' + method_name, graph);
    						
    						//start lexing
    						Event_Handler.process_word(lexer, signature_buffer); //handle method signature
    						Event_Handler.raise_event(lexer.next("{"));
    					
    					}//end if (generate graphs)
    				}//end if (found method) 
    			}//end super if
    			
    			//handle graphs generation
    			if (gen_graph == true && found_method == true)
					if (brackets_c02 < 0 && temp.equals("}")){
						event = lexer.next("}");
						if (event != null)
							Event_Handler.raise_event(event);
						found_method = false;
						Event_Handler.seal_graph(method_name);
					}
    			
					else{
						System.out.println(temp);
						event = lexer.next(temp);
						if (event != null)
							Event_Handler.raise_event(event);
					}
    					
            }//end while (chars stream of current file)           
            
            ////wrap iteration
            //close streams
            writer.close();
            scanner.close();
            
            //copy modified file to original location
            Files.copy(class_file.toPath(), current_file.toPath(), REPLACE_EXISTING);
		}//end for (files loop)
	}
	
	
	/*********************************************
	 * Handling bug implant.
	 * @param writer - Fiel writer.
	 * @param modifier - Method type modifier.
	 * @param class_name - Class name of method.
	 * @param method_name - Method name.
	 *********************************************/
	private static void plant_bug_switch(PrintWriter writer, String modifier, String class_name, String method_name){
		//declare vars
		String returned_val = "";
		String component_string = "" + '"' + class_name + "." + method_name + '"';
		
		//constructors are massy!
		if (modifier.equals("constructor"))
			return;
		
		//figure out what to plant
		switch(modifier.toLowerCase()){
		case "byte":
			returned_val = "0";
			break;
			
		case "int":
			returned_val = "0";
			break;
			
		case "integer":
			returned_val = "0";
			break;
			
		case "double":
			returned_val = "0.0";
			break;
			
		case "float":
			returned_val = "0";
			break;
			
		case "long":
			returned_val = "0";
			break;
			
		case "short":
			returned_val = "0";
			break;
		
		case "string":
			returned_val = "" + '"' + '"';
			break;
		
		case "char":
			returned_val = "'X'";
			break;
		
		case "void":
			returned_val = "";
			break;
			
		case "boolean":
			returned_val = "false";
			break;
		
		default: returned_val = "null";
		}
		
		//do the plant
		writer.println("boolean _bug_switch = Bug_Switcher.has_bug(" + component_string + ");");
		
		if (!modifier.equals("void") && !returned_val.equals("null"))
			writer.println(modifier + " _bug_returned_val = " + returned_val + ";");
	}
	
	
	/*************************************
	 * Plants the bug return command.
	 * @param writer - PrintWriter.
	 * @param modifier - Method modifier.
	 *************************************/
	private static void plant_bug_return(PrintWriter writer, String modifier){
		//constructors are massy. avoid them!
		if (modifier.equals("constructor"))
			return;
		
		//decide if modifier is supported
		boolean modif_supported = false;
		switch(modifier.toLowerCase()){
			case "byte":
				modif_supported = true;
				break;
				
			case "int":
				modif_supported = true;
				break;
				
			case "integer":
				modif_supported = true;
				break;
				
			case "double":
				modif_supported = true;
				break;
				
			case "float":
				modif_supported = true;
				break;
				
			case "long":
				modif_supported = true;
				break;
			
			case "short":
				modif_supported = true;
				break;
				
			case "string":
				modif_supported = true;
				break;
				
			case "char":
				modif_supported = true;
				break;
			
			case "void":
				modif_supported = true;
				break;
				
			case "boolean":
				modif_supported = true;
				break;  
				
			default: modif_supported = false;
		}
		
		//handle void
		if (modifier.equals("void")){
			writer.println("if (_bug_switch)");
			writer.println("\treturn;");
		}
		
		//hande unsupported
		else if (modif_supported == false){
			writer.println("if (_bug_switch)");
			writer.println("\treturn null;");
		}
		
		//handle supported
		else{
			writer.println("if (_bug_switch)");
			writer.println("\treturn _bug_returned_val;");
		}
	}
	
	
	/**************************************************
	 * Loads lexer with all classes and their methods.
	 * @param lexer - lexer.
	 **************************************************/
	private static void load_classes_to_lexer(Lexer lexer, String host_class){
		//declare vars
		Iterator<String> class_iter = Method_Parser.get_all_classes().iterator();
		Iterator<String> method_iter;
		String current_class;
		String current_method;
		
		//process
		while(class_iter.hasNext()){
			current_class = class_iter.next();
			method_iter = classes.get(current_class).iterator();
			
			//scan methods
			while(method_iter.hasNext()){
				current_method = method_iter.next();
				lexer.insert_method(current_class, current_method);
				
				//handle host class
				if (current_class.equals(host_class))
					lexer.insert_method(current_method);
			}//end while (methods)
			
			lexer.insert_class(current_class); //inserts the class name to lexer
		}//end while (classes)
	}
	
	
	/*****************************************************************************
	 * For debug.
	 * @throws IOException 
	 *****************************************************************************/
	public static void main(String[] args) throws IOException{
		Path source_path = FileSystems.getDefault().getPath("");
		FilesAssist.set_source_path(source_path);
		
		tag_methods(FilesAssist.get_all_java_files());
		
		//prints the methods list
//		print_all_methods();
	}
	
}
