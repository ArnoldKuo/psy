# pip install gTTS
#
import os
import cv2
import pandas as pd
from gtts import gTTS

img = cv2.imread('wallpaper.jpg')
height, width, channel = img.shape

screen_width =1920
screen_height=1080
if (width!=screen_width and height!=screen_height):
	img=cv2.resize(img, (screen_width, screen_height), interpolation = cv2.INTER_CUBIC)

# Put Text 
#text = "Wallpaer: Width= "+str(width)+" Height= "+str(height)
text = "Next: press Space / Enter"
x = 660  #int(screen_width/4)
y = 1000   #int(screen_height/4)
cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)
 
text = "Left: press L"
x = 508
y = 380
cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)

text = "Right: press R"
x = 1108
y = 380  
cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)

# Draw Box
L_top, L_bottom, L_left, L_right = 420, 644,  508,  732 # 224x224
R_top, R_bottom, R_left, R_right = 420, 644, 1108, 1332 # 224x224	
cv2.rectangle(img, (L_left, L_top), (L_right, L_bottom), (255,0,0), 2)
cv2.rectangle(img, (R_left, R_top), (R_right, R_bottom), (255,0,0), 2)
	
cv2.namedWindow('fullscreen', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('fullscreen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow('fullscreen', img)

# Loop
ans = []
df = pd.read_csv('shape.csv', header=None)

for i in range(len(df)):
	next = False
    # get text & filenames from dataframe
	text= df[0].iloc[i]
	L_filename= df[1].iloc[i]
	R_filename= df[2].iloc[i]
	
	# read left image and put into box
	L_img = cv2.imread(L_filename)
	img[L_top:L_bottom, L_left:L_right] = L_img
	cv2.rectangle(img, (L_left, L_top), (L_right, L_bottom), (255,0,0), 3)
	# read right image and put into box
	R_img = cv2.imread(R_filename)
	img[R_top:R_bottom, R_left:R_right] = R_img		
	cv2.rectangle(img, (R_left, R_top), (R_right, R_bottom), (255,0,0), 3)
	# show image
	cv2.imshow('fullscreen', img)
		
	# speak text
	tts = gTTS(text,lang='en')
	tts.save('gTTS.mp3')
	#os.system('mpg321 gTTS.mp3') # RPi
	os.system('cmdmp3 gTTS.mp3')  # PC
	#os.system('afplay gTTS.mp3')  # MAC
	
	os.remove('gTTS.mp3')
	
	select='none'
	
	# check keypress
	while(not next):
		keypress = cv2.waitKey(1) & 0xFF # keypress by user
		if keypress==ord("l")	:
			cv2.rectangle(img, (L_left, L_top), (L_right, L_bottom), (0,0,255), 3)
			cv2.imshow('fullscreen', img)
			select='left'
		if keypress==ord("r")	:
			cv2.rectangle(img, (R_left, R_top), (R_right, R_bottom), (0,0,255), 3)
			cv2.imshow('fullscreen', img)
			select='right'
		if keypress==ord(" ") or keypress==0x0D:
			next=True
	# add answer
	ans.append(select)

print(ans)
dt = pd.DataFrame(ans)
dt.to_csv('user.csv')
print('saved to user.csv')
cv2.waitKey(0)
cv2.destroyAllWindows()
