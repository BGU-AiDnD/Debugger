package Experimenter.test;
import Implant.*;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

import org.junit.Test;

import sun.instrument.InstrumentationImpl;
import Experimenter.ExpThread;
import Experimenter.ExperimentInstance;
import Experimenter.InstanceGenerator;
import junit.framework.TestCase;

public class InstanceGeneratorTest extends TestCase {
	@Test
	public void testExportImport(){
Logger.log("InstanceGeneratorTest.testExportImport");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGeneratorTest.testExportImport");
if (_bug_switch)
	return;

		InstanceGenerator generator;
		double asked_ratio = 0.001;
		int num_of_initials = 4;
		ExperimentInstance instance;
		
		try {
			generator = new InstanceGenerator(false);
			instance = generator.generateInstance(asked_ratio, num_of_initials);
			
			File instance_file = new File("temp_instance_file.txt");
			instance.write_to_file(instance_file);
			ExperimentInstance instance_from_file = ExperimentInstance.read_from_file(instance_file);
			
			assertEquals(instance_from_file.get_pool().size(),instance.get_pool().size());
			assertEquals(instance.get_failed_tests(), instance_from_file.get_failed_tests());
			assertEquals(instance.get_initial_tests(), instance_from_file.get_initial_tests());
			
		} catch (IOException | InterruptedException e) {
			e.printStackTrace();
			fail("Exception occured:" + e);
		}
		
	}
	
	/**
	 * Test if instance read from file 
	 */
	@Test
	public void testInstanceRunnable(){
Logger.log("InstanceGeneratorTest.testInstanceRunnable");
boolean _bug_switch = Bug_Switcher.has_bug("InstanceGeneratorTest.testInstanceRunnable");
if (_bug_switch)
	return;

		File instance_file = new File("temp_instance_file.txt");
		try {
			ExperimentInstance instance_from_file = ExperimentInstance.read_from_file(instance_file);
			ExpThread runner = new ExpThread(false);
			
			try{
			runner.exec(instance_from_file);
			}catch(Throwable t){
				t.printStackTrace();
				fail("Runner failed");
			}
			
		} catch (IOException e) {
			e.printStackTrace();
			fail("Exception occured:" + e);
		}
		
	}
}
