package Diagnoser;
import Implant.*;


import Deprecated.PSO;
import GD.GradientDescent;
import GD.Target_Function;

public class Bar_TF extends Target_Function{
	private static int[][] M_matrix;
	private static int[][] skinny_M;
	private static int[] e_vector;
	//private static int[] diagnose;
	
	/*******************************************
	 * Sets up the target functions parameters.
	 * @param M - M matrix.
	 * @param e - error vector.
	 * @param d - diagnose.
	 *******************************************/
	public void setup(int[][] M, int[] e, int[] d){
Logger.log("Bar_TF.setup");
boolean _bug_switch = Bug_Switcher.has_bug("Bar_TF.setup");
if (_bug_switch)
	return;

		//set parameters
		M_matrix = M;
		e_vector = e;
		//diagnose = d;
		
		//build skinny M
		skinny_M = new int[e.length][d.length];
		
		for(int row=0; row < e.length; row++)
			for(int col=0; col < d.length; col++)
				if (M_matrix[row][d[col]] == 1)
					skinny_M[row][col] = 1;
				else skinny_M[row][col] = 0;
			
	}
	
	
	/*********************************************************
	 * Computes the value of the TF for the given parameters.
	 * @param params - parameters.
	 * @return value of TF .
	 *********************************************************/
	public double compute(double[] params) {
Logger.log("Bar_TF.compute");
boolean _bug_switch = Bug_Switcher.has_bug("Bar_TF.compute");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		//sinusalize params vector
		double[] params_tag = new double[params.length];
		for(int i=0; i < params.length; i++)
			params_tag[i] = (Math.sin(params[i]) + 1) / 2;
		
		//initialize vars
		double result = 1;
		double temp_calc = 1;
		
		//start process
		for(int i=0; i < skinny_M.length; i++){
			temp_calc = 1;
			for(int j=0; j < skinny_M[0].length; j++){
				if (skinny_M[i][j] == 1)
					temp_calc = temp_calc * params_tag[j];
			}//end inner for
			
			if (e_vector[i] == 1)
				temp_calc = 1 - temp_calc;
			
			result = result * temp_calc;
		}//end outer for
		
		return -result; //both PSO and GD are looking for minimum!
	}
	

	/*****************
	 * Clones the TF.
	 *****************/
	public Target_Function clone() {
Logger.log("Bar_TF.clone");
boolean _bug_switch = Bug_Switcher.has_bug("Bar_TF.clone");
if (_bug_switch)
	return null;

		return new Bar_TF();
	}
	
	
	/*************************************************************************************
	 ********************************* For debug *****************************************
	 *************************************************************************************/
	public static void main(String[] args){
Logger.log("Bar_TF.main");
boolean _bug_switch = Bug_Switcher.has_bug("Bar_TF.main");
if (_bug_switch)
	return;

		//simulate spectrum
		int[][] M = {{1},
		 		 	 {1},
				 	 {1},
				 	 {1}};
	
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
