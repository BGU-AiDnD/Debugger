package Optim;

import java.lang.Math;
import java.util.concurrent.ForkJoinPool;

import Infrastrcture.Link;
import Infrastrcture.Linked_List;


public class PSO {
	
	//declare parameters
	public static int i_num = 5; //No. of iterations //10
	
	//search space related parameters
	private int d; //dimensions No.
	final public static double max_b = 4 * Math.PI; //maximum boundary
	final public static double min_b = 0; //minimum boundary
	
	//No. of particles
	public static int p_num = 10; //20
	final public static int p_factor = 1;
	
	//weights constants
	private static double inertia_w = 0.2;
	private static double gbest_w = 1;
	private static double pbest_w = 0.3;
	
	//groups related vars
	private int group_num = 1; //groups No. default is 1
	private double[] grbest_vals;
	private double[][] grbest; //matrix of group bests params
	private static double territory = 0.3; 
	
	//declare vars
	private Target_Function TF;
	private Particle[] particles;
	private double[]gbest;
	private double gbest_val;
	public static int join = 0;
	
	
	/*******************************************************************
	 * Constructor. Sets dimensions, particles No. and target function.
	 * @param prob - kind of problem (1=FSP, 1=JSP)
	 * @param dim - dimensions
	 *******************************************************************/
	public PSO(int dim, Target_Function tar_fun){
		d = dim; //dimensions
		TF = tar_fun;
		group_num = 1;
	}
	
	
	/****************************
	 * Groups No. setter.
	 * @param number - group No.
	 ****************************/
	public void set_group_num(int number){
		group_num = number;
	}
	
	
	/********************************************************
	 * Compute the target function for a particle's position.
	 * @param particle - particle to copy its position.
	 * @return value of target function.
	 ********************************************************/
	public synchronized double target_function(Particle particle){
		return target_function(particle.get_position());
	}
	
	
	/**************************************************
	 * Compute the target function for a given context.
	 * @param vars - Context.
	 * @return value of target function.
	 **************************************************/
	public synchronized double target_function(double[] params){
		return TF.compute(params);
	}
	
	
	/*********************************************
	 * Initializes gbest.
	 * @param new_val - New global best position.
	 *********************************************/
	public synchronized void update_gbest(Particle particle){
		double[] position = particle.get_position();
		for(int i=0; i <= d-1; i++){
			gbest[i] = position[i];
		}
		
		gbest_val = target_function(gbest);
	}
	
	
	/******************************************************
	 * getter for gbest_val, for synchronization purposes.
	 * @return gbest_val
	 ******************************************************/
	public synchronized double get_gbest_val(){
		return gbest_val;
	}
	
	
	/****************************
	 * For concurrency purposes. 
	 ****************************/
	public synchronized void increase_join(){
		join++;
	}
	
	
	/****************************
	 * For concurrency purposes. 
	 ****************************/
	public synchronized int get_join(){
		return join;
	}
	
	
	/****************************
	 * For concurrency purposes. 
	 ****************************/
	public synchronized void set_join(int number){
		join = number;
	}
	
	
	/****************************
	 * For concurrency purposes. 
	 ****************************/
	public synchronized double[] get_gbest(){
		return gbest;
	}
	
	
	/*********************************
	 * Returns group best parameters.
	 * @param group - group index.
	 * @return group best parameters.
	 *********************************/
	public synchronized double[] get_grbest(int group){
		return grbest[group];
	}
	
	
	/*********************************
	 * Returns group best value.
	 * @param group - group index.
	 * @return group best value.
	 *********************************/
	public synchronized double get_grbest_val(int group){
		return grbest_vals[group];
	}
	
	
	/******************************
	 * Group best setter.
	 * @param group - group index.
	 * @param params - parameters.
	 *******************************/
	private synchronized void set_grbest(int group, double[] params){
		grbest[group] = params;
	}
	
	
	/**********************************
	 * Group best value setter.
	 * @param group - group index.
	 * @param val - value of new best.
	 **********************************/
	private synchronized void set_grbest_val(int group, double val){
		grbest_vals[group] = val;
	}
	
	
	/**************************************
	 * Prints graph of particles location.
	 **************************************/
	public void graph(){
		int scale = (int)max_b + 1;
		int[][] debug = new int[scale][scale];
		double[] pos;
		
		for(int p=0; p<particles.length; p++){
			pos = particles[p].get_position();
			if(pos[0]>=0 && pos[1]>=0 && pos[0]<scale && pos[1]<scale)
			debug[(int)pos[0]][(int)pos[1]] += 1;
		}
		
		String result = "";
		for(int i=debug.length-1; i>=0; i--){
			result += "| ";
			for(int j=0; j<debug.length; j++){
				if(debug[i][j] != 0)
					result += (debug[i][j] + " ");
				else result += "  ";
			}
			result += "\n";
		}
		
		result += " ";
		for(int j=0; j<debug.length-1; j++)
			result += "__";
		
		System.out.println(result);
	}
	
	
	/******************************
	 * Group tagging of particles.
	 ******************************/
	private void to_groups(){
		int group = 0;
		for(int p=0; p<particles.length; p++){
			//keep group number checked
			if (group > group_num - 1)
				group = 0;
			
			particles[p].set_group(group);
			group++;
		}
	}
	
	
	/*****************************************************************************
	 * Calculates whether potential new grbest too close to other group's grbest.
	 * @param params - params to be checked.
	 * @return - true if not too close, false otherwise.
	 *****************************************************************************/
	private synchronized boolean proximity_check(double[] params, int group, double factor){
		//declare vars
		boolean result = true;
		double dist = 0;
		double[] current_grbest;
		double scale = max_b - min_b;
		
		//no pint in check distance for one group
		if (group_num == 1)
			return true;
		
		//start check
		for(int g=0; g<group_num; g++){
			current_grbest = get_grbest(g);
			dist = 0;
			for(int i=0; i<d; i++){
				dist += Math.pow((params[i] - current_grbest[i]),2); 
			}
			dist = Math.sqrt(dist);
			
			if (dist < (factor * scale) && g != group){
				result = false;
				return result;
			}
		}//end for
		
		return result;
	}
	
	
	
	/*********************************
	 * Updates group best (if legal).
	 * @param particle - particle.
	 *********************************/
	private synchronized void update_grbest(Particle particle){
		//suck data
		int group = particle.get_group();
		double[] pbest = particle.get_pbest();
		double pbest_val = particle.get_pbest_val(); 
		
		//update group best
		if (pbest_val < get_grbest_val(group))
			if(proximity_check(pbest,group, territory)){
				set_grbest(group, pbest); //grbest[group] = pbest;
				set_grbest_val(group, pbest_val); //grbest_vals[group] = pbest_val;
				
				//gbest_w = 1;
			}
				
	}
	
	
	/***********************
	 * Pbest initialization.
	 ***********************/
	private void pbest_init(){
		double[] current_pos = new double[d];
		for (int p=0; p<p_num; p++){
			current_pos = particles[p].get_position();
			particles[p].update_pbest(current_pos, target_function(current_pos));
			
		}//end for
	}
	
	
	/****************************************
	 * position and velocity initialization.
	 ****************************************/
	private void pos_vel_init(){
		particles = new Particle[p_num]; //particles array
		
		for (int i=0; i<=p_num-1; i++){
			particles[i] = new Particle(d);
			particles[i].init_position(max_b, min_b);
			particles[i].init_velocity(max_b, min_b);
		}
		
		//initialize grbest
		grbest = new double[group_num][d];
		grbest_vals = new double[group_num];
	}
	
	
	/************************
	 * Pick one global best.
	 ************************/
	private synchronized void pick_gbest(){
		double min = get_grbest_val(0);
		for(int i=0; i<group_num; i++)
			if (get_grbest_val(i) <= min){
				gbest_val = get_grbest_val(i);
				gbest = get_grbest(i);
			}
	}
	
	
	/*********************
	 * Setup global bests
	 *********************/
	private void setup_grbest(){
		//declare vars
		Linked_List positions = new Linked_List();
		Link link;
		double temp;
		
		//start setup
		//make a list of sorted positions
		for(int p=0; p<particles.length; p++){
			temp = target_function(particles[p]);
			link = new Link();
			link.set_val(temp);
			link.set_params(particles[p].get_position());
			positions.add_by_order(link);
			}//end for
		
		//pick global group bests
		link = positions.get_anchor().get_next();
		int group = 0;
		while(link != null && group < group_num){
			if(proximity_check(link.get_params(),group, 2*territory)){
				grbest[group] = link.get_params();
				grbest_vals[group] = link.get_val();
				group++;
			}
			
			link = link.get_next();
		}//end while
	}
	
	
	/********************
	 * Global best setup
	 ********************/
	private void setup_gbest(){
		//declare vars
		double min_val = particles[0].get_pbest_val();
		double[] min_params = particles[0].get_pbest().clone();
		
		for(int p=0; p<particles.length; p++){
			if (particles[p].get_pbest_val() < min_val){
				min_val = particles[p].get_pbest_val();
				min_params = particles[p].get_pbest();
			}
		}//end for
		
		gbest = min_params;
		gbest_val = min_val;
	}
	
	

	/********************
	 * Run PSO algorithm
	 ********************/
	public void run() {
		//initialize the particles position & velocity
		pos_vel_init();
		
		if(group_num > 1)
			graph();
		
		//tag particles into groups
		to_groups();
			
		//initialize gbest
		gbest = new double[d];
		update_gbest(particles[0]);
		
		//initialize pbest
		pbest_init();
		
		//set global/group bests
		if (group_num == 1)
			setup_gbest();
		setup_grbest();
			
		//RUN
		//ready threads
		ForkJoinPool pool = new ForkJoinPool();
		moveThread move1 = new moveThread();
		moveThread move2 = new moveThread();
		UpdateThread update1 = new UpdateThread();
		UpdateThread update2 = new UpdateThread();
		VelocityThread velocity1 = new VelocityThread();
		VelocityThread velocity2 = new VelocityThread();
		
		move1.start_i = 0; move1.end_i = (int)p_num/2;
		move2.start_i = (int)p_num/2+1; move2.end_i = p_num-1;
		update1.start_i = 0; update1.end_i = (int)p_num/2;
		update2.start_i = (int)p_num/2+1; update2.end_i = p_num-1;
		velocity1.start_i = 0; velocity1.end_i = (int)p_num/2;
		velocity2.start_i = (int)p_num/2+1; velocity2.end_i = p_num-1;
		
		
		//start iterations
		for(int i=0; i<=i_num-1; i++){
			pool = new ForkJoinPool();
			set_join(0); //for concurrency purposes
			velocity1.it = i; velocity2.it = i;
			
			//adjust weights
			pbest_w = pbest_w * (1 - i/PSO.i_num);  //give more weight as simulation goes
			
			//update pbest & gbest
			pool.execute(update1);
			pool.execute(update2);
			
			//wait for threads to finish
			while(get_join()<2){
				
			}
			
			
			//update velocities
			pool.execute(velocity1);
			pool.execute(velocity2);
			
			//wait for threads to finish
			while(get_join()<4){
				
			}
			
			//move particles
			pool.execute(move1);
			pool.execute(move2);
			
			//wait for threads to finish
			while(get_join()<6){
				
			}
			pool.shutdown();
			
		}//end for (iterations)
		
		pick_gbest();
		if(group_num > 1)
			graph();
	}//end run method
	
	
	/************************
	 * String representation
	 ************************/
	
	public String toString(){
		String result = "";
		return result;
	}
	
	
	/*******************************************************************************************
	 * Special classes
	 *******************************************************************************************/
	private class moveThread extends Thread{
		int start_i, end_i;
		
		public synchronized void run(){
			for(int p=start_i; p<=end_i; p++){
				//move
				particles[p].move();
				
			}//end for
			increase_join();
		}//end run()
	}//end moveThread
	
	
	private class UpdateThread extends Thread{
		int start_i, end_i;
		
		public synchronized void run(){
			for(int p=start_i; p<=end_i; p++){
				//update grbest
				double pos_val = target_function(particles[p]);
				update_grbest(particles[p]);
			
				//update pbest
				double[] position = particles[p].get_position();
				int group = particles[p].get_group();
				if(pos_val < particles[p].get_pbest_val() && proximity_check(position, group, territory))
					particles[p].update_pbest(position, pos_val);
				
			}//end for
			
			increase_join();
		}//end run()
	}//end UpdateThread
	
	
	
	private class VelocityThread extends Thread{
		int start_i, end_i;
		int it; //PSO iteration
		int group;
		
		public synchronized void run(){
			for(int p=start_i; p<=end_i; p++){
				group = particles[p].get_group();
				if((int)particles[p].get_pbest_val() != (int)get_grbest_val(group))
					particles[p].update_velocity(it, get_grbest(group), inertia_w, gbest_w, pbest_w);
				else 
					particles[p].update_velocity(it, get_grbest(group), inertia_w, 0, 2*pbest_w);
			}//end for (particles update velocity)
			increase_join();
		}//end run()
	}//end updateThread
		
}//end PSO class
