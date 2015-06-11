package Deprecated;
import Implant.*;


public class Event {
	private String name;
	private String param;
	private String call_for_action;
	private boolean finished;
	
	/********************************
	 * Constructor.
	 * @param nam - event name.
	 * @param prm - event parameter.
	 * @param actn - action code.
	 ********************************/
	public Event(String nam, String prm, String actn){
		name = nam;
		param = prm;
		call_for_action = actn;
		finished = false;
	}
	
	
	/********************************
	 * Constructor.
	 * @param nam - event name.
	 ********************************/
	public Event(String nam){
		name = nam;
		param = "";
		call_for_action = "";
		finished = false;
	}
	
	
	/************************
	 * Name getter.
	 * @return event's name.
	 ************************/
	public String get_name(){
Logger.log("Event.get_name");
boolean _bug_switch = Bug_Switcher.has_bug("Event.get_name");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return name;
	}
	
	
	/**********************
	 * Action name getter.
	 * @return
	 **********************/
	public String get_action(){
Logger.log("Event.get_action");
boolean _bug_switch = Bug_Switcher.has_bug("Event.get_action");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return call_for_action;
	}
	
	
	/********************************************************************
	 * Checks if event needs to be terminated.
	 * @return True - if event need to be terminated. False - otherwise.
	 ********************************************************************/
	public boolean check_finished(){
Logger.log("Event.check_finished");
boolean _bug_switch = Bug_Switcher.has_bug("Event.check_finished");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

		return finished;
	}
	
	
	/*********************************************
	 * Marks the event as needs to be terminated.
	 *********************************************/
	public void mark_as_finished(){
Logger.log("Event.mark_as_finished");
boolean _bug_switch = Bug_Switcher.has_bug("Event.mark_as_finished");
if (_bug_switch)
	return;

		finished = true;
	}
	
	
	/*****************************
	 * parameter getter.
	 * @return event's parameter.
	 *****************************/
	public String get_param(){
Logger.log("Event.get_param");
boolean _bug_switch = Bug_Switcher.has_bug("Event.get_param");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

		return param;
	}
	
	
	/**********************************
	 * Calls for action.
	 * @param last_event - last event.
	 **********************************/
	public void call_for_action(Event last_event){
Logger.log("Event.call_for_action");
boolean _bug_switch = Bug_Switcher.has_bug("Event.call_for_action");
if (_bug_switch)
	return;

		 DDIC.do_action(call_for_action, this, last_event);
	}
}
