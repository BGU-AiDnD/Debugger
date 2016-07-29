package Diagnoser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

import Infrastrcture.Linked_List;

public class Dynamic_Spectrum {
	public int[][] M;
	public int[] e;
	private Hashtable<Integer,Integer> coder;
	public Hashtable<Integer, Integer> getCoder() {
		return coder;
	}


	private Hashtable<Integer,Integer> decoder;
	private int indexer;
	
	
	public Hashtable<Integer, Integer> getDecoder() {
		return decoder;
	}


	public int getIndexer() {
		return indexer;
	}


	/***************
	 * Constructor.
	 ***************/
	public Dynamic_Spectrum(){
		coder = new Hashtable<Integer,Integer>();
		decoder = new Hashtable<Integer,Integer>();
		indexer = 0;
		
		M = new int[1][1];
		M[0][0] = 0;
		
		e = new int[1];
		e[0] = 0;
		
		file_comp(0);
	}
	
	
	/****************************
	 * Private constructor.
	 * @param M - M matrix.
	 * @param e - error vector.
	 ****************************/
	@SuppressWarnings("unchecked")
	private Dynamic_Spectrum(int[][] M, int[] e, 
			Hashtable<Integer,Integer> coder, Hashtable<Integer,Integer> decoder, int indexer){
		
		this.M = new int[M.length][1];
		this.e = e.clone();
		this.indexer = indexer;
		this.coder = (Hashtable<Integer,Integer>)coder.clone();
		this.decoder = (Hashtable<Integer,Integer>)decoder.clone();

		//clone
		for(int i=0; i < M.length; i++)
			this.M[i] = M[i];
		
	}
	
	
	/***********************
	 * Clones the spectrum.
	 ***********************/
	public Dynamic_Spectrum clone(){
		return new Dynamic_Spectrum(M, e, coder, decoder, indexer);
	}
	
	
	/**************************************
	 * Files a component in the converter.
	 * @param comp - Component.
	 * @return the code of the component.
	 **************************************/
	private int file_comp(int comp){
		coder.put(comp, indexer);
		decoder.put(indexer, comp);
		indexer++;
		return (indexer - 1);
	}
	
	
	/*****************************************************
	 * Parses and files all components of a test.
	 * Also, return the number of newly seen components.
	 * @param test - Test.
	 * @return Number of newly seen components.
	 *****************************************************/
	private int parse_test(int[] test){
		//initialize
		int new_num = 0; 
		
		//process
		for(int i=0; i < test.length; i++)
			if (!coder.containsKey(test[i])){
				file_comp(test[i]);
				new_num++;
			}
		
		//wrap
		return new_num;
	}
	
	
	/*********************************************************
	 * Makes a new row for the spectrum, based on given test.
	 * @param test - Test.
	 * @param new_num - Newly seen components number.
	 * @return new row based on given test.
	 *********************************************************/
	private int[] make_new_row(int[] test, int new_num){
		//initialize
		int[] new_row = new int[M[0].length + new_num];
		for(int i=0; i < new_row.length; i++)
			new_row[i] = 0;
		
		//process
		try{
		for(int i=0; i < test.length; i++)
			new_row[coder.get(test[i])] = 1;
		}
		catch(Exception e){
			System.out.println("bummer");
		}
		//wrap
		return new_row;
	}
	
	
	/********************************
	 * Updates the dynamic spectrum.
	 * @param test - Test trace.
	 * @param e_val - Error value.
	 ********************************/
	public void update(int[] test, int e_val){
		//get ready
		int new_num = parse_test(test); //newly seen components
		int[] new_row = make_new_row(test, new_num);
		
		//initialize new matrix
		int[][] new_M = new int[M.length + 1][new_row.length];
		for(int r=0; r < new_M.length; r++)
			for(int c=0; c < new_M[0].length; c++)
				new_M[r][c] = 0;
		
		//copy old rows
		for(int r=0; r < M.length; r++)
			for(int c=0; c < M[r].length; c++)
				new_M[r][c] = M[r][c];
		
		//update new row
		int last_r = new_M.length - 1;
		new_M[last_r] = new_row;
		
		//update e
		int[] new_e = new int[e.length + 1];
		for(int i=0; i < e.length; i++)
			new_e[i] = e[i];
		new_e[new_e.length - 1] = e_val;
		
		//wrap
		M = new_M;
		e = new_e;
	}
		
	
	/*****************************************************
	 * Decodes a diagnosis made for the dynamic spectrum.
	 * @param diag - Diagnosis.
	 * @return the diagnosis, decoded.
	 *****************************************************/
	public int[] decode_diag(int[] diag){
		//initialize
		int[] result = new int[diag.length];
		
		//process
		for(int i=0; i < diag.length; i++)
			result[i] = decoder.get(diag[i]);
		
		//wrap
		return result;
	}
	
	
	/***********************************************
	 * Decodes a component.
	 * @param comp - Component code-index.
	 * @return the original index of the component.
	 ***********************************************/
	public int decode_comp(int comp){
		return decoder.get(comp);
	}
	
	
	/********************************
	 * Decodes a batch of diagnoses.
	 * @param diags - Diagnoses.
	 * @return the batch, decoded.
	 ********************************/
	public LinkedList<int[]> decode_diags(LinkedList<int[]> diags){
		//initialize
		LinkedList<int[]> result = new LinkedList<int[]>();
		int[] temp_diag;
		
		//process
		Iterator<int[]> iterator = diags.iterator();
		while(iterator.hasNext()){
			temp_diag = decode_diag(iterator.next());
			result.add(temp_diag);
		}
		
		//wrap
		return result;
	}
	
	
	/****************************************************************
	 * Loads a pectrum table from file with a header.
	 * @param file - CSV file contains spectrum matrix, with header.
	 * @throws FileNotFoundException
	 ****************************************************************/
	public void load_file_with_header(File file) throws FileNotFoundException{
		//get ready
		Scanner scanner = new Scanner(new BufferedReader(new FileReader(file)));
		int comps_num = 0;
		int tests_num = 0;
		int row = 0;
		
		//parse header
		String header_flat = scanner.nextLine();
		String[] header_columns = header_flat.split(",");
		Hashtable<Integer,Double> header = new Hashtable<Integer, Double>();
		
		for(int i=0; i < header_columns.length ; i++) {
			header.put(i, Double.parseDouble(header_columns[i]));
			comps_num ++;
		}
		
		
		//parse rest of rows
		String row_flat;
		String[] row_data;
		Linked_List list;
		int temp_e = 0;
		
		while(scanner.hasNextLine()) {
			row_flat = scanner.nextLine();
			tests_num++;
			row_data = row_flat.split(",");
			list = new Linked_List();
			
			for(int i=0; i < row_data.length; i++){
				if (i < row_data.length - 1 && row_data[i].equals("1"))
					list.add_val(i);
				
				if (i == row_data.length - 1){
					temp_e = Integer.parseInt(row_data[i]);
				}//end if
				
			}//end for	
	
			//ignore dummy row
			if (list.get_length() > 0)
				update(list.to_int_array(), temp_e);
			
		}//end while
		
		//wrap
		scanner.close();
	}
	
	
	/*********************************************************************************
	 ******************************* For Debug 
	 * @throws FileNotFoundException ***************************************
	 *********************************************************************************/
	public static void main(String[] args) throws FileNotFoundException{
		Dynamic_Spectrum ds = new Dynamic_Spectrum();
		ds.load_file_with_header(new File("result_matrix.csv"));
		System.out.println("finished!");
	}
}
