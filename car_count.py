import cv2

camera = cv2.VideoCapture("raw.mp4")
firstFrame = None
fps = 0
car_num = 0

#Auto counting module function
def car_count(frame, firstFrame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		return [], gray
	else:
		cv2.rectangle(frame, (0, 565), (1280, 590), (0, 0, 255), 2)
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=3)
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
		if cnts != []:
			for c in cnts:
				if cv2.contourArea(c) < 700:
					x, y, w, h = cv2.boundingRect(c)
					print ("xywh", str(x), str(y), str(w), str(h))
					if x > 550:
						cv2.circle(frame,(int(x+w), int(y+h)), 20, (255,0,0), 2)
						cv2.rectangle(frame, (x, y), (x + 3*w, y + 3*h), (0, 255, 0), 2)
					if int(x+3*w)>560 and int(x+3*w)<580:
						global car_num
						car_num += 1
						cv2.putText(frame,str(car_num), (50, 50), 0, 1, (0, 0, 255), 2)
					return frame, gray
		else:
			return [], gray
#main
while True:
	grabbed, frame = camera.read()
	out_frame, gray = car_count(frame, firstFrame)
	if out_frame != []:
		cv2.imshow("w1", out_frame)
		if cv2.waitKey(10) & 0xff == ord("q"):
			break
	print ("------------------FPS:%d----------------------"%fps)
	print ("CAR_NUM:%d"%car_num)
	firstFrame = gray.copy()
	fps+=1

camera.release()
cv2.destroyAllWindows()
