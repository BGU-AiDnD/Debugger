package opennlp.maxent.io;
import Implant.*;


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
import java.io.IOException;
import java.io.ObjectOutputStream;

import opennlp.model.AbstractModel;

public class ObjectQNModelWriter extends QNModelWriter {

  protected ObjectOutputStream output;
  
  /**
   * Constructor which takes a GISModel and a ObjectOutputStream and prepares
   * itself to write the model to that stream.
   *
   * @param model The GISModel which is to be persisted.
   * @param dos The stream which will be used to persist the model.
   */
  public ObjectQNModelWriter(AbstractModel model, ObjectOutputStream dos) {
    super(model);
    output = dos;
  }

  public void writeUTF(String s) throws IOException {
Logger.log("ObjectQNModelWriter.writeUTF");
boolean _bug_switch = Bug_Switcher.has_bug("ObjectQNModelWriter.writeUTF");
if (_bug_switch)
	return;

    output.writeUTF(s);
  }

  public void writeInt(int i) throws IOException {
Logger.log("ObjectQNModelWriter.writeInt");
boolean _bug_switch = Bug_Switcher.has_bug("ObjectQNModelWriter.writeInt");
if (_bug_switch)
	return;

    output.writeInt(i);
  }

  public void writeDouble(double d) throws IOException {
Logger.log("ObjectQNModelWriter.writeDouble");
boolean _bug_switch = Bug_Switcher.has_bug("ObjectQNModelWriter.writeDouble");
if (_bug_switch)
	return;

    output.writeDouble(d);
  }

  public void close() throws IOException {
Logger.log("ObjectQNModelWriter.close");
boolean _bug_switch = Bug_Switcher.has_bug("ObjectQNModelWriter.close");
if (_bug_switch)
	return;

    output.flush();
    output.close();
  }
}
