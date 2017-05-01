package inst;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileFilter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.ClassLoader;
import java.lang.Class;
import java.util.Arrays;
import java.util.ArrayList;

import java.security.ProtectionDomain;
import java.util.LinkedList;
import java.util.List;
import java.util.StringTokenizer;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

import javassist.CannotCompileException;
import javassist.ClassPath;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtField;
import javassist.CtMethod;
import javassist.CtNewMethod;
import javassist.Modifier;
import javassist.NotFoundException;
import javassist.bytecode.AnnotationsAttribute;
import javassist.bytecode.AttributeInfo;
import java.net.URLClassLoader;


public class MyInstrumenter implements ClassFileTransformer {
 
	public boolean init=false;
	public static String injectedClassName = null;
	
	public void initiate(String name, ClassLoader loader, ProtectionDomain protectionDomain){
		if(!init){
		init=true;
			injectedClassName="junit.framework.TestCase";
		//injectedClassName=name;
		ClassPool cp = ClassPool.getDefault();	
		
		cp.importPackage("java.io.PrintWriter");
		cp.importPackage("java.io.BufferedWriter");
		cp.importPackage("java.io.FileWriter");
		cp.importPackage("java.io.File");
		cp.importPackage("java.io.IOException");
		cp.importPackage("java.lang.StringBuffer");
		cp.importPackage("java.net.URLClassLoader");
		cp.importPackage("java.net.URL");
		cp.importPackage(injectedClassName);
		cp.importPackage("java.util.LinkedList");
		cp.importPackage("java.util.List");
		
		
		System.out.println("Injecting method to " + injectedClassName + "...");
		//injectToMethod(loader,protectionDomain);	
		System.out.println("Method injection done");
		
		ClassPathForGeneratedClasses gcp = new ClassPathForGeneratedClasses();  
			cp.insertClassPath(gcp); 

		System.out.println("Hello!" + System.currentTimeMillis());
		
		try {
			CtClass traceWriterClass = cp.makeClass("TestsTraces");
			CtField fileNameField;			
			fileNameField = CtField.make("public static String fileName=null;", traceWriterClass);
			fileNameField.setModifiers(Modifier.PUBLIC | Modifier.STATIC);
			traceWriterClass.addField(fileNameField,"null");
			
			CtField testClassField;			
			testClassField = CtField.make("public static String testClass=null;", traceWriterClass);
			testClassField.setModifiers(Modifier.PUBLIC | Modifier.STATIC);
			traceWriterClass.addField(testClassField,"null");
			
			CtField outField;			
			outField = CtField.make("public static java.io.PrintWriter out=null;", traceWriterClass);
			outField.setModifiers(Modifier.PUBLIC | Modifier.STATIC);
			traceWriterClass.addField(outField,"null");
			
			CtField qField;			
			qField = CtField.make("public static java.util.LinkedList q = new java.util.LinkedList();", traceWriterClass);
			qField.setModifiers(Modifier.PUBLIC | Modifier.STATIC);
			traceWriterClass.addField(qField,"new java.util.LinkedList()");
			
			
			StringBuilder changeFile=new StringBuilder();
			changeFile.append("public static synchronized void changefile(java.lang.String newName){\n");
			//changeFile.append("if(TestsTraces.fileName==null){\n");
			changeFile.append("long time= System.currentTimeMillis();\n");
			changeFile.append("String name=newName;\n");
			changeFile.append("String namePre=\"..\\\\..\\\\DebuggerTests\\\\Trace_\"+name;\n");
			changeFile.append("boolean check =TestsTraces.fileName!=null && namePre.equals(TestsTraces.fileName.substring(0, TestsTraces.fileName.lastIndexOf(\"_\")));\n");
			changeFile.append("if( check){ return; }\n");
			changeFile.append("TestsTraces.fileName=\"..\\\\..\\\\DebuggerTests\\\\Trace_\"+name+\"_\"+time+\".txt\";\n");
			changeFile.append("File f=new File(TestsTraces.fileName.substring(0, TestsTraces.fileName.lastIndexOf(\"\\\\\")));\n");
			//changeFile.append("f=new File(f.getPath());\n");
			//changeFile.append("System.out.println(\"dir: \" +f.getPath());\n");
			changeFile.append("f.mkdirs();\n");
			changeFile.append("System.out.println(\"changed! \" +TestsTraces.fileName);\n");
			changeFile.append("TestsTraces.testClass=TestsTraces.fileName.substring(0, TestsTraces.fileName.lastIndexOf('.')); TestsTraces.q = new java.util.LinkedList();\n");
			changeFile.append("try {\n");
			changeFile.append("TestsTraces.out = new java.io.PrintWriter(new java.io.BufferedWriter(new java.io.FileWriter(TestsTraces.fileName, true)));\n");
			changeFile.append("} catch (IOException e) {\n");
			changeFile.append("e.printStackTrace();\n");
			changeFile.append("}\n");
			//changeFile.append("}\n");
			changeFile.append("}\n");
			CtMethod m=CtNewMethod.make(changeFile.toString(), traceWriterClass);
			m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
			traceWriterClass.addMethod(m);

			StringBuilder write=new StringBuilder();
			write.append("public static synchronized void write(java.lang.String line){\n");
			//write.append("String toWrite=line.substring(0, line.lastIndexOf('.'));\n");
			write.append("String toWrite=line;\n");
			write.append("if(TestsTraces.fileName!=null && TestsTraces.out!=null && !TestsTraces.q.contains(toWrite)){\n");
			
			write.append("TestsTraces.out.println(\"[inst2] + \"+toWrite);\n");
			write.append("TestsTraces.out.flush();\n");
			write.append("TestsTraces.q.add(toWrite);\n");
			write.append("}\n");
			write.append("}\n");
			

			StringBuilder Add=new StringBuilder();
			Add.append("public static synchronized void Add(String line){\n");
			Add.append("if(line.equals(TestsTraces.testClass))\n");
			Add.append("return;\n");
			Add.append("TestsTraces.q.add(line);\n");
			Add.append("while(TestsTraces.q.size()>=10){\n");
			Add.append("TestsTraces.q.remove();\n");
			Add.append("}\n");
			Add.append("}\n");
			m=CtNewMethod.make(Add.toString(), traceWriterClass);
			m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
			traceWriterClass.addMethod(m);
			
			m=CtNewMethod.make(write.toString(), traceWriterClass);
			m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
			traceWriterClass.addMethod(m);
			
			
			traceWriterClass.writeFile("target\\classes");
			traceWriterClass.toClass(loader,protectionDomain);
			gcp.addGeneratedClass(traceWriterClass); 
			traceWriterClass.writeFile("target\\classes\\org\\eclipse\\cdt");
			
		} catch (Exception e) {
			System.out.println("exception in initiate");

			e.printStackTrace();			
		}
	
	}
	
	
}
	

public byte[] nicerTransform(ClassLoader loader, String className, Class<?> classBeingRedefined,    		
    ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
	
	this.initiate(className,loader,protectionDomain);
	
	byte[] byteCode = classfileBuffer;
	try{
	loader.loadClass("TestsTraces");
	}
	catch(Exception e){}
	String[] s=className.split("/");
	boolean eclipse=s[0].equals("org") &&s[1].equals("eclipse") &&s[2].equals("cdt");
	boolean poi=s[0].equals("org") &&s[1].equals("apache") &&s[2].equals("poi");
	boolean ant=s[0].equals("org") &&s[1].equals("apache") &&s[2].equals("tools");
	boolean tomPack=s[2].equals("catalina") || s[2].equals("coyote") || s[2].equals("el") || s[2].equals("jasper") || s[2].equals("juli") || s[2].equals("naming") || s[2].equals("tomcat");
	boolean tomcat=s[0].equals("javax") ||  s[0].equals("org") &&s[1].equals("apache") && tomPack;
	boolean myapp=s[0].equals("com") &&s[1].equals("mycompany") &&s[2].equals("app");
	boolean surefire=s[3].equals("surefire");
	boolean lang=s[0].equals("java") ;
	boolean mvn=s[0].equals("org") && s[1].equals("apache") && s[2].equals("maven") ;
	boolean sun=s[0].equals("sun") || s[1].equals("sun") ;
	boolean junit=s[0].equals("org") && s[1].equals("junit");
	boolean osgi=s[0].equals("org") && s[1].equals("eclipse")&& s[2].equals("osgi");
	//System.out.println(s[0] +" " +s[1]+" " +s[2]+" " +s[3]);
	ClassPool cp = ClassPool.getDefault();
	String name=className.replace("/",".");
		name=name.split("$")[0];
	cp.importPackage(name);
	if (!surefire && !lang  && !sun && !junit && !mvn && !osgi) {

		
		
        try { 

            
		/*	paths=((URLClassLoader)"".getClass().getClassLoader().getSystemClassLoader()).getURLs();
		for (URL c : paths){
			//System.out.println("URL: "+c.getFile());
			cp.appendClassPath(c.getFile());
		}*/
			cp.importPackage(name);
			//cp.appendSystemPath();
			//System.out.println(System.getProperty("user.dir"));
			/*List<File> WorkingDir= getSubdirs(new File(System.getProperty("user.dir")));
			for(File path : WorkingDir) {
				System.out.println(path.toString());
				cp.appendClassPath(path.toString()); 
		    }*/
			cp.appendClassPath(System.getProperty("user.dir"));
			//cp.appendClassPath("C:/projs/cdt4Working/testedVer/repo/core/org.eclipse.cdt.core/target/classes/org/eclipse/cdt/core/parser");
			//cp.appendClassPath(new URL(System.getProperty("user.dir")).toString());
			//cp.appendClassPath(Class.forName(name,true,ClassLoader.getSystemClassLoader()).getClass().getClassLoader().getSystemClassLoader());
		

            CtClass cc = cp.get(name);                
            CtMethod[] methods = cc.getDeclaredMethods();
			if(!cc.isInterface()){
            for (CtMethod method : methods){

            	CtMethod m = cc.getDeclaredMethod(method.getName());
				if(m.isEmpty()){
					continue;
				}
            	String met=cc.getName()+"@"+method.getName();

            	StringBuffer toInsert = new StringBuffer();

          		// Load trace writer class dynamically
				
            	toInsert.append("Class testsRunnerClass=null;");
            	toInsert.append("try{");
            	toInsert.append("	testsRunnerClass = Class.forName(\"TestsTraces\",true, \"amir\".getClass().getClassLoader().getSystemClassLoader());");
            	toInsert.append("}catch(Exception exception){");
            	//toInsert.append("	System.out.println(\"exception1\");");
            	toInsert.append("	if(testsRunnerClass==null){");
				//D:\Amir_Almishali\agent\CDT_8_1_2\org.eclipse.cdt\core\org.eclipse.cdt.core.tests\target\classes
    			//toInsert.append("		URL classUrl = new URL(\"file:\\\\\\target\\\\classes\\\\\");");
    			toInsert.append("try{");
            	//toInsert.append("		URL classUrl = new URL(\"file:///D:/Amir_Almishali/agent/CDT_8_1_2/org.eclipse.cdt/core/org.eclipse.cdt.core.tests/target/classes/\");");
            	//toInsert.append("		URL classUrl = new URL(\"file:///C:/tomcat/TOMCAT_8_0_8/\");");
            	toInsert.append("		URL classUrl = new URL(System.getProperty(\"user.dir\"));");
    			toInsert.append("		URLClassLoader myLoader = URLClassLoader.newInstance(new URL[]{classUrl}, \"amir\".getClass().getClassLoader().getSystemClassLoader());");// get class of String
    			toInsert.append("		System.out.println(\"before load class \" + myLoader);");
    			//toInsert.append("		testsRunnerClass = myLoader.loadClass(\"TestsTraces\");");
    			toInsert.append("	testsRunnerClass = Class.forName(\"TestsTraces\",true, myLoader);");
    			//URLClassLoader myLoader = URLClassLoader.newInstance(new URL[]{classUrl}, Object.class.getClassLoader());
    			//myLoader.loadClass(name);
    			
    			
            	//toInsert.append("	testsRunnerClass = Class.forName(\"TestsTraces\");");
            	toInsert.append("}catch(Exception exception2){");
            	//toInsert.append("	System.out.println(\"exception2\");");
            	//toInsert.append("	exception2.printStackTrace();");
            	toInsert.append("}");
				        			
    			
    			//toInsert.append("		System.out.println(\"after load class\" + testsRunnerClass);");
    			//toInsert.append("		testsRunnerClass = URLClassLoader.newInstance(new URL[]{classUrl}, Object.class.getClassLoader()).loadClass(\"TestsTraces\");");        			
    			toInsert.append("	}");
            	toInsert.append("}");

            	
            	toInsert.append("try{");
            	toInsert.append("Class[] cArg = new Class[1];");
            	toInsert.append("cArg[0] = String.class;");
            	toInsert.append("Object[] params = {\""+ met +"\"};");
        		// If starting a new test, close previous file with trace of previous test
            	boolean isTestFunction = (cc.getName().contains("Test") && method.getName().startsWith("test"));
            	if(isTestFunction){
            		// Rename when finished past test
            		toInsert.append("testsRunnerClass.getMethod(\"changefile\", cArg).invoke(null, params);");
            		//toInsert.append("TestsTraces.changefile(\""+met + "\");\n");
            		
            	}
            	                 	
            	// Print method to current trace file
            	toInsert.append("testsRunnerClass.getMethod(\"write\", cArg).invoke(null, params);");              	
            	//toInsert.append("TestsTraces.write(\""+met + "\");\n");

        		toInsert.append("} catch (Exception e) {");
            	toInsert.append("	System.out.println(\"exception e\");");
        		toInsert.append("	e.printStackTrace();");
        		toInsert.append("}");
            	
            	//String ins="System.out.println(\"[inst2] +\" \" "+met+"\");";                	
            	String ins=toInsert.toString();
				//System.out.println(ins);
            	try {
            		int mod=m.getModifiers();
            		boolean act=true;
            		act =act & !Modifier.isNative(mod);
            		act =act & !Modifier.isAbstract(mod);
            		act =act & !Modifier.isFinal(mod);
            		if(act)
            		m.insertBefore(ins);
				}
				catch(Exception e){
				System.out.println("exception in insertBefore "+ met);
					System.out.println(e.getMessage());
					System.err.println(met);
					e.printStackTrace();
				}
            	/*ins="System.out.flush();";
				try {
            	m.insertBefore(ins);
				}
				catch(Exception e){
					System.err.println(met);
				}*/
				
				
				// If finished current test, copy current.txt to a file to start a new current.txt
				// to avoid blowup of file
			/*	if(cc.getName().startsWith("Test") && method.getName().startsWith("test")){
					File i = new File();
					
				}
										}
				*/
            }
			}
            byteCode = cc.toBytecode();
            cc.detach();
        } catch (Exception ex) {
		System.out.println("exception in nicer");
            ex.printStackTrace();
			System.err.println(ex.getMessage());
        }
	}
	
	return byteCode;
}


@Override
public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
        ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
	
	return nicerTransform(loader,className,classBeingRedefined,protectionDomain,classfileBuffer);
}
}