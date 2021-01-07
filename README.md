# Ginseng-Image-analysis

## About Ginseng Image Analysis
Ginseng Image Analysis is an open-source software for counting the infected regions of ginseng. The goal of this python tool is to provide a easy-to-use GUI for performing infected area analysis with no prior programming background. A simple pixel count is returned back to the user defining the region of infection.

## How to Use
You may run the tool from the command line or simply download the .exe file if you are not comfortable running python programs from the command line. Keep in mind python .exe files take a while to load as it must compile the code before running. Once the program has opened up you input your image file and click Analyze to proceed. Keep in mind the picture of each ginseng in the analysis should ideally be performed at the same height to ensure accurate comparsion between images. It is best to take the picture using the same camera and resolution for the course of your experiment.

The input image should now display on your screen. Once the image is displayed click on the top left of one infected region and drag until you meet the bottom right of the region. It is best to put this selection window as close around the region as possible. Once you unclick, the analysis begins and an output containing the pixel area will be displayed. Simply repeat the selection for each infected region in the image. 

## How it Works
Ginseng Image Analysis utilizes a python package called plantcv for image analysis. PlantCV is an imagine analysis software library containing multiple functions for assessing plant phenotypes.

## Citation
Fahlgren N, Feldman M, Gehan MA, Wilson MS, Shyu C, Bryant DW, Hill ST, McEntee CJ, Warnasooriya SN, Kumar I, Ficor T, Turnipseed S, Gilbert KB, Brutnell TP, Carrington JC, Mockler TC, Baxter I. (2015) A versatile phenotyping system and analytics platform reveals diverse temporal responses to water availability in Setaria. Molecular Plant 8: 1520-1535. http://doi.org/10.1016/j.molp.2015.06.005

## Issues
If each image in your experiment is not taken with the same camera, at the same height, or at the same lighting conditions varying results may be produced. Ideally, there will be a framework upon which a camera will be set up to take a picture at the same distance from the tray each time. The selection rectangle must be correctly aligned around the perimeter of the infected region.
