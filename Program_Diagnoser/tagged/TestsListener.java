package Implant;
import Implant.*;

import org.junit.runner.Description;
import org.junit.runner.notification.RunListener;

import Implant.Logger;

public class TestsListener extends RunListener{
    public void testFinished(Description description) throws Exception {
Logger.log("TestsListener.testFinished");
boolean _bug_switch = Bug_Switcher.has_bug("TestsListener.testFinished");
if (_bug_switch)
	return;

    	//trim method name
    	String class_name = description.getClassName();
    	trim_class_name(class_name);
    	
    	//dump trace to disk
    	Logger.commit(class_name + '.' + description.getMethodName() + ".txt");
    	
    	System.out.println("Test finished.");
    }
    
    public void testStarted(Description description) throws Exception {
Logger.log("TestsListener.testStarted");
boolean _bug_switch = Bug_Switcher.has_bug("TestsListener.testStarted");
if (_bug_switch)
	return;

    	System.out.println("\nStart test " + '"' + description.getMethodName() + '"');
    	Logger.refresh();
    }
    
    
    /***********************************
     * Trims class name.
     * @param class_name - Class name.
     ***********************************/
    public static String trim_class_name(String class_name){
Logger.log("TestsListener.trim_class_name");
boolean _bug_switch = Bug_Switcher.has_bug("TestsListener.trim_class_name");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

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
