#Glom staining analysis of ratio plugin
from ij import IJ, WindowManager
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, GenericDialog
from loci.plugins import BF

import sys

def deconv():
	imp = IJ.getImage()	
	IJ.run(imp, "Colour Deconvolution", "vectors=[H DAB]")
	WaitForUserDialog("select image with staining of interest and click OK.").show() 
	imp = IJ.getImage()
	IJ.run(imp, "8-bit", "")
	rm.runCommand(imp,"Deselect")
	IJ.run("Threshold...", "Default")
	WaitForUserDialog("Threshold","set threshold").show()
	IJ.run(imp, "Create Selection", "")
	rm.addRoi(imp.getRoi())
	
	rm.select(0)
	rm.runCommand("Rename", ImageName + "Stain total")
	IJ.setTool("freehand")
	WaitForUserDialog("select composite image and click OK.").show()

def loopglom(numb, glom):
	""" Loop for analysis of unlimited number of glomeruli .

	Keyword arguments:
	numb -- number for glom and staining already analysed
	glom -- number of glom and staining already analysed. 
	"""

	IJ.setTool("freehand")
	IJ.setForegroundColor(0, 0, 255)
	
	while True:
		numb += 1
		Name = "Glom "+str(numb)
		glom += 1
		WaitForUserDialog("select glom and click OK.").show()
		rm.addRoi(imp.getRoi())
		rm.select(glom)
		area_glom = str(int(imp.getStatistics().area))
		rm.runCommand("Rename", Name )
		rm.runCommand(imp,"Deselect")
		rm.setSelectedIndexes([0,glom])
		rm.runCommand(imp,"AND")
		roiType = imp.getRoi()
		if roiType == None:
			rm.select(glom)
			rm.addRoi(imp.getRoi())
			rm.runCommand(imp,"Deselect")
		else:
			rm.addRoi(imp.getRoi())
		
		glom_stain = glom + 1
		rm.select(glom_stain)
		area_stain_glom = str(int(imp.getStatistics().area))
		rm.runCommand("Rename", "Stained "+Name)
		rm.runCommand(imp,"Deselect")
		rm.select(glom)
		IJ.run(imp, "Fill", "slice")
		glom += 1
		rm.runCommand(imp,"Deselect")
				
		float_ratio = float(area_stain_glom)/float(area_glom)
		if float_ratio == 1.0 :
			float_ratio = 0
		ratio = str(float_ratio)
		
		print dir
		f = open(dir + 'Results staining ratio.csv','a')
		if f.tell() == 0:
			f.write('Image Name\t Glom Name\t Glom area\t Glom Staining area\tRatio\n')
		f.write(imp.getTitle() + '\t' + Name +'\t' + area_glom + '\t' + area_stain_glom +'\t' + ratio + '\n')
		print imp.getTitle() + '\t' + Name +'\t' + area_glom + '\t' + area_stain_glom +'\t' + ratio
		f.close()
		
		gd = GenericDialog("Again?")
		gd.addMessage("More gloms?\nSo click OK.")
		gd.showDialog()
		if not gd.wasOKed():
			break
	
while True:

	WaitForUserDialog("Want to finish an analysis first? Open ROI and click OK. \nIf NOT click OK ").show() #Condition if image need to be re-open and analysis continue
	
	rm=RoiManager().getInstance()
	if rm==None:
		rm = RoiManager()
	listROI = rm.getCount()
	num_ROI = int(rm.getCount())
	
	IJ.run("Bio-Formats Importer", "open= IJ.getDirectory()" + "autoscale color_mode=Default view=Hyperstack stack_order=XYCZT")
	imp = IJ.getImage()
	ImageName=imp.getTitle()
	dir = IJ.getDirectory("image")
	IJ.run(imp, "RGB Color", "")
	imp = IJ.getImage()
	
	if num_ROI == 0:
		deconv()
		loopglom(0, 0)
		
	else:
		glom_ROI = int(listROI)-1
		numb_ROI = (int(listROI)-1)/2
		for i in range(1, listROI, 2):
			rm.select(i)
   			IJ.run(imp, "Fill", "slice")
   
		loopglom(numb_ROI, glom_ROI)
			
	IJ.run("Clear Results", "")
	rm.runCommand("Save", dir + "RoiSet "+ ImageName +".zip")	
	IJ.run("Close All", "")
	rm.reset()
		
	gd = GenericDialog("Again?")
	gd.addMessage("Run on another image again")
	gd.showDialog()
	if  gd.wasCanceled():
		break

		