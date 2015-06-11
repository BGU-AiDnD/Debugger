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
package opennlp.maxent.quasinewton;
import Implant.*;


/**
 * class to store lineSearch result
 */
public class LineSearchResult {
  public static LineSearchResult getInitialObject(double valueAtX, double[] gradAtX, double[] x, int maxFctEval) {
Logger.log("LineSearchResult.getInitialObject");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getInitialObject");
if (_bug_switch)
	return null;

    return new LineSearchResult(0.0, 0.0, valueAtX, null, gradAtX, null, x, maxFctEval);
  }

  public static LineSearchResult getInitialObject(double valueAtX, double[] gradAtX, double[] x) {
Logger.log("LineSearchResult.getInitialObject");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getInitialObject");
if (_bug_switch)
	return null;

    return new LineSearchResult(0.0, 0.0, valueAtX, null, gradAtX, null, x, QNTrainer.DEFAULT_MAX_FCT_EVAL);
  }

  private int fctEvalCount;
  private double stepSize;
  private double valueAtCurr;
  private double valueAtNext;
  private double[] gradAtCurr;
  private double[] gradAtNext;
  private double[] currPoint;
  private double[] nextPoint;

  public LineSearchResult(double stepSize, double valueAtX, double valurAtX_1, 
      double[] gradAtX, double[] gradAtX_1, double[] currPoint, double[] nextPoint, int fctEvalCount) {
    this.stepSize = stepSize;
    this.valueAtCurr = valueAtX;
    this.valueAtNext = valurAtX_1;
    this.gradAtCurr = gradAtX;
    this.gradAtNext = gradAtX_1;
    this.currPoint = currPoint;
    this.nextPoint = nextPoint;
    this.setFctEvalCount(fctEvalCount);
  }

  public double getStepSize() {
Logger.log("LineSearchResult.getStepSize");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getStepSize");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

    return stepSize;
  }
  public void setStepSize(double stepSize) {
Logger.log("LineSearchResult.setStepSize");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setStepSize");
if (_bug_switch)
	return;

    this.stepSize = stepSize;
  }
  public double getValueAtCurr() {
Logger.log("LineSearchResult.getValueAtCurr");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getValueAtCurr");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

    return valueAtCurr;
  }
  public void setValueAtCurr(double valueAtCurr) {
Logger.log("LineSearchResult.setValueAtCurr");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setValueAtCurr");
if (_bug_switch)
	return;

    this.valueAtCurr = valueAtCurr;
  }
  public double getValueAtNext() {
Logger.log("LineSearchResult.getValueAtNext");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getValueAtNext");
double _bug_returned_val = 0.0;
if (_bug_switch)
	return _bug_returned_val;

    return valueAtNext;
  }
  public void setValueAtNext(double valueAtNext) {
Logger.log("LineSearchResult.setValueAtNext");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setValueAtNext");
if (_bug_switch)
	return;

    this.valueAtNext = valueAtNext;
  }
  public double[] getGradAtCurr() {
Logger.log("LineSearchResult.getGradAtCurr");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getGradAtCurr");
if (_bug_switch)
	return null;

    return gradAtCurr;
  }
  public void setGradAtCurr(double[] gradAtCurr) {
Logger.log("LineSearchResult.setGradAtCurr");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setGradAtCurr");
if (_bug_switch)
	return;

    this.gradAtCurr = gradAtCurr;
  }
  public double[] getGradAtNext() {
Logger.log("LineSearchResult.getGradAtNext");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getGradAtNext");
if (_bug_switch)
	return null;

    return gradAtNext;
  }
  public void setGradAtNext(double[] gradAtNext) {
Logger.log("LineSearchResult.setGradAtNext");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setGradAtNext");
if (_bug_switch)
	return;

    this.gradAtNext = gradAtNext;
  }
  public double[] getCurrPoint() {
Logger.log("LineSearchResult.getCurrPoint");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getCurrPoint");
if (_bug_switch)
	return null;

    return currPoint;
  }
  public void setCurrPoint(double[] currPoint) {
Logger.log("LineSearchResult.setCurrPoint");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setCurrPoint");
if (_bug_switch)
	return;

    this.currPoint = currPoint;
  }
  public double[] getNextPoint() {
Logger.log("LineSearchResult.getNextPoint");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getNextPoint");
if (_bug_switch)
	return null;

    return nextPoint;
  }
  public void setNextPoint(double[] nextPoint) {
Logger.log("LineSearchResult.setNextPoint");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setNextPoint");
if (_bug_switch)
	return;

    this.nextPoint = nextPoint;
  }
  public int getFctEvalCount() {
Logger.log("LineSearchResult.getFctEvalCount");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.getFctEvalCount");
int _bug_returned_val = 0;
if (_bug_switch)
	return _bug_returned_val;

    return fctEvalCount;
  }
  public void setFctEvalCount(int fctEvalCount) {
Logger.log("LineSearchResult.setFctEvalCount");
boolean _bug_switch = Bug_Switcher.has_bug("LineSearchResult.setFctEvalCount");
if (_bug_switch)
	return;

    this.fctEvalCount = fctEvalCount;
  }
}