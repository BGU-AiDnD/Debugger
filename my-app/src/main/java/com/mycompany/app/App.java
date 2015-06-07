package com.mycompany.app;

/**
 * Hello world!
 *
 */
public class App 
{

	public static void g()
	{
		System.out.println( "Hello g!" );
	}
	public static void f()
	{
		System.out.println( "Hello World!" );
		g();
	}
	
	
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
		f();
    }
}
