package Parsing;
import java.util.Arrays;

public class Utils {

	public static String intArrayToString(int[] array){
		return Arrays.toString(array);
	}
	
	public static int[] stringToIntArray(String arrayAsString){
	    String[] strings = arrayAsString.replace("[", "").replace("]", "").split(", ");
	    int result[] = new int[strings.length];
	    for (int i = 0; i < result.length; i++) {
	      result[i] = Integer.parseInt(strings[i]);
	    }
	    return result;
	 }
	public static String[] stringToStringArray(String arrayAsString){
	    return arrayAsString.replace("[", "").replace("]", "").split(", ");
	 }	
}
