package inst;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import java.security.ProtectionDomain;
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
		cp.importPackage("junit.framework");
		
		
		System.out.println("Injecting methdo to " + injectedClassName + "...");
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
			StringBuilder changeFile=new StringBuilder();
			changeFile.append("public static synchronized void changefile(java.lang.String newName){\n");
			changeFile.append("if(TestsTraces.fileName==null){\n");
			changeFile.append("long time= System.currentTimeMillis();\n");
			changeFile.append("TestsTraces.fileName=\"..\\\\..\\\\DebuggerTests\\\\Trace_\"+newName+\"_\"+time+\".txt\";\n");
			changeFile.append("System.out.println(\"changed! \" +TestsTraces.fileName);\n");
			changeFile.append("}\n");
			
			changeFile.append("}\n");
			CtMethod m=CtNewMethod.make(changeFile.toString(), traceWriterClass);
			m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
			traceWriterClass.addMethod(m);
			
			StringBuilder write=new StringBuilder();
			write.append("public static synchronized void write(java.lang.String line){\n");
			write.append("if(TestsTraces.fileName!=null){\n");
			write.append("PrintWriter out;\n");
			write.append("try {\n");
			write.append("out = new PrintWriter(new BufferedWriter(new FileWriter(TestsTraces.fileName, true)));\n");
			write.append("out.println(\"[inst2] + \"+line);\n");
			write.append("out.close();\n");
			write.append("} catch (IOException e) {\n");
			write.append("e.printStackTrace();\n");
			write.append("}\n");
			write.append("}\n");
			write.append("}\n");
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
	boolean myapp=s[0].equals("com") &&s[1].equals("mycompany") &&s[2].equals("app");
	if (myapp || eclipse) {

		String name=className.replace("/",".");
		name=name.split("$")[0];
		/*URL[] paths=((URLClassLoader)loader).getURLs();
		for (URL c : paths){
			System.out.println("URL: "+c.toString());
		}*/
        try { 

            ClassPool cp = ClassPool.getDefault();
    		
            CtClass cc = cp.get(name);                
            CtMethod[] methods = cc.getDeclaredMethods();
			if(!cc.isInterface()){
            for (CtMethod method : methods){

            	CtMethod m = cc.getDeclaredMethod(method.getName());
				if(m.isEmpty()){
					continue;
				}
            	String met=cc.getName()+"."+method.getName();

            	StringBuffer toInsert = new StringBuffer();

          		// Load trace writer class dynamically
            	toInsert.append("Class testsRunnerClass=null;");
            	toInsert.append("try{");
            	toInsert.append("	testsRunnerClass = Class.forName(\"TestsTraces\");");
            	toInsert.append("}catch(Exception exception){");
            	//toInsert.append("	System.out.println(\"exception1\");");
            	toInsert.append("	if(testsRunnerClass==null){");
				//D:\Amir_Almishali\agent\CDT_8_1_2\org.eclipse.cdt\core\org.eclipse.cdt.core.tests\target\classes
    			//toInsert.append("		URL classUrl = new URL(\"file:\\\\\\target\\\\classes\\\\\");");
    			toInsert.append("try{");
            	toInsert.append("		URL classUrl = new URL(\"file:///D:/Amir_Almishali/agent/CDT_8_1_2/org.eclipse.cdt/core/org.eclipse.cdt.core.tests/target/classes/\");");
    			toInsert.append("		URLClassLoader myLoader = URLClassLoader.newInstance(new URL[]{classUrl});");
    			//toInsert.append("		System.out.println(\"before load class \" + myLoader);");
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
            	try {
            		m.insertBefore(ins);
				}
				catch(Exception e){
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
			System.out.println(ex.getMessage());
        }
	}
	
	return byteCode;
}



public byte[] transform2(ClassLoader loader, String className, Class<?> classBeingRedefined,
        ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
   	
	this.initiate(className.replace("/","."),loader,protectionDomain);
	byte[] byteCode = classfileBuffer;

	String[] s=className.split("/");
	boolean eclipse=s[0].equals("org") &&s[1].equals("eclipse") &&s[2].equals("cdt");
	boolean myapp=s[0].equals("com") &&s[1].equals("mycompany") &&s[2].equals("app");
	if (myapp || eclipse) {

		String name=className.replace("/",".");
		name=name.split("$")[0];
		/*URL[] paths=((URLClassLoader)loader).getURLs();
		for (URL c : paths){
			System.out.println("URL: "+c.toString());
		}*/
        try { 

            ClassPool cp = ClassPool.getDefault();
    		
            CtClass cc = cp.get(name);                
            CtMethod[] methods = cc.getDeclaredMethods();
			if(!cc.isInterface()){
            for (CtMethod method : methods){

            	CtMethod m = cc.getDeclaredMethod(method.getName());
				if(m.isEmpty()){
					continue;
				}
            	String met=cc.getName()+"."+method.getName();

            	StringBuffer toInsert = new StringBuffer();

        		// If starting a new test, close previous file with trace of previous test
            	boolean isTestFunction = (cc.getName().contains("Test") && method.getName().startsWith("test"));
            	if(isTestFunction){
            		// Rename when finished past test
            		//toInsert.append("testsRunnerClass.getMethod(\"changefile\", cArg).invoke(null, params);");
            		//toInsert.append("TestsTraces.changefile(\""+met + "\");\n");
            		
            		toInsert.append("System.out.println(\"Try to change file +\" \" "+met+"\");");
            		toInsert.append(injectedClassName+".changefile(\""+met + "\");\n");
            		
            	}
            	                 	
            	// Print method to current trace file
            	//toInsert.append("testsRunnerClass.getMethod(\"write\", cArg).invoke(null, params);");              	
            	//toInsert.append("TestsTraces.write(\""+met + "\");\n");
            	toInsert.append("System.out.println(\"Try to write to file +\" \" "+met+"\");");
            	toInsert.append(injectedClassName+".write(\""+met + "\");\n");
            	
            	//String ins="System.out.println(\"[inst2] +\" \" "+met+"\");";                	
            	String ins=toInsert.toString();
            	try {
            		m.insertBefore(ins);
				}
				catch(Exception e){
				System.out.println("exception in trans2 insertBefore");
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
		System.out.println("exception in transform2");
            ex.printStackTrace();
			System.out.println(ex.getMessage());
        }
	}
	
	return byteCode;    	
}



/**
 * This is just a test 
 * Injecting to a static method functions to help us print traces out to a file
 * @param protectionDomain 
 * @param loader 
 */
public static void injectToMethod(ClassLoader loader, ProtectionDomain protectionDomain){
	ClassPool cp =ClassPool.getDefault();
	try {
		CtClass injectedClass= cp.get(injectedClassName);
		CtField fileNameField;			
		fileNameField = CtField.make("public static String fileName=null;", injectedClass);
		fileNameField.setModifiers(Modifier.PUBLIC | Modifier.STATIC);
		injectedClass.addField(fileNameField,"null");
		
		StringBuilder changeFile=new StringBuilder();
		changeFile.append("public static synchronized void changefile(java.lang.String newName){\n");
		changeFile.append("if("+injectedClassName+".fileName==null){\n");
		changeFile.append("long time= System.currentTimeMillis();\n");
		changeFile.append(""+injectedClassName+".fileName=\"..\\\\..\\\\DebuggerTests\\\\Trace_\"+newName+\"_\"+time+\".txt\";\n");
		changeFile.append("System.out.println(\"changed! \" +"+injectedClassName+".fileName);\n");
		changeFile.append("}\n");
		
		changeFile.append("}\n");
		CtMethod m=CtNewMethod.make(changeFile.toString(), injectedClass);
		m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
		injectedClass.addMethod(m);
		
		StringBuilder write=new StringBuilder();
		write.append("public static synchronized void write(java.lang.String line){\n");
		write.append("if("+injectedClassName+".fileName!=null){\n");
		write.append("PrintWriter out;\n");
		write.append("try {\n");
		write.append("out = new PrintWriter(new BufferedWriter(new FileWriter("+injectedClassName+".fileName, true)));\n");
		write.append("out.println(\"[inst2] + \"+line);\n");
		write.append("out.close();\n");
		write.append("} catch (IOException e) {\n");
		write.append("e.printStackTrace();\n");
		write.append("}\n");
		write.append("}\n");
		write.append("}\n");
		
		m=CtNewMethod.make(write.toString(), injectedClass);
		m.setModifiers(Modifier.PUBLIC | Modifier.STATIC | Modifier.SYNCHRONIZED);
		injectedClass.addMethod(m);
		
		injectedClass.writeFile();
		
		Method[] ms=injectedClass.toClass(loader,protectionDomain).getDeclaredMethods();
		/*for (Method m2 : ms){
			System.out.println("		method : "+m2.getName());
		}*/
		//traceWriterClass.writeFile("target\\classes");
		//traceWriterClass.toClass(this.getClass().getClassLoader(), this.getClass().getProtectionDomain());
		//gcp.addGeneratedClass(traceWriterClass); 
		//traceWriterClass.writeFile("target\\classes\\org\\eclipse\\cdt");
		
	} catch (Exception e) {
	System.out.println("exception in inject");
		e.printStackTrace();			
	}    	
}

public static void main(String[] args){
	Class testsRunnerClass=null;
	try{
		testsRunnerClass = Class.forName("TestsTraces");
	}catch(ClassNotFoundException exception){
		if(testsRunnerClass==null){
			URL classUrl=null;
			try {
				classUrl = new URL("target\\classes\\");
			} catch (MalformedURLException e) {
				
				e.printStackTrace();
			}
			try {
				testsRunnerClass = URLClassLoader.newInstance(new URL[]{classUrl}, String.class.getClassLoader()).loadClass("TestsTraces");
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
		}
	}
	
	String met="sssd";
	// Run
	try {
		testsRunnerClass.getMethod("changefile", String.class).invoke(null,met);
		testsRunnerClass.getMethod("write", String.class).invoke(null,met);
	} catch (Exception e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	
	System.out.println("end");
		
    	
    }


@Override
public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
        ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
	
	return nicerTransform(loader,className,classBeingRedefined,protectionDomain,classfileBuffer);
}
}