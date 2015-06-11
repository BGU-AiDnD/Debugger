package Deprecated;
import Implant.*;


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
Logger.log("Particle.update_velocity");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.update_velocity");
if (_bug_switch)
	return;

		//generate randomness every 2nd iteration
		double gbest_r;
		double pbest_r;
		
		if(it % 2 == 0 ){
			gbest_r = generator.nextDouble()*3;
			pbest_r = generator.nextDouble()*3;
		} else{
			gbest_r = 1; 
			pbest_r = 1;
		}
	
			
		//calculate vectors
		double[] pb_vector = new double[d];
		double[] gb_vector = new double[d];
		for(int i=0; i<d; i++){
			pb_vector[i] = pbest[i] - position[i];
			gb_vector[i] = gbest[i] - position[i];
		}
		
		
		//calculate magnitudes
		double pb_magn = 0; 
		double gb_magn = 0; 
		double v_magn = 0;
		for(int i=0; i<d; i++){
			pb_magn += Math.pow(pb_vector[i],2);
			gb_magn += Math.pow(gb_vector[i],2);
			v_magn += Math.pow(velocity[i],2);
		}
		pb_magn = Math.sqrt(pb_magn);
		gb_magn = Math.sqrt(gb_magn);
		v_magn = Math.sqrt(v_magn);
		
		//handle zero magnitude
		if (pb_magn == 0)
			pb_magn = 1;
		if (gb_magn == 0)
			gb_magn = 1; 
		if (v_magn == 0)
			v_magn = 1; 
		
		
		//update velocity
		for (int i=0; i<d; i++){
			velocity[i] = (inertia_w * (velocity[i])/v_magn + 
							gbest_r * gbest_w * (gb_vector[i])/gb_magn + 
							pbest_r * pbest_w * (pb_vector[i])/pb_magn) * 1.5*(1-it/(PSO.i_num));
		}
		
	}
	
	/**************************************************
	 * Initialize particle position (randomly)
	 * @param max_b - Maximum boundary of search space.
	 * @param min_b - Minimum boundary of search space.
	 **************************************************/
	public void init_position(double max_b, double min_b){
Logger.log("Particle.init_position");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.init_position");
if (_bug_switch)
	return;

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
Logger.log("Particle.set_position");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.set_position");
if (_bug_switch)
	return;

		position[dim] = val;
	}
	
	
	/********************************
	 * Returns the particle's group.
	 * @return particle's group.
	 ********************************/
	public int get_group(){
Logger.log("Particle.get_group");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.get_group");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

		return group;
	}
	
	
	/***************************
	 * Group setter.
	 * @param gr - group index.
	 ***************************/
	public void set_group(int gr){
Logger.log("Particle.set_group");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.set_group");
if (_bug_switch)
	return;

		group = gr;
	}
	
	
	/**************************************************
	 * Initializes particle velocity (randomly)
	 * @param max_b - Maximum boundary of search space.
	 * @param min_b - Minimum boundary of search space.
	 **************************************************/
	public void init_velocity(double max_b, double min_b){
Logger.log("Particle.init_velocity");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.init_velocity");
if (_bug_switch)
	return;

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
Logger.log("Particle.zero_velocity");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.zero_velocity");
if (_bug_switch)
	return;

		this.velocity = new double[velocity.length];
	}
	
	
	/***********************************
	 * Returns particle's best position
	 * @return particle's best position
	 ***********************************/
	public synchronized double[] get_pbest(){
Logger.log("Particle.get_pbest");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.get_pbest");
if (_bug_switch)
	return null;

		return pbest;
	}
	
	
	/***********************************
	 * Returns particle's best score
	 * @return particle's best score
	 ***********************************/
	public synchronized double get_pbest_val(){
Logger.log("Particle.get_pbest_val");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.get_pbest_val");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

		return pbest_val;
	}
	
	/******************************
	 * Returns particle's position
	 * @return particle's position
	 ******************************/
	public synchronized double[] get_position(){
Logger.log("Particle.get_position");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.get_position");
if (_bug_switch)
	return null;

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
Logger.log("Particle.move");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.move");
if (_bug_switch)
	return;

		for (int i=0; i<=d-1; i++){
			position[i] += velocity[i];
		}
	}
	
	/************************************************************
	 * Updates the best position found by the particle (by force)
	 * @param new_pbest - New best position of the particle.
	 ************************************************************/
	public synchronized void update_pbest(double[] new_pbest, double val){
Logger.log("Particle.update_pbest");
boolean _bug_switch = Bug_Switcher.has_bug("Particle.update_pbest");
if (_bug_switch)
	return;

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
