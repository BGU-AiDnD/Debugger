/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package opennlp.model;
import Implant.*;


import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;


/**
 * Abstract class for collecting event and context counts used in training. 
 *
 */
public abstract class AbstractDataIndexer implements DataIndexer {

  private int numEvents;
  /** The integer contexts associated with each unique event. */ 
  protected int[][] contexts;
  /** The integer outcome associated with each unique event. */ 
  protected int[] outcomeList;
  /** The number of times an event occured in the training data. */
  protected int[] numTimesEventsSeen;
  /** The predicate/context names. */
  protected String[] predLabels;
  /** The names of the outcomes. */
  protected String[] outcomeLabels;
  /** The number of times each predicate occured. */
  protected int[] predCounts;

  public int[][] getContexts() {
Logger.log("AbstractDataIndexer.getContexts");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getContexts");
if (_bug_switch)
	return null;

    return contexts;
  }

  public int[] getNumTimesEventsSeen() {
Logger.log("AbstractDataIndexer.getNumTimesEventsSeen");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getNumTimesEventsSeen");
if (_bug_switch)
	return null;

    return numTimesEventsSeen;
  }

  public int[] getOutcomeList() {
Logger.log("AbstractDataIndexer.getOutcomeList");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getOutcomeList");
if (_bug_switch)
	return null;

    return outcomeList;
  }

  public String[] getPredLabels() {
Logger.log("AbstractDataIndexer.getPredLabels");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getPredLabels");
if (_bug_switch)
	return null;

    return predLabels;
  }

  public String[] getOutcomeLabels() {
Logger.log("AbstractDataIndexer.getOutcomeLabels");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getOutcomeLabels");
if (_bug_switch)
	return null;

    return outcomeLabels;
  }
  
  

  public int[] getPredCounts() {
Logger.log("AbstractDataIndexer.getPredCounts");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getPredCounts");
if (_bug_switch)
	return null;

    return predCounts;
  }

  /**
   * Sorts and uniques the array of comparable events and return the number of unique events.
   * This method will alter the eventsToCompare array -- it does an in place
   * sort, followed by an in place edit to remove duplicates.
   *
   * @param eventsToCompare a <code>ComparableEvent[]</code> value
   * @return The number of unique events in the specified list.
   * @since maxent 1.2.6
   */
  protected int sortAndMerge(List<ComparableEvent> eventsToCompare, boolean sort) {
Logger.log("AbstractDataIndexer.sortAndMerge");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.sortAndMerge");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

    int numUniqueEvents = 1;
    numEvents = eventsToCompare.size();
    if (sort) {
      Collections.sort(eventsToCompare);
      if (numEvents <= 1) {
        return numUniqueEvents; // nothing to do; edge case (see assertion)
      }

      ComparableEvent ce = eventsToCompare.get(0);
      for (int i = 1; i < numEvents; i++) {
        ComparableEvent ce2 = eventsToCompare.get(i);

        if (ce.compareTo(ce2) == 0) { 
          ce.seen++; // increment the seen count
          eventsToCompare.set(i, null); // kill the duplicate
        }
        else {
          ce = ce2; // a new champion emerges...
          numUniqueEvents++; // increment the # of unique events
        }
      }
    }
    else {
      numUniqueEvents = eventsToCompare.size();
    }
    if (sort) System.out.println("done. Reduced " + numEvents + " events to " + numUniqueEvents + ".");

    contexts = new int[numUniqueEvents][];
    outcomeList = new int[numUniqueEvents];
    numTimesEventsSeen = new int[numUniqueEvents];

    for (int i = 0, j = 0; i < numEvents; i++) {
      ComparableEvent evt = eventsToCompare.get(i);
      if (null == evt) {
        continue; // this was a dupe, skip over it.
      }
      numTimesEventsSeen[j] = evt.seen;
      outcomeList[j] = evt.outcome;
      contexts[j] = evt.predIndexes;
      ++j;
    }
    return numUniqueEvents;
  }
  
  
  public int getNumEvents() {
Logger.log("AbstractDataIndexer.getNumEvents");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getNumEvents");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

    return numEvents;
  }
  
  /**
   * Updates the set of predicated and counter with the specified event contexts and cutoff. 
   * @param ec The contexts/features which occur in a event.
   * @param predicateSet The set of predicates which will be used for model building.
   * @param counter The predicate counters.
   * @param cutoff The cutoff which determines whether a predicate is included.
   */
   protected static void update(String[] ec, Set<String> predicateSet, Map<String,Integer> counter, int cutoff) {
Logger.log("AbstractDataIndexer.update");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.update");
if (_bug_switch)
	return;

     for (String s : ec) {
       Integer i = counter.get(s);
       if (i == null) {
         counter.put(s, 1);
       }
       else {
         counter.put(s, i + 1);
       }
       if (!predicateSet.contains(s) && counter.get(s) >= cutoff) {
         predicateSet.add(s);
       }
     }
  }

  /**
   * Utility method for creating a String[] array from a map whose
   * keys are labels (Strings) to be stored in the array and whose
   * values are the indices (Integers) at which the corresponding
   * labels should be inserted.
   *
   * @param labelToIndexMap a <code>TObjectIntHashMap</code> value
   * @return a <code>String[]</code> value
   * @since maxent 1.2.6
   */
  protected static String[] toIndexedStringArray(Map<String,Integer> labelToIndexMap) {
Logger.log("AbstractDataIndexer.toIndexedStringArray");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.toIndexedStringArray");
if (_bug_switch)
	return null;

    final String[] array = new String[labelToIndexMap.size()];
    for (String label : labelToIndexMap.keySet()) {
      array[labelToIndexMap.get(label)] = label;
    }
    return array;
  }

  public float[][] getValues() {
Logger.log("AbstractDataIndexer.getValues");
boolean _bug_switch = Bug_Switcher.has_bug("AbstractDataIndexer.getValues");
if (_bug_switch)
	return null;

    return null;
  }
}