package inst;
import inst.MyInstrumenter;

import java.lang.instrument.Instrumentation;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.io.File;

import javassist.ClassPool;



public class MyAgent {

	public static void classPaths(ArrayList<String> cPs) throws IOException{
		File f =new File("D:\\Amir_Almishali\\agent\\dirs2.txt");
		if(f.exists()){
	BufferedReader br = new BufferedReader(new FileReader("D:\\Amir_Almishali\\agent\\dirs2.txt"));
	String line;
	while ((line = br.readLine()) != null) {
	cPs.add(line);
	}
	br.close();
		}
	}


    public static void premain(String agentArgs, Instrumentation inst) {
		ArrayList<String> cPs = new ArrayList<String>();
		cPs.add(".");
		try{
		classPaths(cPs);
		Iterator<String> it= cPs.iterator();
		StringBuilder sb=new StringBuilder(); 
		while(it.hasNext()){
			sb.append(";");
			sb.append(it.next());
		}
		if(cPs.size()!=1){
		String paths=sb.toString();
		paths=paths.substring(1);
		ClassPool cp = ClassPool.getDefault();
		cp.appendPathList(paths);
		}
		} catch (Exception ex) {
                ex.printStackTrace();
            }
		
		MyInstrumenter m=new MyInstrumenter();
		//m.initiate();
        inst.addTransformer(m);
    }
}
