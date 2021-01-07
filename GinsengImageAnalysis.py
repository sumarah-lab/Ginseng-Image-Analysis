import PySimpleGUI as sg
import random
import string
import cv2 as cv
from plantcv import plantcv as pcv
import numpy as np
import csv

def draw_rectangle(start=None, end=None):
	"""
	Displays selection rectangle on top of image file (requires the image to be redrawn each time)
	
	Parameters
	----------
	start : tuple
		X,Y coordinates of the starting point of the selection rectangle
	end : tuple
		X,Y coordinates of the ending point of the selection rectangle
	"""
	
	if start is not None and end is not None:
		graph.DrawImage(data=imgbytes, location=(0, 0))
		graph.draw_rectangle(start,end, line_color='white')

def draw_plot(x_start, y_start, x_end, y_end):
	"""
		Utilizes plantcv (citation below) to count the green pixels (Chlorophyll) of wells containg plants in a 4x6 grid format of the selected tray.
		
		Outputs
		-------
		A csv file containing the green pixel count for each well containing plants within the grid 
		
		Parameters
		----------
		x_start : int
			Contains the x coordinate of the top left of the user selection
		y_start : int
			Contains the y coordinate of the top left of the user selection
		x_end : int
			Contains the x coordinate of the bottom right of the user selection
		y_end : int
			Contains the y coordinate of the bottom right of the user selection
		
		Citation
		--------
		Fahlgren N, Feldman M, Gehan MA, Wilson MS, Shyu C, Bryant DW, Hill ST, McEntee CJ, Warnasooriya SN, Kumar I, Ficor T, Turnipseed S, Gilbert KB, Brutnell TP, Carrington JC, Mockler TC, Baxter I. (2015) A versatile phenotyping system and analytics platform reveals diverse temporal responses to water availability in Setaria. Molecular Plant 8: 1520-1535. http://doi.org/10.1016/j.molp.2015.06.005
		
		Website Link
		------------
		https://plantcv.readthedocs.io/en/stable/
	"""
	
	# Resize x,y values from the resized image to the initial raw image x,y coordinates for an accurate count on pixels
	x_start = x_start * img_width/dim[0]
	y_start = y_start * img_height/dim[1]
	x_end = x_end * img_width/dim[0]
	y_end = y_end * img_height/dim[1]
	
	# Crop raw image to selection window
	cropped = pcv.crop(img, x=int(x_start), y=int(y_start), h=int(y_end-y_start), w=int(x_end-x_start))
	
	# Debug code to display cropped image. Uncomment to see cropped window
	#cropbytes = cv.imencode('.png', cropped)[1].tobytes()
	#graph.DrawImage(data=cropbytes, location=(0, 0))
	
	
		
	# Utilize plantcv code to count green pixels within selection window
	# For further information see : https://plantcv.readthedocs.io/en/latest/multi-plant_tutorial/
	s = pcv.rgb2gray_hsv(rgb_img=cropped, channel='v')
	s_thresh = pcv.threshold.binary(gray_img=s, threshold=95, max_value=255, object_type='dark')
	ab_fill = pcv.fill(bin_img=s_thresh, size=4000) #good at 1000 too
	masked = pcv.apply_mask(cropped, mask=s_thresh, mask_color='white')
	id_objects, obj_hierarchy = pcv.find_objects(masked, ab_fill)
	roi1, roi_hierarchy= pcv.roi.rectangle(img=masked, x=int(cropped.shape[1]/2), y=int(cropped.shape[0]/2), h=100, w=100)
	roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=cropped, roi_contour=roi1, 
                                                                   roi_hierarchy=roi_hierarchy, 
                                                                   object_contour=id_objects, 
                                                                   obj_hierarchy=obj_hierarchy,
                                                                   roi_type='partial')
	infected_area = obj_area #includes plug in values for pictures with gel plug still intact
	
	sg.Popup('Finished Analysis! Pixel Area: %d' %(infected_area))
	
def image_analysis(input_image):
	"""
	Displays the image and waits for the user to select a rectangle around the tray.
	
	Parameters
	----------
	input_image : str
		The name of the image file in png format
	"""
	
	global layout_image
	global graph
	global imgbytes
	global img
	global img_width
	global img_height 
	global dim
	global filename
	
	# Grab window size to display the image of the appropriate height/width
	win_width, win_height = sg.Window.get_screen_size()
	
	# Leave a 100 pixel gap for text and button
	print(int(np.round(win_height*0.15)))
	win_height = win_height - int(np.round(win_height*0.15)) #100
	win_ratio = win_width/(win_height)

	# Set layout to contain the image as a pysimplegui graph, followed by text
	layout_image = [
		[
			sg.Graph(
				canvas_size=(win_width, win_height),
				graph_bottom_left=(0, win_height),
				graph_top_right=(win_width, 0),
				key="graph",
				enable_events=True,
				drag_submits=True,
				change_submits=True
			)
		],[
			sg.Text("", key="info", size=(80,1),font=("Helvetica", 20))
		],[
			sg.Button('Perform another Analysis?',font=("Helvetica",20)), sg.Exit()
		]
	]

	# Need keyboard events to be recorded
	window = sg.Window("rect on image",return_keyboard_events=True).Layout(layout_image)
	window.Finalize()
	window.Maximize()

	graph = window.Element("graph")
	
	# Read the image into plantcv for analysis
	img, path, filename = pcv.readimage(filename=input_image, mode='rgb')

	# Resize img to specific window size
	img_width = img.shape[1]
	img_height = img.shape[0]
	img_ratio = img_width/img_height

	# Resize image according to window dimensions
	if (win_ratio > img_ratio):
		dim = (int(img_width * (win_height/img_height)), win_height)
		resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
		print('first')
	else:
		dim = (win_width, int(img_height*(win_width/img_width)))
		print(dim)
		resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)

	# Convert cv2 image code to imen code for displaying using graph.DrawImage
	imgbytes = cv.imencode('.png', resized)[1].tobytes()
	graph.DrawImage(data=imgbytes, location=(0, 0))

	# Set dragging to false until user left clicks
	dragging = False
	start_point, end_point = None, None

	while True:
		# Timeout needs to be higher otherwise selection rectangle slows everything down
		event, values = window.read(timeout=100)
		
		info  = window.Element("info")
		info.Update(value="Please select the tray.")
		
		
		if event == 'Perform another Analysis?':
			window.Close()
			main()
		
		
		print(event)
		if event is None:
			break # exit

		# Wait for user input in graph (left click)
		if event == "graph":
			x,y = values["graph"]
			
			if not dragging:
				start_point = (x,y)
				dragging = True
			# When dragging stops record end point
			else:
				end_point = (x,y)
			
			# Ccontinuously draw rectangle for selection window
			draw_rectangle(start=start_point, end=end_point)
		
		# Wait for user to stop clicking left mouse
		elif event.endswith('+UP'):
			end_point = (x,y)
			dragging = False
			
			# Draw final selection window
			draw_rectangle(start=start_point, end=end_point)
			
			# Calculate green pixels using PlantCV
			draw_plot(start_point[0], start_point[1], end_point[0], end_point[1])
			
	window.close()
	
def main():
	"""
	Displays GUI window for inputting required files.
	
	Input Image : Desired png file to undergo green pixel analysis
	"""
	
	layout = [[sg.Text('Plant Image Analysis')],
              [sg.Text('Input Image', size=(18, 1)), sg.InputText(), sg.FileBrowse()],
              [sg.Button('Analyze'), sg.Exit()]]
			  
	
	# Display window and wait for user input
	window = sg.Window('Plant Image Analysis', layout)
	while True:
		event, values = window.Read()
		
		if event is None or event == 'Exit':
			break
		if event == 'Analyze':
			# Grab the input files from the from the input file window
			input_image = values[0]
			if not (input_image.endswith('.JPG')):
				sg.Popup('Please input a JPG file!')
			else:
					# Close file input window and open the image analysis window 
					window.Close()
					image_analysis(input_image)

main()	