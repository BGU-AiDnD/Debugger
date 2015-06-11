package Implant;
import Implant.*;


import java.io.IOException;

public class Tester {
	public static void main(String[] args) throws IOException, InterruptedException{
Logger.log("Tester.main");
boolean _bug_switch = Bug_Switcher.has_bug("Tester.main");
if (_bug_switch)
	return;

		TestsRunner.run_from_remote("org.apache.commons.math3.util.FastMathTest.testSinhAccuracy");
//		TestsRunner.run_from_remote();
	}
}
