#Masson tissue coll selection macro
from ij import IJ, WindowManager
from ij.plugin.filter import Analyzer
from ij.plugin.frame import RoiManager
from ij.text import TextPanel
from ij.measure import ResultsTable
from ij.gui import DialogListener, GenericDialog
from ij.process import ImageConverter, AutoThresholder, ImageProcessor
from ij.gui import WaitForUserDialog
from loci.plugins.in import ImagePlusReader, ImporterOptions, ImportProcess
from loci.plugins import BF
from ij.io import OpenDialog
import time
import sys

#ROI set
rm=RoiManager().getInstance()
if (rm==None):
	rm = RoiManager()
	

IJ.run("Bio-Formats Importer", "open= IJ.getDirectory()" + "autoscale color_mode=Default view=Hyperstack stack_order=XYCZT")

# set image
imp = IJ.getImage()
dir = IJ.getDirectory("image")
ImageName=imp.getTitle()

IJ.run(imp, "RGB Color", "")
imp = IJ.getImage()
IJ.run(imp, "8-bit", "")
IJ.run("Threshold...", "Default")
WaitForUserDialog("Threshold","set threshold").show()
IJ.run(imp, "Create Selection", "")
rm.addRoi(imp.getRoi())
rm.select(0);
rm.runCommand("Rename", ImageName)
rm.runCommand(imp,"Deselect")


#Set image original
IJ.setTool("freehand")
WaitForUserDialog("draw to remove not tissue of interest").show()
rm.addRoi(imp.getRoi()) 		
rm.setSelectedIndexes([0,1])
rm.runCommand(imp,"OR")
rm.runCommand(imp,"XOR")
rm.addRoi(imp.getRoi())
rm.select(1)
rm.runCommand(imp,"Delete")
rm.runCommand(imp,"Deselect")
rm.select(1)
IJ.run(imp, "Fill", "slice")


#create masson area tissue
WaitForUserDialog("select original and run deconv, select masson coll stain").show() 
imp = IJ.getImage()
Name=imp.getTitle()
IJ.run(imp, "8-bit", "")
rm.runCommand(imp,"Deselect")
IJ.run("Threshold...", "Default")
WaitForUserDialog("Threshold","set threshold").show()
IJ.run(imp, "Create Selection", "")
rm.addRoi(imp.getRoi())
rm.setSelectedIndexes([0,1])
rm.runCommand(imp,"AND")
rm.addRoi(imp.getRoi())
rm.runCommand(imp,"Deselect")
rm.select(1)
rm.runCommand(imp,"Delete")

rm.select(1)
areamasson=str(int(imp.getStatistics().area))
rm.select(0)
areatissue=str(int(imp.getStatistics().area))
ratio= str(float(areamasson)/float(areatissue))


f = open(dir + 'Masson.csv','a')
if f.tell() == 0:
	f.write('Image Name\tTotal area\tMasson area\tRatio\n')
f.write(imp.getTitle() + '\t' + areatissue + '\t'+ areamasson + '\t' + ratio + '\n')
print imp.getTitle() + '\t' + areatissue + '\t'+ areamasson + '\t' + ratio 
	

IJ.run("Clear Results", "")
rm.runCommand("Save", dir + ImageName+".zip")	
IJ.run("Close All", "")
rm.reset()
f.close()
