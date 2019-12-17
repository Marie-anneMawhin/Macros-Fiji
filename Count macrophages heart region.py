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

def runroi():
	IJ.setTool(3)
	gd = GenericDialog("Zone")
	gd.setModal(False)
	gd.addMessage("Define the region of interest")
	gd.addMessage("Select an area on the image")
	gd.showDialog()
	
	while not gd.wasOKed():
		if gd.wasCanceled():
			sys.exit(1)
		time.sleep(1)
	
def runmacroP():
	dir = IJ.getDirectory("image")
	rm=RoiManager().getInstance()
	#listROI=rm.getCount()
	
	imp = IJ.getImage()
	IJ.run(imp, "Set Scale...", "distance=1 known=0.65 pixel=1 unit=um")
	ImageConverter(imp).convertToGray8();
	IJ.run(imp, "Subtract Background...", "rolling=6")
	IJ.run(imp, "Mean...", "radius=2")
	
	for i in range(0,6):
		imp = IJ.getImage()
		rm.select(imp, i)
		areasize = str(int(imp.getStatistics().area))
		IJ.run("Duplicate...", " ")
		IJ.run("Clear Outside")	
		IJ.run("Threshold...", "Default")
		WaitForUserDialog("Threshold","set threshold").show()         

		imp=IJ.getImage()
		IJ.run(imp, "Convert to Mask", "")
		IJ.run(imp, "Options...", "iterations=3 count=2 do=Close")
		IJ.run(imp, "Analyze Particles...", "size=60-1000 pixel show=Masks display")
		imp=IJ.getImage()
		IJ.run(imp, "Create Selection", "")
		rm.addRoi(imp.getRoi())
		areacell=str(int(imp.getStatistics().area))
		rm.runCommand("Deselect")
		imp.close()
		imp.close()
		ImageName=imp.getTitle()
		imp = IJ.getImage()
		rt = ResultsTable().getResultsTable()
		rt.showRowNumbers(False)
		count = rt.getCounter()
	
		f = open(dir + 'CD68 count.csv','a')
		if f.tell() == 0:
			f.write('Image Name\tTotal area\tCell area\tCount\n')
	
		f.write(imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t'+ areacell + '\t' + str(count) + '\n')
		print imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t'+ areacell + '\t' + str(count) 
		f.close()
		imp.close()
		IJ.run("Clear Results", "")
		
	rm.runCommand("Save", dir + ImageName+".zip")	
	IJ.run("Close All", "")
	rm.reset()
	f.close()

def runwhole():
	imp = IJ.openImage()
	imp.show()
	IJ.run("Set Measurements...", "area redirect=None decimal=9")
	WaitForUserDialog("open ROIs").show();
	runmacroP()

while True:
	runwhole()

	gd = GenericDialog("Again?")
	gd.addMessage("Run again on another image?")
	gd.showDialog()
	if not gd.wasOKed():
		break