package Optim;

public abstract class Target_Function {
	public abstract double compute(double[] params);
	
	public abstract Target_Function clone();
}
