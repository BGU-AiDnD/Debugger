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


/**
 * A maxent predicate representation which we can use to sort based on the
 * outcomes. This allows us to make the mapping of features to their parameters
 * much more compact.
 */
public class ComparablePredicate implements Comparable<ComparablePredicate> {
  public String name;
  public int[] outcomes;
  public double[] params;

  public ComparablePredicate(String n, int[] ocs, double[] ps) {
    name = n;
    outcomes = ocs;
    params = ps;
  }

  public int compareTo(ComparablePredicate cp) {
Logger.log("ComparablePredicate.compareTo");
boolean _bug_switch = Bug_Switcher.has_bug("ComparablePredicate.compareTo");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

    int smallerLength = (outcomes.length > cp.outcomes.length?
        cp.outcomes.length : outcomes.length);

    for (int i=0; i<smallerLength; i++) {
      if (outcomes[i] < cp.outcomes[i]) return -1;
      else if (outcomes[i] > cp.outcomes[i]) return 1;
    }

    if (outcomes.length < cp.outcomes.length) return -1;
    else if (outcomes.length > cp.outcomes.length) return 1;

    return 0;
  }

  public String toString() {
Logger.log("ComparablePredicate.toString");
boolean _bug_switch = Bug_Switcher.has_bug("ComparablePredicate.toString");
String _bug_returned_val = "";
if (_bug_switch)
	return _bug_returned_val;

    StringBuilder s = new StringBuilder();
    for (int outcome : outcomes) {
      s.append(" ").append(outcome);
    }
    return s.toString();
  }

}
 
