#zone macro
from ij import IJ, WindowManager
from ij.plugin.filter import Analyzer
from ij.plugin.frame import RoiManager
from ij.text import TextPanel
from ij.measure import ResultsTable
from ij.gui import DialogListener, GenericDialog
from ij.process import ImageConverter, AutoThresholder
from ij.gui import WaitForUserDialog

import time
import sys

rm=RoiManager().getInstance()
if (rm==None):
	rm = RoiManager()

imp=IJ.getImage()
		
IJ.setTool("polygon");
rm.select(0);
rm.runCommand(imp,"Deselect");
rm.runCommand(imp,"Fill");
WaitForUserDialog("draw").show() 
rm.addRoi(imp.getRoi());
rm.select(1);
rm.addRoi(imp.getRoi());
rm.runCommand(imp,"Show All");
rm.select(2);
WaitForUserDialog("draw").show() 
rm.select(1);
rm.addRoi(imp.getRoi());
rm.select(3);
WaitForUserDialog("draw").show() 
rm.runCommand(imp,"Update");
rm.addRoi(imp.getRoi());
rm.select(4);
WaitForUserDialog("draw").show() 
rm.runCommand(imp,"Update");
rm.addRoi(imp.getRoi());
rm.select(5);
WaitForUserDialog("draw").show() 
rm.setSelectedIndexes([0,1]);
rm.runCommand(imp,"AND");
rm.addRoi(imp.getRoi());
rm.select(6);
rm.runCommand("Rename", "IVS");
rm.setSelectedIndexes([0,2]);
rm.runCommand(imp,"AND");
rm.addRoi(imp.getRoi());
rm.select(7);
rm.runCommand("Rename", "RV");
rm.setSelectedIndexes([0,3]);
rm.runCommand(imp,"AND");
rm.addRoi(imp.getRoi());
rm.select(8);
rm.runCommand("Rename", "LVPW");
rm.setSelectedIndexes([0,4]);
rm.runCommand(imp,"AND");
rm.addRoi(imp.getRoi());
rm.select(9)
rm.runCommand("Rename", "Lateral")
rm.setSelectedIndexes([0,5])
rm.runCommand(imp,"AND")
rm.addRoi(imp.getRoi())
rm.select(10)
rm.runCommand("Rename", "LVAW")
rm.setSelectedIndexes([1,2,3,4,5])
rm.runCommand(imp,"Delete")
rm.runCommand("Deselect")
dir = IJ.getDirectory("image")
ImageName=imp.getTitle()
rm.runCommand("Save", dir + ImageName+".zip")
rm.runCommand(imp,"Delete");
IJ.setTool("freehand");
imp.close();