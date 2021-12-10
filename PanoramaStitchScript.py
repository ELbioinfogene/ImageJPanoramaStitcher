'''imageJ-python macro
Panorama Stitcher-
inputs a folder of N images that are then pairwise stitched to make a panorama
Eric Larsen 2021
WORKING 12/10/2021'''

#IMAGEJ ONLY
from ij import IJ
#Import Python Dependencies
#note: jython only supports default python libraries
import os

#Ask user for folder
ImageDir = IJ.getDir("Choose Folder of Images to Stitch")

PANO_STATE = 0
#OS walk through ImageDir
for foldername, subfolder, filename in os.walk(ImageDir):
	for INDEX,NAME in enumerate(filename):
		if INDEX==0:
			#open 1st and 2nd images, then use IJ.run() to pairwise stitch them into BASE0
			IMG1 = IJ.openImage('{}\\{}'.format(foldername,NAME))
			IMG2 = IJ.openImage('{}\\{}'.format(foldername,filename[INDEX+1]))
			IMG1.show()
			IMG2.show()
			#use MACRO RECORD tool to manually perform an action and determine what this string looks like
			STITCH_INPUTS = 'first_image={} second_image={} fusion_method=[Linear Blending] fused_image=BASE{} check_peaks=5 compute_overlap'.format(IMG1.getTitle(),IMG2.getTitle(),PANO_STATE)
			IJ.run('Pairwise stitching',STITCH_INPUTS)

		if INDEX>=2:
			#open Nth image to make an additional BASE
			IMG_N = IJ.openImage('{}\\{}'.format(foldername,NAME))
			IMG_N.show()
			STITCH_INPUTS = 'first_image=BASE{} second_image={} fusion_method=[Linear Blending] fused_image=BASE{} check_peaks=5 compute_overlap'.format(PANO_STATE,IMG_N.getTitle(),PANO_STATE+1)
			IJ.run('Pairwise stitching',STITCH_INPUTS)
			PANO_STATE = PANO_STATE+1

print('Pairwise Stitched {} images into {} panoramas'.format(INDEX+1,PANO_STATE+1))

#leave all BASE images open for the user to review in case the stitching algo makes a mistake at one step
#save final BASE as OUTPUT_PAN.png