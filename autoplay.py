import numpy as np
import mss
import cv2
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

sct = mss.mss()
command = "stay"

is_up_pressed = False
is_down_pressed = False

xmin = 90
t0 = time.perf_counter()
while True:
	monitor = sct.monitors[1]
	image = sct.grab(monitor)
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

	basex = 380
	basey = 130
	frame = image[basey:basey+200, basex:basex+610]
	bgcol = frame[5,607]
	elapsed = int(round((time.perf_counter() - t0)/60))
	elapsed = min(elapsed,40)

	if (is_down_pressed):
		xmin = 120+elapsed
	elif(xmin > 100+elapsed):
		xmin -= 2
	else:
		xmin = 100 + elapsed
	xmax = 180 + elapsed
	ymin = 130
	ymax = 135

	hitbox = frame[ymin:ymax, xmin:xmax]                                            
	hb_average = (np.mean(hitbox))
	ab_diff = abs(bgcol - hb_average)#*(1+5*elapsed/90)

	if (not is_down_pressed):
		xmin2 = 70#+elapsed
	else:
		xmin2 = 35
	
	xmax2 = 180 + elapsed

	ymin2 = 95
	ymax2 = 100

	hitbox2 = frame[ymin2:ymax2, xmin2:xmax2]                                            
	hb2_average = (np.mean(hitbox2))
	ab2_diff = abs(bgcol - hb2_average)*(2+5*elapsed/90)
	

	if (ab_diff > 0 and (not is_up_pressed)):
		keyboard.press(Key.up)
		is_up_pressed = True
		command = 'jump'
	elif (ab_diff == 0 and is_up_pressed):
		keyboard.release(Key.up)
		is_up_pressed = False
		command='stay'
		keyboard.press(Key.down)
		keyboard.release(Key.down)
	elif (ab2_diff > 6 and (not is_down_pressed)):
		keyboard.press(Key.down)
		is_down_pressed = True
		command = 'duck'
	elif (ab2_diff <= 1 and is_down_pressed):
		keyboard.release(Key.down)
		is_down_pressed = False
		command='stay'


	font = cv2.FONT_HERSHEY_SIMPLEX
	pos = (300,175)
	fontScale = 0.6
	col = int(255-bgcol)
	fontColor = (col,col,col)
	lineType = 2

	cv2.putText(frame,str(command)+' ('+'%.1f %.1f %.1f' % (bgcol,hb_average,hb2_average)+')', 
	    pos, 
	    font, 
	    fontScale,
	    fontColor,
	    lineType)

	cv2.rectangle(frame, (xmin-2,ymin-2),(xmax+2,ymax+2),fontColor,1)
	cv2.rectangle(frame, (xmin2-2,ymin2-2),(xmax2+2,ymax2+2),fontColor,1)

	cv2.imshow('screen',frame)
	#cv2.imshow('hitbox', np.concatenate((hitbox,hitbox2),axis = 0))
	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break
