from ij import IJ, WindowManager
from ij.plugin.filter import Analyzer
from ij.measure import ResultsTable
from ij.gui import DialogListener, GenericDialog
from ij.process import ImageConverter, AutoThresholder
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
	gd.addSlider("Min threshold", 0, maxi, 1)
	gd.addDialogListener(TListener())
	gd.showDialog()

def runwhole():
	imp = IJ.openImage()
	imp.show()
	dir = IJ.getDirectory("image")
	
	# fix scale (for area size)
	IJ.run(imp, "Set Scale...", "distance=1 known=1 pixel=1 unit=unit");
	
	runroi()
	
	imp = IJ.getImage()
	roi = imp.getRoi()
	if roi is None:
		sys.exit(1)
	areasize = str(int(imp.getStatistics().area))
	IJ.run("Clear Outside")
	IJ.run("Split Channels")
	maxi = 0
	imp = IJ.getImage()
	if 'C3-' in imp.getTitle()[0:3] or 'blue' in imp.getTitle()[-10:-1]:
			imp.close()
		
	list = WindowManager.getIDList()
	#print list
	for i in list:
		imp = IJ.getImage()
		maxi = imp.getStatistics().max
		runthreshold(maxi)
		WindowManager.getImage(i)
		f = open(dir + 'threshold-RG-script-results.csv', 'a')
		if f.tell() == 0:
		# print header
			f.write('Image Name\tROI Size (Total)\tROI Size (above threshold)\n')
		imp = IJ.getImage()
		rt = ResultsTable()
		rt.showRowNumbers(False)
		a = Analyzer(imp, 279, rt)
		a.measure()
		f.write(imp.getTitle() + '\t' + areasize + '\t' + rt.getStringValue(0,0) + '\n')
		print imp.getTitle() + '\t' + areasize + '\t' + rt.getStringValue(0,0)
	
		imp.close()
	
	
	f.close()
	
	

while True:
	runwhole()

	gd = GenericDialog("Again?")
	gd.addMessage("Run again on another image?")
	gd.showDialog()
	if not gd.wasOKed():
		break
