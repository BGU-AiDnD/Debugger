package Optim;

///////////////////////////////////////////////////////////////////////////
////
//Program file name: Minimum.java                                       //
////
//© Tao Pang 2006                                                       //
////
//Last modified: April 17, 2012                                         //
////
//(1) This Java program is part of the book, "An Introduction to        //
//Computational Physics, 2nd Edition," written by Tao Pang and      //
//published by Cambridge University Press on January 19, 2006.      //
////
//(2) No warranties, express or implied, are made for this program.     //
////
///////////////////////////////////////////////////////////////////////////

//An example of searching a minimum of a multivariable
//function through the steepest-descent method.
public class GradientDescent {
	int dim;
	private double del; 
	private double a;
	private Diagnoser.Bar_TF TF; 
	
	
	/*******************************
	 * Constructor.
	 * @param TF - Target Function.
	 *******************************/
	public GradientDescent(Diagnoser.Bar_TF TF, int dim){
		del = 1e-6; //original: 1e-6
		a = 0.5; //original: 0.5
		this.dim = dim; 
		this.TF = TF;
	}
	
	
	/*************************
	 * Runs the GD algorithm.
	 *************************/
	public double[] run() {
		double[] x = new double[dim];
		
		//initialize 1st solution
		for(int i=0; i < x.length; i++)
			x[i] = 0.5; //Math.PI / 6;
		
		return steepestDescent(x);
	}

	//Method to carry out the steepest-descent search.
	public double[] steepestDescent(double[] x) {
		int n = x.length;
		double h = 1e-6;
		double g0 = g(x);
		double fi[] = new double[n];
		
		fi = f(x, h);
		double dg = 0;
		
		for (int i=0; i < n; i++) 
			dg += fi[i]*fi[i];
		
		dg = Math.sqrt(dg);
		
		double b = a/dg;
		while (dg > del) {
			for (int i=0; i<n; ++i) 
				x[i] -= b*fi[i];
			
			h /= 2;
			fi = f(x, h);
			dg = 0;
			
			for (int i=0; i < n; ++i) 
				dg += fi[i]*fi[i];
			
			dg = Math.sqrt(dg);
			b  = a/dg;
			
			double g1 = g(x);
			if (g1 > g0) 
				a /= 2;
			else g0 = g1;
		}
		
		return x;
	}

	//Method to provide function f = gradient g(x).
	public double[] f(double[] x, double h) {
		int n = x.length;
		double z[] = new double[n];
		double g0 = g(x);
		
		
		double y[] = (double[]) x.clone();
		for (int i=0; i < n; ++i) {	
			y[i] += h;
			z[i] = (g(y)-g0)/h;
		}
		return z;
	}

	//Method to provide function g(x).
	public double g(double[] x) {
		return TF.compute(x); 
	}
	
	
	///////////////////////For Debug/////////////////////////////////
	public static void main(String[] args){
		//new GradientDescent().run();
	}
}
