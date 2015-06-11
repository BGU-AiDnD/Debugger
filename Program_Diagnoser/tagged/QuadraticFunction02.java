/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package opennlp.maxent.quasinewton;
import Implant.*;


/**
 * sample function for unit tests of LineSearch
 */
public class QuadraticFunction02 implements DifferentiableFunction {
  public double valueAt(double[] x) {
Logger.log("QuadraticFunction02.valueAt");
boolean _bug_switch = Bug_Switcher.has_bug("QuadraticFunction02.valueAt");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

    // -x^2;
    return Math.pow(x[0], 2) * -1;	
  }

  public double[] gradientAt(double[] x) {
Logger.log("QuadraticFunction02.gradientAt");
boolean _bug_switch = Bug_Switcher.has_bug("QuadraticFunction02.gradientAt");
if (_bug_switch)
	return null;

    // -2x
    return new double[] {-2.0 * x[0]};
  }

  public int getDomainDimension() {
Logger.log("QuadraticFunction02.getDomainDimension");
boolean _bug_switch = Bug_Switcher.has_bug("QuadraticFunction02.getDomainDimension");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

    return 1;
  }
}