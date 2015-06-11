package Diagnoser;
import Implant.*;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;

import Deprecated.PSO;
import GD.GradientDescent;


@SuppressWarnings("unused")
public class Barinel {
	private TreeSet<Diagnosis> diagnoses;
	//private Linked_List d_probs; //diagnoses probabilities
	private int[][] M_matrix; //spectrum matrix
	private int[] e_vector; //error vector
	private Dynamic_Spectrum ds;
	
	public double[] prior_probs;
	public static double prior_p = 0.05; //apriory probability for single component (original: 0.1)
	public static int GD_calls = 0; //for debug
	
	/********************
	 * Lite Constructor.
	 ********************/
	public Barinel(){
		M_matrix = null;
		e_vector = null;
		ds = null;
		prior_probs = null;
		diagnoses = new TreeSet<Diagnosis>();
	}
	
	
	/****************************
	 * Constructor + Load.
	 * @param M - M matrix.
	 * @param e - error vector.
	 ****************************/
	public Barinel(int[][] M, int[] e){
		M_matrix = M;
		e_vector = e;
		ds = null;
		diagnoses = new TreeSet<Diagnosis>();
		prior_probs = null;
	}
	
	
	/****************************
	 * Constructor + Load.
	 * @param M - M matrix.
	 * @param e - error vector.
	 ****************************/
	public Barinel(Dynamic_Spectrum ds){
		M_matrix = null;
		e_vector = null;
		this.ds = ds;
		diagnoses = new TreeSet<Diagnosis>();
		prior_probs = null;
	}
	
	
	/*********************************************
	 * (non-uniform) comps probabilities setter.
	 * @param probs - comps. probabilities 
	 *********************************************/
	public void set_prior_probs(double[] probs){
Logger.log("Barinel.set_prior_probs");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.set_prior_probs");
if (_bug_switch)
	return;

		prior_probs = probs;
	}
	
	
	/*****************************************
	 * loads Barinel with spectrum knowledge.
	 * @param M - M matrix.
	 * @param e - error vector.
	 *****************************************/
	public void load(int[][] M, int[] e){
Logger.log("Barinel.load");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.load");
if (_bug_switch)
	return;

		M_matrix = M;
		e_vector = e;
	}
	
	
	/***********************************************
	 * Loads spectrum matrix from file with header.
	 * @param file - CSV file containing a header.
	 * @throws FileNotFoundException
	 ***********************************************/
	public void load_file_with_header(File file) throws FileNotFoundException{
Logger.log("Barinel.load_file_with_header");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.load_file_with_header");
if (_bug_switch)
	return;

		Dynamic_Spectrum ds = new Dynamic_Spectrum();
		ds.load_file_with_header(file);
		this.ds  = ds;
	}
	
	
	/*****************************************
	 * Computes prior non-uniform probabiity.
	 * @param diag - Diagnosis.
	 * @return prior non-uniform probabiity.
	 *****************************************/
	private double non_uniform_prior(Diagnosis diag){
Logger.log("Barinel.non_uniform_prior");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.non_uniform_prior");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		int[] comps = diag.get_diag();
		double prob = 1;
		
		for(int i=0; i < comps.length; i++)
			prob *= this.prior_probs[comps[i]];
		
		return prob;
	}
	
	
	/**************************************
	 * Calculates diagnoses probabilities.
	 **************************************/
	private void generate_probs(){
Logger.log("Barinel.generate_probs");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.generate_probs");
if (_bug_switch)
	return;

		//for debug
		GD_calls++;
		
		//declare vars
		//double[] temp_probs = new double[diagnoses.size()];
		TreeSet<Diagnosis> new_set = new TreeSet<Diagnosis>();
		Diagnosis temp_diagnosis;
		double probs_sum = 0;
		int dim;
		Bar_TF TF;
		
		//start process
		Iterator<Diagnosis> iterator = diagnoses.iterator();
		while(iterator.hasNext()){
			temp_diagnosis = iterator.next();
			
			//setup target function
			TF = new Bar_TF();
			if (ds == null)
				TF.setup(M_matrix,e_vector,temp_diagnosis.get_diag());
			else
				TF.setup(ds.M,ds.e,temp_diagnosis.get_diag());
			
			dim = temp_diagnosis.get_diag().length; //deduce dimensions
			
			//run Gradient Descent 
//			GradientDescent GD = new GradientDescent(TF, dim);
//			double[] x = GD.run();
//			double e_dk = -TF.compute(x);
//			double dk;
			
			//run pso
			PSO pso = new PSO(dim, TF);
			pso.run();
			double[] x = pso.get_gbest();
			double e_dk = -TF.compute(x);
			double dk;
			
			if (prior_probs == null)
				dk = Math.pow(prior_p,temp_diagnosis.get_diag().length); //assuming same prior prob. for every component.
			
			else dk = non_uniform_prior(temp_diagnosis);
			
			temp_diagnosis.set_prob(e_dk * dk); //temporary probability
			
			//update probabilities sum
			probs_sum += temp_diagnosis.get_prob();
			
			//decode if dynamic spectrum was used
			if (ds != null)
				temp_diagnosis.set_diag(ds.decode_diag(temp_diagnosis.get_diag()));
			
			//save h probabilities
			temp_diagnosis.set_h_list(x);
			
		}//end while
		
		//normalize probabilities (and order them)
		iterator = diagnoses.iterator();
		while(iterator.hasNext()){
			temp_diagnosis = iterator.next();
			temp_diagnosis.set_prob(temp_diagnosis.get_prob() / probs_sum);
			
			new_set.add(temp_diagnosis);
		}//end while
		
		diagnoses = new_set;
	}
	
	
	/****************
	 * Runs Barinel.
	 ****************/
	public TreeSet<Diagnosis> run(){
Logger.log("Barinel.run");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.run");
if (_bug_switch)
	return null;

		//generate diagnoses using STACCATO
		LinkedList<int[]> diags;
		if (ds == null)
			diags = Staccato.run(M_matrix, e_vector);
		else
			diags = Staccato.run(ds);
		
		//enhance diagnoses list to accommodate probabilities
		Iterator<int[]> iterator = diags.iterator();
		while(iterator.hasNext())
			diagnoses.add(new Diagnosis(iterator.next()));
		
		//generate probabilities
		generate_probs();
		
		return diagnoses;
	}
	
	
	/***************************
	 * Prints diagnosis report.
	 ***************************/
	public void print_report(){
Logger.log("Barinel.print_report");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.print_report");
if (_bug_switch)
	return;

		//declare vars
		Iterator<Diagnosis> iterator = diagnoses.descendingIterator();
		Diagnosis temp_diagnosis;
		int i = 1;
		
		//start process
		while(iterator.hasNext()){
			temp_diagnosis = iterator.next();
			System.out.print(i + ") Diagnosis: ");
			System.out.print(temp_diagnosis.toString());
			System.out.print(", Probability: " + temp_diagnosis.get_prob());
			System.out.println("");
			
			i++;
		}//end while
	}
	
	
	/***********************************************************************
	 * Exports the saved diagnoses into a CSV file.
	 * @param file_name - File name (stating the ending is not obligatory).
	 * @throws IOException
	 ***********************************************************************/
	public void export_diags_to_csv(String file_name) throws IOException{
Logger.log("Barinel.export_diags_to_csv");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.export_diags_to_csv");
if (_bug_switch)
	return;

		//handle file
		file_name.replace(".csv", "");
		file_name += ".csv";
		File file = new File(file_name);
		if (!file.exists())
			file.createNewFile();
		
		//get ready
		PrintWriter writer = new PrintWriter(file);
		Iterator<Diagnosis> iterator = diagnoses.descendingIterator();
		Diagnosis current_diag;
		int[] current_array;
		
		//process
		while(iterator.hasNext()){
			current_diag = iterator.next();
			current_array = current_diag.get_diag();
			for(int i=0; i < current_array.length; i++)
				writer.print(current_array[i] + ",");
			
			//write probability
			writer.print("P," + current_diag.get_prob());
			writer.println();
		}//end while
		
		//wrap
		writer.close();
	}
	
	
	/***********************************************************************************
	 ***************************************For debug***********************************
	 ***********************************************************************************/
	public static void main(String[] args){
Logger.log("Barinel.main");
boolean _bug_switch = Bug_Switcher.has_bug("Barinel.main");
if (_bug_switch)
	return;

		//simulate spectrum
//		int[][] M = {{1,1,0},
//		 		 	 {0,1,1},
//				 	 {1,0,1},
//				 	 {1,0,1}};
//	
//		int[] e = {1,1,1,0};
		
		
		//setup Barinel
//		Barinel barinel = new Barinel(M,e);
//		barinel.run();
//		barinel.print_report();
		
		Barinel barinel = new Barinel();
		try {
			barinel.load_file_with_header(new File("result_matrix.csv"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch bloc			e.printStackTrace();
		}
		
		barinel.run();
		barinel.print_report();
	}
}
