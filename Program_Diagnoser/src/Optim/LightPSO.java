package Optim;

import java.util.concurrent.ThreadLocalRandom;

public class LightPSO {
	//declare parameters
	private int iterations = 10; //No. of iterations //30
	int iteration;
	
	//search space related parameters
	private int dim; //dimensions No.
	final public double max_b = 1; //4 * Math.PI; //maximum boundary
	final public double min_b = 0; //minimum boundary
	
	//particles
	public int p_num = 20; //30
	private double[][] position_matrix;
	private double[][] velocity_matrix;
	
	//weights constants
	private double inertia_w = 0.2;
	private double gbest_w = 1;
	private double pbest_w = 0.3;
	
	//values storage
	double[] gbest; //glbal best coordinates
	double[][] pbest; //particle's best coordinates
	double[] pbest_val;
	double gbest_val;
	
	//target function
	Target_Function TF;
	
	
	/***********************************
	 * Constructor.
	 * @param p_num - Particles number.
	 * @param dim - Dimensions number.
	 ***********************************/
	public LightPSO(int dim, Target_Function TF){
		this.dim = dim;
		this.TF = TF;
		
		//construct the particles matrices
		position_matrix = new double[p_num][1];
		velocity_matrix = new double[p_num][1];
		
		//construct the values holders
		pbest = new double[p_num][1];
		gbest = new double[dim];
		pbest_val = new double[p_num];
		
		for(int p=0; p < p_num; p++){
			position_matrix[p] = new double[dim];
			velocity_matrix[p] = new double[dim];
			pbest[p] = new double[dim];
		}
	}
	
	
	/************************************************************
	 * Randomizes content of the position and velocity matrices.
	 * Also, finds the initial best value and its coordinates.
	 ************************************************************/
	private void initialize(){
		//declare vars
		double[] velocity;
		double[] position;
		double interval = max_b - min_b;
		
		//initialize vals holders
		gbest = new double[dim];
		pbest = new double[p_num][dim];
		
		//scan all particles
		for(int p=0; p < p_num; p++){
			
			//create new records
			velocity = new double[dim];
			position = new double[dim];
			
			//scan dimensions
			for(int d=0; d < dim; d++){
				//randomize location (make sure within boundaries)
				position[d] = min_b + Math.random() * interval;
				
				//randomize velocity
				velocity[d] = min_b + Math.random() * interval;	
			}
			//update matrices
			position_matrix[p] = position;
			velocity_matrix[p] = velocity;
			pbest[p] = position.clone();
			pbest_val[p] = TF.compute(position);
		}//end for (particles)
		
		//update global best value and coordinates
		find_gbest(); 
	}
	
	
	/***************************************************************
	 * Finds the global best value and coordinates.
	 * PSO tries to find the MINIMIUM value of the target function!
	 ***************************************************************/
	private void find_gbest(){
		//get ready
		gbest = position_matrix[0];
		gbest_val = TF.compute(position_matrix[0]);
		double current_val;
		
		//scan all particles
		for (int p=1; p < p_num; p++){
			current_val = TF.compute(position_matrix[p]);
			if (current_val < gbest_val){
				gbest = position_matrix[p];
				gbest_val = current_val;
			}
		}//end for
	}
	
	
	/***********************
	 * Moves the particles.
	 ***********************/
	private void move_particles(){
		for(int p=0; p < p_num; p++)
			move_particle(p);
	}
	
	
	/*****************************
	 * Moves a single particle.
	 * @param p - particle index.
	 *****************************/
	private void move_particle(int p){
		//raffle random factor
		double random_factor = ThreadLocalRandom.current().nextDouble();
		
		//move
		for(int d=0; d < dim; d++){
			position_matrix[p][d] += velocity_matrix[p][d];
			if (position_matrix[p][d] > max_b){
				position_matrix[p][d] = max_b;
				velocity_matrix[p][d] = 0;  //stop in this direction!
			}
			else if (position_matrix[p][d] < min_b){
				position_matrix[p][d] = min_b;
				velocity_matrix[p][d] = 0; //stop in this direction!
			}
		}//end for (dimensions)
		
		//update pbest
		double temp_val = TF.compute(position_matrix[p]);
		if (temp_val < pbest_val[p]){
			pbest[p] = position_matrix[p].clone();
			pbest_val[p] = temp_val;
		}
		
		//update gbest
		if (temp_val < gbest_val){
			gbest_val = temp_val;
			gbest = position_matrix[p].clone();
		}
		
		//update velocity
		update_velocity(p, random_factor);
	}
	
	
	/*********************************
	 * Updates a particle's velocity.
	 * @param p - Particle index.
	 *********************************/
	private void update_velocity(int p, double randfactor){
		//declare vars
		double rand_factor = 1;
		
		//calculate vectors
		double[] pb_vector = new double[dim];
		double[] gb_vector = new double[dim];
		
		//insert randomness (wobbling)
		if(iteration == 3 || iteration == 6 || iteration == 9 || iteration % 3 == 0)
			rand_factor = randfactor;
		else rand_factor = 1;
		
		for(int d=0; d < dim; d++){
			pb_vector[d] = pbest[p][d] - position_matrix[p][d];
			gb_vector[d] = gbest[d] - position_matrix[p][d];
			
			//update velocity component
			velocity_matrix[p][d] = (inertia_w * velocity_matrix[p][d] + gbest_w * gb_vector[d] * rand_factor + 
					pbest_w * pb_vector[d]);
		}	
	}
	
	
	/***************************************************************************
	 * Runs the PSO algorithm to find a solution for the given target function.
	 * PSO is set to fund the MINIMUM value of the target function.
	 * @return an array representing the coordinates of the solution.
	 ***************************************************************************/
	public double[] run(){	
		//initialize velocity and position of particles
		//also, finds the initial global best value and its coordinates
		initialize();
		
		//process
		for(int iteration=0; iteration < iterations; iteration++)
			move_particles();
		
		//wrap
		return gbest;
	}
	
}
