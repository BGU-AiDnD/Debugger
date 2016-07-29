package Diagnoser;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;
import java.util.HashMap;

import Optim.GradientDescent;
import Optim.LightPSO;
import Optim.PSO;


public class Barinel {
	public enum optim_technique {PSO, GD, LightPSO};
	
	private TreeSet<Diagnosis> diagnoses;
	//private Linked_List d_probs; //diagnoses probabilities
	private int[][] M_matrix; //spectrum matrix
	private int[] e_vector; //error vector
	private Dynamic_Spectrum ds;
	private optim_technique optim_t = optim_technique.LightPSO;
	private Staccato staccato;
	
	public double[] prior_probs;
	public static final double prior_p = 0.05; //apriory probability for single component (original: 0.1)
	
	/********************
	 * Lite Constructor.
	 ********************/
	public Barinel(){
		M_matrix = null;
		e_vector = null;
		ds = null;
		prior_probs = null;
		diagnoses = new TreeSet<Diagnosis>();
		
		staccato = new Staccato();
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
		
		staccato = new Staccato();
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
		
		staccato = new Staccato();
	}
	
	
	/**********************************************
	 * Optimization technique setter.
	 * @param t - Alias of optimization technique.
	 **********************************************/
	public void set_optim_technique(optim_technique t){
		optim_t = t;
	}
	
	
	/*********************************************
	 * (non-uniform) comps probabilities setter.
	 * @param probs - comps. probabilities 
	 *********************************************/
	public void set_prior_probs(double[] probs){
		prior_probs = probs;
	}
	
	
	/*****************************************
	 * loads Barinel with spectrum knowledge.
	 * @param M - M matrix.
	 * @param e - error vector.
	 *****************************************/
	public void load(int[][] M, int[] e){
		M_matrix = M;
		e_vector = e;
	}
	
	
	/***********************************************
	 * Loads spectrum matrix from file with header.
	 * @param file - CSV file containing a header.
	 * @throws FileNotFoundException
	 ***********************************************/
	public void load_file_with_header(File file) throws FileNotFoundException{
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
		//declare vars
		//double[] temp_probs = new double[diagnoses.size()];
		TreeSet<Diagnosis> new_set = new TreeSet<Diagnosis>();
		double probs_sum = 0;
		int dim;
		Bar_TF TF;
		
		//start process
		for(Diagnosis temp_diagnosis : diagnoses){
			//setup target function
			TF = new Bar_TF();
			if (ds == null)
				TF.setup(M_matrix,e_vector,temp_diagnosis.get_diag());
			else
				TF.setup(ds.M,ds.e,temp_diagnosis.get_diag());
			
			dim = temp_diagnosis.get_diag().length; //deduce dimensions
			
			//optimize according to designated tehnique
			double[] x = null;
			double e_dk = 0.0;
			double dk = 0.0;
			
			switch(optim_t){
				case GD: //run Gradient Descent
					GradientDescent GD = new GradientDescent(TF, dim);
					x = GD.run();
					e_dk = -TF.compute(x);
					break;
				
				case PSO: //run Partical Swarm Optimization
					PSO pso = new PSO(dim, TF);
					pso.run();
					x = pso.get_gbest();
					e_dk = -TF.compute(x);
					break;
					
				case LightPSO:
					LightPSO LPSO = new LightPSO(dim, TF);
					x = LPSO.run();
					e_dk = -TF.compute(x);
			}
	
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
		double temp_prob;
		DecimalFormat df = new DecimalFormat("##.##");
		for(Diagnosis temp_diagnosis : diagnoses){
			//normalize
			temp_prob = temp_diagnosis.get_prob() / probs_sum;
			
			//round
			temp_prob = Double.parseDouble(df.format(temp_prob));
			
			//set
			temp_diagnosis.set_prob(temp_prob);
			
			new_set.add(temp_diagnosis);
		}//end while
		
		diagnoses = new_set;
	}
	
	
	/****************
	 * Runs Barinel.
	 ****************/
	public TreeSet<Diagnosis> run(){
		//initialize
		diagnoses = new TreeSet<Diagnosis>();
		
		//generate diagnoses using STACCATO
		LinkedList<int[]> diags;
		if (ds == null)
			diags = staccato.run(M_matrix, e_vector);
		else
			diags = staccato.run(ds);
		
		//enhance diagnoses list to accommodate probabilities
		for(int[] diag : diags)
			diagnoses.add(new Diagnosis(diag));
		
		//generate probabilities
		generate_probs();
		
		return diagnoses;
	}
	
	
	/***************************
	 * Prints diagnosis report.
	 ***************************/
	public void print_report(){
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
	
	public static void export_diags_to_csv_findings_order(LinkedList<int[]> diags, String file_name) throws IOException {
		
	}
	/***********************************************************************************
	 ***************************************For debug***********************************
	 ***********************************************************************************/
	public static void main(String[] args){
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
			e.printStackTrace();
		}
		
		//run BD
		barinel.set_optim_technique(optim_technique.GD);
		barinel.run();
		System.out.println("GD Results:");
		barinel.print_report();
		
		//run PSO
		barinel.set_optim_technique(optim_technique.PSO);
		barinel.run();
		System.out.println("\nPSO Results:");
		barinel.print_report();
		
		//run Light PSO
		barinel.set_optim_technique(optim_technique.LightPSO);
		barinel.run();
		System.out.println("\nLight PSO Results:");
		barinel.print_report();
	}
}
