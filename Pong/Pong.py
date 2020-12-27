#Libraries
import cv2
import numpy as np
#Screenshots 
import mss
import mss.tools
#Android connection protocol
from ppadb.client import Client
# Threading is required to control the wall under a parallel process
import threading

#Connect Android Phone
Client = Client(host='127.0.0.1', port=5037)
Phones = Client.devices()
Phone = Phones[0]

#Initial position of the wall
wall_x = 838
wall_y = 252
wall_min_y = 27
wall_max_y = 475
ball_pos = 252

Run = True

# Defining the function to control the wall
def move_wall():
	global wall_y

	while Run:
		# As the size of the monitor is not the same of my phone screen, a adjustment factor is required.
		Factor  = 1.33
		move = ball_pos*Factor
		if ball_pos < wall_min_y:
			move = wall_min_y
		if ball_pos > wall_max_y:
			move = wall_max_y

		x1 = wall_x*1.33
		y1 = wall_y*Factor
		x2 = wall_x*1.33
		y2 = move
		# Shell command to the phone
		Phone.shell(f'input touchscreen swipe {x1} {y1} {x2} {y2} 55')

# Starting the threading
t = threading.Thread(target=move_wall)
t.start()


sct = mss.mss()
#Position of the window to monitor through mss
monitor = {"top": 70, "left": 10, "width": 900, "height": 520}

while(1):
	# taking screenshots of the monitor
	img = sct.grab(monitor)
	img = np.array(img)
	#Set the initial and final points to draw a black rectangle on the screen
	# this will cover the score on the top screen to avoid confusions on the computer vision
	StartPoint = (400, 55)
	EndPoint = (480,140)
	Color = (0,0,0)

	#initial and final points for the movement range of the wall 
	p1 = (838,27)
	p2 = (870, 475)

	#initial and final points to cover the skpeaker symbol 
	s1 = (45,50)
	s2 = (105, 100)

	#initial and final points to cover the thropy symbol
	t1 = (810,280)
	t2 = (838, 330)

	#Draw the rectangles
	cv2.rectangle(img,p1,p2,(0,0,255))
	cv2.rectangle(img,s1,s2,Color,-1)
	cv2.rectangle(img,t1,t2,Color,-1)
	cv2.rectangle(img, StartPoint, EndPoint, Color, -1)
	
	#Change color space needed to use OpenCV
	GrayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	GrayBlurred = cv2.blur(GrayImg, (3,3))

	#Detecting the circle
	DetectedCircles = cv2.HoughCircles(
		GrayBlurred,
		cv2.HOUGH_GRADIENT,
		1,
		100,
		param1=50,
		param2=25,
		minRadius=5,
		maxRadius=40) 

	#Circle detection
	if DetectedCircles is not None:
		DetectedCircles = np.uint16(np.around(DetectedCircles))

		# Once a circle is detected, return the circle position
		for o in DetectedCircles[0, :]:
			x,y,r = o[0],o[1],o[2]
			cv2.circle(img, (x,y),r,(0,255,0),5)
			ball_pos = y

	cv2.imshow('Output', img)
	#Show image
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()  
		Run = False
		break