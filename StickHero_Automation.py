# Necessary libraries
from ppadb.client import Client as AdbClient
import numpy as np
import cv2
import time

#Phone connection using ADB
client = AdbClient(host = '127.0.0.1', port=5037)
phones = client.devices()
phone = phones[0]

#Infinite loop to the code keep running
while(1):

	# Take the phone screenshoot
	image = phone.screencap()
	with open ('screenshot.png','wb') as fb:
		fb.write(image)

	# Return a numpy array of size (1280,720,3) with the screenshoot info in RGB
	img = cv2.imread('screenshot.png')

	# We know that in this row you can always find the black blocks of the game
	row = 900

	# A black pixel is [0 0 0] in RGB
	# BlackPixels is a numpy array with the number of black pixels in the X axis (max of 720 pixels)
	BlackPixels = np.array([])

	# Determine how many black pixels there are
	for pix, RGB in enumerate(img[row]):
		if (RGB == np.array([0,0,0])).all():
			BlackPixels = np.append(BlackPixels,pix)

	# Change type of the numpy array
	BlackPixels = BlackPixels.astype('int')

	#There are always 4 points for the black blocks
	#P1 is always the first pixel in BlackPixels
	p1 = BlackPixels[0]
	#P4 is always the last pixel in BlackPixels
	p4 = BlackPixels[len(BlackPixels)-1]

	# Calculate P2 and P3
	for i, pix in enumerate(BlackPixels):
			if(pix+1 != BlackPixels[i+1]):
				p2 = BlackPixels[i]
				p3 = BlackPixels[i+1]
				break
	# P1/P2/P3/P4 represent the pixels where the black blocks start and end
	#print(p1,p2,p3,p4)


	# Distance in pixels to the red spot in the middle of each block
	RedSpot = ((p3-p2) + (p4-p3)/2)
	print(f'Block 1 start:	{p1+1} pixel')
	print(f'Block 1 finish:	{p2+1} pixel')
	print(f'Block 2 start:	{p3+1} pixel')
	print(f'Block 2 finish:	{p4+1} pixel')
	print(f'Distance to RedSpot: {RedSpot} pixels')

	#LFactor for the phone connection
	F = 1.45
	phone.shell(f'input touchscreen swipe 360 400 360 400 {int(RedSpot*F)}')
	time.sleep(3)
