package Optim;

import java.util.Random;

public class Particle {
	
	private int d;  //number of dimensions
	private double[] position;
	private double[] velocity; 
	private double[] pbest; //best position found by this particle
	private double pbest_val;
	private int group; //for multigrouped PSO
	
	private Random generator = new Random();
	
	/************************************************
	 * Updates particle velocity.
	 * @param gbest - The global best position found.
	 * @param inertia_w - Weight of inertia.
	 * @param gbest_w - Weight of gbest direction.
	 * @param pbest - Weight of pbest direction.
	 ************************************************/
	public synchronized void update_velocity(int it, double[] gbest, double inertia_w, double gbest_w, double pbest_w){
	
			
		//calculate vectors
		double[] pb_vector = new double[d];
		double[] gb_vector = new double[d];
		for(int i=0; i<d; i++){
			pb_vector[i] = pbest[i] - position[i];
			gb_vector[i] = gbest[i] - position[i];
		}
		
		
		
		//update velocity
		for (int i=0; i<d; i++){
			velocity[i] = (inertia_w * velocity[i] + gbest_w * gb_vector[i] + 
							  pbest_w * pb_vector[i]);
		}
		
	}
	
	/**************************************************
	 * Initialize particle position (randomly)
	 * @param max_b - Maximum boundary of search space.
	 * @param min_b - Minimum boundary of search space.
	 **************************************************/
	public void init_position(double max_b, double min_b){
		double rand;
		for (int i=0; i<=(d-1); i++){
			rand = generator.nextDouble();
			position[i] = rand * (max_b - min_b) + min_b;
		}
	}
	
	
	/***********************************
	 * Position setter (by dimension).
	 * @param dim - dimension.
	 * @param val - value.
	 ***********************************/
	public void set_position(int dim, double val){
		position[dim] = val;
	}
	
	
	/********************************
	 * Returns the particle's group.
	 * @return particle's group.
	 ********************************/
	public int get_group(){
		return group;
	}
	
	
	/***************************
	 * Group setter.
	 * @param gr - group index.
	 ***************************/
	public void set_group(int gr){
		group = gr;
	}
	
	
	/**************************************************
	 * Initializes particle velocity (randomly)
	 * @param max_b - Maximum boundary of search space.
	 * @param min_b - Minimum boundary of search space.
	 **************************************************/
	public void init_velocity(double max_b, double min_b){
		double rand;
		double scale = max_b - min_b;
		for (int i=0; i<=d-1; i++){
			rand = generator.nextDouble();
			//randomize velocity; up to +scale and down to -scale
			velocity[i] = rand * 2*scale - scale;  
		}
		
		//find magnitude as preparation for normalization
		double magn = 0; 
		for (int i=0; i<d; i++){
			magn += Math.pow(velocity[i],2);
		}
		
		magn = Math.sqrt(magn);
		
		//normalize velocity
		for(int i=0; i<d; i++){
			velocity[i] = velocity[i] / magn;
		}
	}
	
	
	/***********************************
	 * Initialize velocity to dead stop.
	 ***********************************/
	public void zero_velocity(){
		this.velocity = new double[velocity.length];
	}
	
	
	/***********************************
	 * Returns particle's best position
	 * @return particle's best position
	 ***********************************/
	public synchronized double[] get_pbest(){
		return pbest;
	}
	
	
	/***********************************
	 * Returns particle's best score
	 * @return particle's best score
	 ***********************************/
	public synchronized double get_pbest_val(){
		return pbest_val;
	}
	
	/******************************
	 * Returns particle's position
	 * @return particle's position
	 ******************************/
	public synchronized double[] get_position(){
		return position;
	}
	
	/*************************************************
	 * Moves the particle.
	 * @param gbest - The global best position found.
	 * @param inertia_w - Weight of inertia.
	 * @param gbest_w - Weight of gbest direction.
	 * @param pbest - Weight of pbest direction.
	 *************************************************/
	public synchronized void move(){
		for (int i=0; i<=d-1; i++){
			position[i] += velocity[i];
		}
	}
	
	/************************************************************
	 * Updates the best position found by the particle (by force)
	 * @param new_pbest - New best position of the particle.
	 ************************************************************/
	public synchronized void update_pbest(double[] new_pbest, double val){
		for (int i=0; i<=d-1; i++){
			pbest[i] = new_pbest[i];
		}
		
		pbest_val = val;
	}
	
	/**********************************
	 * Builder. Creates new particle.
	 * @param dim - No. of dimensions.
	 **********************************/
	public Particle(int dim){
		d = dim;
		position = new double[d];
		pbest = new double[d];  
		velocity = new double[d];
		group = 0; //default group is 0 (1st group)
	}
}
