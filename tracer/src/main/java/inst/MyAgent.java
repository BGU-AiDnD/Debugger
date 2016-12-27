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
import java.util.Arrays;
import java.util.ArrayList;
import java.io.FileFilter;

import javassist.ClassPool;



public class MyAgent {

	public static ArrayList<String> classPaths(String path) throws IOException{
		ArrayList<String> cPs=new ArrayList<String>();
		//File f =new File("D:\\Amir_Almishali\\agent\\dirs2.txt");
		File f =new File(path);
		if(f.exists()){
	//BufferedReader br = new BufferedReader(new FileReader("D:\\Amir_Almishali\\agent\\dirs2.txt"));
	BufferedReader br = new BufferedReader(new FileReader(path));
	String line;
	while ((line = br.readLine()) != null) {
		//System.out.println(line);
	cPs.add(line);
	}
	br.close();
	}
		
	return cPs;
	}

public static boolean IsClassesDir(File folder){
	File[] listOfFiles = folder.listFiles();
    for (int i = 0; i < listOfFiles.length; i++) {
      if (listOfFiles[i].isFile()) {
        boolean b=listOfFiles[i].getName().indexOf(".class")!=-1 || listOfFiles[i].getName().indexOf(".jar")!=-1;
        		if(b){
        			return true;
				}
      } 
    }
    return false;

}
	
 
public static boolean IsClassesDirORG(File folder){
	if (folder==null)
		return false;
	
		boolean e=folder.getName().indexOf(".jar")!=-1;
		if(e){
			return true;
				}
		boolean d=folder.getName().indexOf("classes")!=-1;
		if(d){
			return true;
				}
	File[] listOfFiles = folder.listFiles();
    for (int i = 0; i < listOfFiles.length; i++) {
		boolean c=listOfFiles[i].getName().indexOf("org")!=-1;
		if(c){
        			return true;
				}
      if (listOfFiles[i].isFile()) {
        boolean b=listOfFiles[i].getName().indexOf(".class")!=-1 || listOfFiles[i].getName().indexOf(".jar")!=-1;
        		if(b){
        			return true;
				}
      } 
    }
    return false;

}
	
 	
	
public static List<File> getSubdirs(File file) {
	File[] files=file.listFiles(new FileFilter() {
        public boolean accept(File f) {
            return f.isDirectory() ||  f.getName().indexOf(".jar")!=-1;//&& IsClassesDir(f);
        }
    });
	
    List<File> subdirs = null;//Arrays.asList();
	if (files!=null){
		subdirs=Arrays.asList(files);
		subdirs = new ArrayList<File>(subdirs);
	}
	else{
	subdirs = new ArrayList<File>();
	}
	

    List<File> deepSubdirs = new ArrayList<File>();
    for(File subdir : subdirs) {
		if (subdir.isDirectory()){
        deepSubdirs.addAll(getSubdirs(subdir)); 
		}
		else{
			deepSubdirs.add(subdir);
		}
    }
    subdirs.addAll(deepSubdirs);
    List<File> subdirsClasses=new ArrayList<File>();
	for(File subdir : subdirs) {
		if (IsClassesDirORG(subdir)){
        subdirsClasses.add(subdir); 
		}
    }
    return subdirsClasses;
}

    public static void premain(String agentArgs, Instrumentation inst) {
		ClassPool cp = ClassPool.getDefault();
		//List<File> WorkingDir= getSubdirs(new File(System.getProperty("user.dir")));
		//System.out.println("user.dir: "+System.getProperty("user.dir").toString());
		if (agentArgs!=null){
			//System.out.println(agentArgs);
			List<File> WorkingDir=new ArrayList<File>();
			try{ 
			ArrayList<String> cPs= classPaths(agentArgs);
			Iterator<String> it= cPs.iterator();
		while(it.hasNext()){
			String n=it.next();
			System.out.println(n);
			WorkingDir.addAll(getSubdirs(new File(n)));
		}
			}catch(Exception e){
					System.out.println(" exception in premain");
					System.out.println(e.getMessage());
					e.printStackTrace();
				}
		//List<File> WorkingDir= getSubdirs(new File(agentArgs));
		//WorkingDir.addAll(getSubdirs(new File("C:\\Users\\amir\\.m2\\repository")));
		for(File path : WorkingDir) {
			//System.out.println("dir: "+path.toString());
			try {
			cp.appendClassPath(path.toString()); }
			catch(Exception e){
					System.out.println(e.getMessage());
					e.printStackTrace();
				}
		    }
		}
		
		MyInstrumenter m = new MyInstrumenter();
		//m.initiate();
        inst.addTransformer(m);
    }
}
