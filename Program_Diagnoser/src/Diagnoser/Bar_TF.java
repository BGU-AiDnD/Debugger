package Diagnoser;

import java.util.LinkedList;

import Optim.GradientDescent;
import Optim.PSO;
import Optim.Target_Function;

public class Bar_TF extends Target_Function{
	private int[][] M_matrix;
	private int[][] skinny_M;
	private int[] e_vector;
	private int[] diagnosis;
	
	//compilation params
	private Object[] compilation;
	private boolean[] flip;
	
	/*******************************************
	 * Sets up the target functions parameters.
	 * @param M - M matrix.
	 * @param e - error vector.
	 * @param d - diagnosis.
	 *******************************************/
	public void setup(int[][] M, int[] e, int[] d){
		//set parameters
		M_matrix = M;
		e_vector = e;
		diagnosis = d;
		
		//compile
		compile();
	}
	
	
	/**************************
	 * Builds a skinny matrix.
	 **************************/
	private void build_skinny_M(){
		skinny_M = new int[e_vector.length][diagnosis.length];
		
		for(int row=0; row < e_vector.length; row++)
			for(int col=0; col < diagnosis.length; col++)
				if (M_matrix[row][diagnosis[col]] == 1)
					skinny_M[row][col] = 1;
				else skinny_M[row][col] = 0;
	}
	
	
// Old compute method:
//	/*********************************************************
//	 * Computes the value of the TF for the given parameters.
//	 * @param params - parameters.
//	 * @return value of TF .
//	 *********************************************************/
//	public double compute(double[] params) {
//		//sinusalize params vector
//		double[] params_tag = new double[params.length];
//		for(int i=0; i < params.length; i++)
//			params_tag[i] = (Math.sin(params[i]) + 1) / 2;
//		
//		//initialize vars
//		double result = 1;
//		double temp_calc = 1;
//		
//		//start process
//		for(int i=0; i < skinny_M.length; i++){
//			temp_calc = 1;
//			for(int j=0; j < skinny_M[0].length; j++){
//				if (skinny_M[i][j] == 1)
//					temp_calc = temp_calc * params_tag[j];
//			}//end inner for
//			
//			if (e_vector[i] == 1)
//				temp_calc = 1 - temp_calc;
//			
//			result = result * temp_calc;
//		}//end outer for
//		
//		return -result; //as a convention, optimizers are looking for minimum!
//	}
	
	
	/*******************
	 * Compiles the TF.
	 *******************/
	@SuppressWarnings("unchecked")
	private void compile() {
		//initialize compilation
		compilation = new Object[M_matrix.length];
		for(int i=0; i < compilation.length; i++)
			compilation[i] = new LinkedList<Integer>();
		
		flip = new boolean[M_matrix.length];
		
		//build skinny M
		build_skinny_M();
		
		//process skinny M
		for(int i=0; i < skinny_M.length; i++){
			for(int j=0; j < skinny_M[0].length; j++){
				if (skinny_M[i][j] == 1)
					((LinkedList<Integer>) compilation[i]).add(j);
			}//end inner for
			
			if (e_vector[i] == 1)
				flip[i] = true;
		}//end outer for
	}
	
	
	/*********************************************************
	 * Computes the value of the TF for the given parameters.
	 * @param params - parameters.
	 * @return value of TF .
	 *********************************************************/
	@SuppressWarnings("unchecked")
	public double compute(double[] params){
		//initialize
		double result = 1;
		double temp = 1;
		
		//interpret compilation
		for(int i=0; i < compilation.length; i++){
			
			temp = 1;
			for(int j : (LinkedList<Integer>) compilation[i])
				temp *= params[j]; 
			
			if (flip[i])
				temp = 1 - temp;
			
			result *= temp;
		}//end for
		
		//wrap
		return -result; //as a convention, optimizers are looking for minimum!
	}
	

	/*****************
	 * Clones the TF.
	 *****************/
	public Target_Function clone() {
		return new Bar_TF();
	}
	
	
	/*************************************************************************************
	 ********************************* For debug *****************************************
	 *************************************************************************************/
	public static void main(String[] args){
		//simulate spectrum
		int[][] M = {{1,1,1,0},
		 		 	 {0,0,0,1},
				 	 {1,0,1,0},
				 	 {1,1,1,1}};
	
		int[] e = {0,0,1,0};
		
		//simulate diagnose
		int[] diagnose = {0};
		
		//ready target function
		Bar_TF TF = new Bar_TF();
		TF.setup(M,e,diagnose);
		
		//deduce dimensions
		int dim = diagnose.length;
		
		//run PSO
		PSO pso = new PSO(dim, TF);
		pso.run();
		
		//run Gradient Descent (for comparison)
		GradientDescent GD = new GradientDescent(TF, dim);
		double[] x = GD.run();
		
		//print results for comparison
		System.out.println("PSO: " + -TF.compute(pso.get_gbest()));
		System.out.println("GD : " + -TF.compute(x));
	}

}
