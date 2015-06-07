package inst;

import java.io.ByteArrayInputStream;  
import java.io.IOException;  
import java.io.InputStream;  
import java.net.MalformedURLException;  
import java.net.URL;  
import java.util.HashMap;  
  
import javassist.CannotCompileException;  
import javassist.ClassPath;  
import javassist.CtClass;  
import javassist.NotFoundException;  
  
public final class ClassPathForGeneratedClasses implements ClassPath {  
  
 public ClassPathForGeneratedClasses() {  
 super();  
 classes = new HashMap<String, InputStream>();  
 }  
  
 public void addGeneratedClass(CtClass generated) throws CannotCompileException {  
 try {  
 generated.stopPruning(true);  
 ByteArrayInputStream source = new ByteArrayInputStream(generated.toBytecode());  
 classes.put(generated.getName(), source);  
 generated.stopPruning(false);  
 } catch (IOException e) {  
 // should not happen  
 System.out.println("unexpected : " + e);  
 System.exit(1);  
 }  
 }  
  
 public void close() {  
 this.classes.clear();  
 }  
  
 public URL find(String classname) {  
 try {  
 String urlString = "file:/ClassPathForGeneratedClasses/" + classname;  
 URL result = (classes.containsKey(classname)) ? new URL(urlString) : null;  
 return result;  
 } catch (MalformedURLException e) {  
 return null;  
 }  
 }  
  
 public InputStream openClassfile(String classname) throws NotFoundException {  
 if (!classes.containsKey(classname)) {
 return null;  
 }  
 return classes.get(classname);  
 }  
  
 private HashMap<String, InputStream> classes;  

}  
