
#--------------------------------------------------------------------
# Libraries
#--------------------------------------------------------------------

from ppadb.client import Client
import numpy as np
import time
import mss
import mss.tools

#--------------------------------------------------------------------
# Function defining the tap, the function sends shell events type "sendevent"
# which are faster than input
#---------------------------#-------------------------------------------------------------------------------------------------------------
def tap(dir):
	Phone.shell('sendevent /dev/input/event2 3 57 0')
	if dir == 0:
		Phone.shell('sendevent /dev/input/event2 3 53 178')
	elif dir == 1:
		Phone.shell('sendevent /dev/input/event2 3 53 538')
	Phone.shell('sendevent /dev/input/event2 3 54 600')
	Phone.shell('sendevent /dev/input/event2 3 58 1')
	Phone.shell('sendevent /dev/input/event2 3 49 0')
	Phone.shell('sendevent /dev/input/event2 0 0 0')
	# Tap duration in seconds
	time.sleep(0.03)
	Phone.shell('sendevent /dev/input/event2 3 57 -1')
	Phone.shell('sendevent /dev/input/event2 0 0 0')

#--------------------------------------------------------------------	
# Function defining the windows screenshot, there are 2 windows in which the progam detects
# a change in the pixels color.
#--------------------------------------------------------------------
def GrabImage(Pos):
	if Pos == 0: # 0 -> left position
		# box = {'top': 537, 'left': 213, 'width': 35, 'height':85}
		box = {'top': 410, 'left': 354, 'width': 30, 'height':100}
	elif Pos == 1: # 1 -> right position
		# box = {'top': 535, 'left': 710, 'width': 35, 'height':87}
		box = {'top': 410, 'left': 576, 'width': 30, 'height':100}
	img = sct.grab(box)
	img = np.array(img)
	# Convert the image to grayscale as it is easier to manage
	GrayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Returns the sum of the window in terms of grayscale
	return int(GrayImg.sum())

#--------------------------------------------------------------------
# Connection to Android Phone
#--------------------------------------------------------------------

Client = Client(host='127.0.0.1', port=5037)
Phones = Client.devices()
Phone = Phones[0]

#--------------------------------------------------------------------
#Initialize parameters
#--------------------------------------------------------------------

sct = mss.mss() # Ultra fast screenshots module
Pos = 0 # timberman always starts on the left (0)
Change = 0 # Change flag
Ima0 = GrabImage(Pos) # Initial image to compare the sequence
tap (0) #Start game

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------

while True:
	
	Ima1 = GrabImage(Pos) # Next image in the sequence to compare

	if Change == 1:
		Ima0 = Ima1
		Change = 0

	if (abs(Ima1-Ima0)>60000): #Check whether the windows' sum is different enough (an obstacule is observed)
		Change = 1
		if (Pos == 0): # Change the position of timberman
			Pos = 1
		else:
			Pos = 0

	if Pos == 0:
		print(f'Position: Left')
	else:
		print(f'Position: Right')

	Ima0=Ima1 # Update sequence
	tap(Pos) # Tap in the required position

