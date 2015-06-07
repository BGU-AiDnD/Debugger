package Implant;
import java.io.File;
import java.io.IOException;
import static java.nio.file.StandardCopyOption.*;import java.nio.file.Files;
import org.junit.runner.Description;
import org.junit.runner.notification.Failure;
import org.junit.runner.notification.RunListener;

import Implant.Logger;

public class TestsListener extends RunListener{
	
	/****************************************
	 * Protocol for after-test-has-finished. 
	 ****************************************/
    public void testFinished(Description description) throws Exception {
    	//trim method name
    	String class_name = description.getClassName();
    	trim_class_name(class_name);
    	
    	//dump trace to disk
    	Logger.commit(class_name + '.' + description.getMethodName() + ".txt");
    	
    	System.out.println("Test finished.");
    }
    
    /***********************************
     * Protocol for before-test-starts.
     ***********************************/
    public void testStarted(Description description) throws Exception {
    	System.out.println("\nStart test " + '"' + description.getMethodName() + '"');
    	Logger.refresh();
    	String full_name = description.getClassName() + '.' + description.getMethodName();
    	TestsRunner.set_now_running(full_name);
    }
    
    
    /******************************************************
     * Protocol for assumption failure. 
     * (Assumption: test contains bug-injected component).
     ******************************************************/
    public void testAssumptionFailure(Failure failure){
    	//initialize
    	File base_trace = null;
    	File reg_trace = null;
    	String test_long_name = "";
    	
    	//notify the user
    	String test_short_name = failure.getDescription().getMethodName();
    	System.out.println("Test " + '"' + test_short_name + '"' + " was aborted because it contains no bug-injected components.");
    	
    	//duplicate the base trace instead of in-practice-trace
    	try{
    		test_long_name = failure.getDescription().getClassName() + '.' + test_short_name;
	    	base_trace = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces/base/" + test_long_name + ".txt");
	    	reg_trace = new File("c:/tom/eclipse/workspace/Program_Diagnoser/traces/" + test_long_name + ".txt");
    	}catch(Exception e){
    		System.out.println("something went wrong.");
    		e.printStackTrace();
    	}
    	
    	System.out.println("trying yo copy files...");
    	try {
			Files.copy(base_trace.toPath(), reg_trace.toPath(),REPLACE_EXISTING);
		} catch (IOException e) {
			System.out.println("something went wrong.");
			e.printStackTrace();
		}
    	System.out.println("Base trace was copied to the trace-in-practice");
    	
    	//wrap
    	Logger.refresh(); //clear the log so it won't ovveride the trace just created
    }
    
    
    /***********************************
     * Trims class name.
     * @param class_name - Class name.
     ***********************************/
    public static String trim_class_name(String class_name){
    	//initialize
    	String temp_name = "";
    	String result;	
    	
    	//process
    	if (class_name.contains(".")){
    		int index = class_name.length() - 1;
    		
    		while(class_name.charAt(index) != '.'){
    			temp_name += class_name.charAt(index);
    			index--;
    		}//end while
    	}//end if
    	
    	//reverse mirror
    	result = "";
    	for(int i = temp_name.length() - 1; i >= 0; i-- )
    		result += temp_name.charAt(i);    	
    	
    	return result;
    }
}
