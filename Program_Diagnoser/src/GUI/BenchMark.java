package GUI;

import Experimenter.TDP_Run;
import Parsing.FilesAssist;
import java.io.File;
import java.io.IOException;


public class BenchMark {

	

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		int iterations=Integer.parseInt(args[0]);
		String Instances=args[1];
		String out=args[2];
		FilesAssist.instances_path = 	 new File(Instances).toPath();
		FilesAssist.outPath = 	 new File(out).toPath().toString()+"\\";
		double threshold=Double.parseDouble(args[3]);
		
		//System.exit(0);
		//TDP_Run.executions_num=iterations;
		TDP_Run.set_executions_num(iterations);
		TDP_Run.set_threshold_prob(threshold);
		TDP_Run.set_init_tests(TDP_Run.initialize_method.BENCHMARK);
		TDP_Run.method_types selected = TDP_Run.method_types.values()[6];
		TDP_Run.set_plan_method(selected);
		try {
			TDP_Run.main(args);
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

	/**
	 * Create the frame.
	 */

	
	
	
	
}
