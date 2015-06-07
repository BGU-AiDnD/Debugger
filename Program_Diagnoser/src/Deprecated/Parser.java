package Deprecated;

import java.io.*;
import java.util.Scanner;

import Deprecated.DDIC;
import Deprecated.Event;
import Deprecated.Event_Handler;
import Deprecated.Lexer;
import Parsing.Method_Parser;

public class Parser {
    
	
	/*************************************************
	 * Finds and tags all methods in the source code.
	 * @param file_names - names of the files.
	 *************************************************/
	private static void tag_methods(File[] files){
		try {
			Method_Parser.tag_methods(files);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	
	/*******************************************
	 * Generates call graph out of source code.
	 * @throws IOException
	 *******************************************/
	private static void generate_graph(Lexer lexer, Process_Graph graph) throws IOException {
        Event event;
        Event_Handler.load_graph_seed(graph);
    	Scanner scanner = null;
		

		
		try {
            scanner = new Scanner(new BufferedReader(new FileReader("Method_Organizer.java")));
            scanner.useDelimiter("");

            String temp;
            while (scanner.hasNext()) {
            	temp = scanner.next();
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
            		
            	}
            	System.out.println(temp);
            	event = lexer.next(temp);
            	if(event != null)
            		Event_Handler.raise_event(event);
            }//end while
            
        } finally {
            if (scanner != null)
                scanner.close();
        	
        }//end finally
    }//end generate graph
	
	/*******************************************************************************
	 ************************************For Debug**********************************
	 *******************************************************************************/
	public static void main(String[] args){
    	//find and tag methods
        File[] files = {new File("Event_Handler.java")};
        tag_methods(files);
        
    	//declare vars
		Process_Graph graph = new Process_Graph("some method");
    	Lexer lexer = new Lexer();
    	
        //LOAD LEXER with syntax rules
        DDIC.load_data(lexer);
        
        //load LEXER with methods names (!!!syntactically for debugging!!!)
        lexer.insert_method("ifunction1");
        lexer.insert_method("ifunction2");
        lexer.insert_method("ifunction3");
        
        //generate call graph
        try {
			generate_graph(lexer, graph);
		} catch (IOException e) {
			e.printStackTrace();
		}
        
		//print resulted graph
		System.out.println();
       // graph.print_graph();
        graph.sample_route();
    	
	}
}