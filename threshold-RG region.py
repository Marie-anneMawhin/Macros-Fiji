from ij import IJ, WindowManager
from ij.plugin.filter import Analyzer
from ij.measure import ResultsTable
from ij.gui import DialogListener, GenericDialog, WaitForUserDialog, Roi
from ij.process import ImageConverter, AutoThresholder
from ij.plugin.frame import RoiManager
import time
import sys


class TListener (DialogListener):
	def dialogItemChanged(self, gd, event):
		th = gd.getNextNumber()
		#IJ.log("Something was changed: " + str(th))
		imp = IJ.getImage()
		list = WindowManager.getIDList()
		for i in list:
			imp = WindowManager.getImage(i)
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

def runthreshold(maxi):
	gd = GenericDialog("Threshold")
	gd.addMessage("Adjust threshold's min limit (0 - %d):" % maxi)
	gd.addSlider("Min threshold", 0, maxi, 30)
	gd.addDialogListener(TListener())
	gd.showDialog()

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
		IJ.run("Split Channels")
		maxi = 0
		imp = IJ.getImage()
		
		if 'C3-' in imp.getTitle()[0:3] or 'blue' in imp.getTitle()[-10:-1]:
				imp.close()

		listchannel = ['green' in imp.getTitle()[-10:-1], 'red' in imp.getTitle()[-10:-1]]
				
		for n in listchannel:
			imp = IJ.getImage()
			maxi = imp.getStatistics().max
			runthreshold(maxi)
			WindowManager.getImage(n)
			
			f = open(dir + 'threshold-RG-script-results.csv', 'a')
			if f.tell() == 0:
			
				f.write('Image Name\tROI Size (Total)\tROI Size (above threshold)\n')
			imp = IJ.getImage()
			rt = ResultsTable()
			rt.showRowNumbers(False)
			a = Analyzer(imp, 279, rt)
			a.measure()
			f.write(imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t' + rt.getStringValue(0,0) + '\n')
			print imp.getTitle() + '\t' + rm.getName(i) + '\t' + areasize + '\t' + rt.getStringValue(0,0)
			imp.close()	
			f.close()
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
