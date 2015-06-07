package Deprecated;

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
		return name;
	}
	
	
	/**********************
	 * Action name getter.
	 * @return
	 **********************/
	public String get_action(){
		return call_for_action;
	}
	
	
	/********************************************************************
	 * Checks if event needs to be terminated.
	 * @return True - if event need to be terminated. False - otherwise.
	 ********************************************************************/
	public boolean check_finished(){
		return finished;
	}
	
	
	/*********************************************
	 * Marks the event as needs to be terminated.
	 *********************************************/
	public void mark_as_finished(){
		finished = true;
	}
	
	
	/*****************************
	 * parameter getter.
	 * @return event's parameter.
	 *****************************/
	public String get_param(){
		return param;
	}
	
	
	/**********************************
	 * Calls for action.
	 * @param last_event - last event.
	 **********************************/
	public void call_for_action(Event last_event){
		 DDIC.do_action(call_for_action, this, last_event);
	}
}
