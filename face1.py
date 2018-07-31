import cv2
import sys
import json
import time
import numpy as np
from keras.models import model_from_json


emotion_labels = ['angry', 'fear', 'happy', 'sad', 'surprise', 'neutral']
# load json and create model arch
json_file = open('./model.json','r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model.load_weights('./model.h5')
face_patterns = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def predict_emotion(face_image_gray): # a single cropped face
	resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
	# cv2.imwrite(str(index)+'.png', resized_img)
	
	image = resized_img.reshape(1, 1, 48, 48)
	list_of_list = model.predict(image, batch_size=1, verbose=1)
	angry, fear, happy, sad, surprise, neutral = [prob for lst in list_of_list for prob in lst]
	return [angry, fear, happy, sad, surprise, neutral]




def facedect(filename):

	sample_image = cv2.imread('./project/save_file/'+filename)
	sample_image0 = cv2.imread('./project/save_file/'+filename)
	faces = face_patterns.detectMultiScale(sample_image,scaleFactor=1.1,minNeighbors=5,minSize=(100, 100))
	sample_image1 = cv2.cvtColor(sample_image, cv2.COLOR_BGR2GRAY)
	res=[]
	imgs=[]
	for (x, y, w, h) in faces:
		face_image_gray = sample_image1[y:y+h, x:x+w]
		angry, fear, happy, sad, surprise, neutral = predict_emotion(face_image_gray)
		cv2.rectangle(sample_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		font=cv2.FONT_HERSHEY_SIMPLEX
		l=[angry, fear, happy, 0, surprise, neutral]
		print(l)
		ind=l.index(max(l))
		text=emotion_labels[ind]
		res.append(ind)
		imgs.append([sample_image0[y:y+h, x:x+w],ind])
		sample_image=cv2.putText(sample_image,text,(x, y),font,1.2,(255,255,255),2)
	

	
	return sample_image0,sample_image,res,imgs
