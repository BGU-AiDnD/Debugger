package Parsing;
import Implant.*;

import Implant.*;


import java.util.Arrays;

public class Utils {

	public static String intArrayToString(int[] array){
Logger.log("Utils.intArrayToString");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.intArrayToString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

Logger.log("Utils.intArrayToString");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.intArrayToString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return Arrays.toString(array);
	}
	
	public static int[] stringToIntArray(String arrayAsString){
Logger.log("Utils.stringToIntArray");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.stringToIntArray");
if (_bug_switch)
	return null;

Logger.log("Utils.stringToIntArray");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.stringToIntArray");
if (_bug_switch)
	return null;
	
	    String[] strings = arrayAsString.replace("[", "").replace("]", "").split(", ");
	    int result[] = new int[strings.length];
	    for (int i = 0; i < result.length; i++) {
	      result[i] = Integer.parseInt(strings[i]);
	    }
	    return result;
	 }
	public static String[] stringToStringArray(String arrayAsString){
Logger.log("Utils.stringToStringArray");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.stringToStringArray");
if (_bug_switch)
	return null;

Logger.log("Utils.stringToStringArray");
boolean _bug_switch = Bug_Switcher.has_bug("Utils.stringToStringArray");
if (_bug_switch)
	return null;
	
	    return arrayAsString.replace("[", "").replace("]", "").split(", ");
	 }	
}
