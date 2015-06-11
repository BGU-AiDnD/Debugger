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
 * A wrapper to turn EventCollectors created for Maxent 1.0 into EventStreams
 * for Maxent 1.2.  For efficiency, it would be best to convert your
 * EventCollector into a EventStream directly, but this will allow your
 * application to work with Maxent 1.2 with very little recoding.
 */
public final class EventCollectorAsStream extends AbstractEventStream {
  final Event[] events;
  final int numEvents;
  int index = 0;

  public EventCollectorAsStream(EventCollector ec) {
    events = ec.getEvents(false);
    numEvents = events.length;
  }

  public Event next() {
Logger.log("EventCollectorAsStream.next");
boolean _bug_switch = Bug_Switcher.has_bug("EventCollectorAsStream.next");
if (_bug_switch)
	return null;

    return events[index++];
  }

  public boolean hasNext() {
Logger.log("EventCollectorAsStream.hasNext");
boolean _bug_switch = Bug_Switcher.has_bug("EventCollectorAsStream.hasNext");
boolean _bug_returned_val = false;
if (_bug_switch)
	return _bug_returned_val;

    return (index < numEvents);
  }

}
