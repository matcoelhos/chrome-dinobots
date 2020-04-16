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

keyboard = Controller()

sct = mss.mss()
command = "stay"

is_up_pressed = False

xmin = 90

keyboard.press(Key.down)
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
	elapsed = min(elapsed,20)

	if (is_up_pressed):
		xmin = 80+elapsed
	else:
		xmin = 110 + elapsed
	xmax = 180 + elapsed
	ymin = 130
	ymax = 135

	hitbox = frame[ymin:ymax, xmin:xmax]                                            
	hb_average = (np.mean(hitbox))
	ab_diff = abs(bgcol - hb_average)#*(1+5*elapsed/90)

	

	if (ab_diff > 0 and (not is_up_pressed)):
		keyboard.release(Key.down)
		keyboard.press(Key.up)
		is_up_pressed = True
		command = 'jump'
	elif (ab_diff == 0 and is_up_pressed):
		keyboard.release(Key.up)
		keyboard.press(Key.down)
		keyboard.release(Key.down)
		keyboard.press(Key.down)
		is_up_pressed = False
		command='stay'


	font = cv2.FONT_HERSHEY_SIMPLEX
	pos = (300,175)
	fontScale = 0.6
	col = int(255-bgcol)
	fontColor = (col,col,col)
	lineType = 2

	cv2.putText(frame,str(command)+' ('+'%.1f %.1f' % (bgcol,hb_average)+')', 
	    pos, 
	    font, 
	    fontScale,
	    fontColor,
	    lineType)

	cv2.rectangle(frame, (xmin-2,ymin-2),(xmax+2,ymax+2),fontColor,1)
	#cv2.rectangle(frame, (xmin2-2,ymin2-2),(xmax2+2,ymax2+2),fontColor,1)

	cv2.imshow('screen',frame)
	#cv2.imshow('hitbox', np.concatenate((hitbox,hitbox2),axis = 0))
	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break

