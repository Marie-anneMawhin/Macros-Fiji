from ij import IJ, WindowManager
from ij.plugin.filter import Analyzer
from ij.measure import ResultsTable
from ij.gui import DialogListener, GenericDialog
from ij.process import ImageConverter, AutoThresholder
from ij.gui import WaitForUserDialog
from ij.plugin.frame import RoiManager
import time
import sys


class TListener (DialogListener):
	def dialogItemChanged(self, gd, event):
		th = gd.getNextNumber()
		#IJ.log("Something was changed: " + str(th))
		imp = IJ.getImage()
		#list = WindowManager.getIDList()
		#for i in list:
		#	imp = WindowManager.getImage(i)
		IJ.setThreshold(imp, th, 65535, "Red")
		return True

def runroi():
	IJ.setTool(3)
	gd = GenericDialog("Zone")
	gd.setModal(False)
	gd.addMessage("Define the region of interest")
	gd.addMessage("Select an area on the image")
	gd.showDialog()
	# ugly
	while not gd.wasOKed():
		if gd.wasCanceled():
			sys.exit(1)
		time.sleep(1)


def runregion():
	rm = RoiManager().getInstance()
	listROI=rm.getCount()
	dir = IJ.getDirectory("image")
	
	
	for i in range(listROI):
			
		imp = IJ.getImage()
		IJ.run("Duplicate...", " ")
		rm.select(i)
		rm.runCommand("Measure")
			
		ROIrt=Analyzer.getResultsTable()
		areasize=ROIrt.getRowAsString(i)
		IJ.run("Clear Outside")
		imp = IJ.getImage()
		
		IJ.run(imp, "Color Threshold...", "")
		WaitForUserDialog("Threshold","set and select threshold").show()
	
		IJ.run("Clear Outside")
		imp2 = imp.crop()
	
		ic = ImageConverter(imp)
		ic.convertToRGB()
		imp = IJ.getImage()
		ic = ImageConverter(imp)
		ic.convertToHSB()
	
		hue    = imp.getImageStack().getPixels(1)
		bright = imp.getImageStack().getPixels(3)
		nred = 0
		ngreen = 0

		for x, val in enumerate(hue):
			if bright[x] > 1:
				if val > 5 and val < 35:
					nred += 1
				if val > 35 and val < 100:
					ngreen += 1
	
	
	
		list = WindowManager.getIDList()
		f = open(dir + 'threshold-script-results RG HSV.csv', 'a')
		if f.tell() == 0:
		
			f.write('Image Name\tROI Size (Total)\t"Red" area\t"Green" area\tRatio\n')
	
		if ngreen == 0:
			ratio = 99999999
		else:
			ratio = float(nred)/float(ngreen)
		f.write(imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t' + str(nred) + '\t' + str(ngreen) + '\t' + str(ratio) + '\n')
		print imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t' + str(nred) + '\t' + str(ngreen) + '\t' + str(ratio) + '\n'
		f.close()
		imp.close()
	
	IJ.run("Close All", "")
	rm = RoiManager().getInstance()
	rm.reset()
	ROIrt=Analyzer.getResultsTable()
	ROIrt.reset()
			
def runwhole():
	
	imp = IJ.openImage()
	imp.show()
	
	# fix scale (for area size)
	IJ.run(imp, "Set Scale...", "distance=1 known=1 pixel=1 unit=unit")
	WaitForUserDialog("open ROIs").show() 
	runregion()

while True:
	runwhole()

	gd = GenericDialog("Again?")
	gd.addMessage("Run again on another image?")
	gd.showDialog()
	if not gd.wasOKed():
		break
