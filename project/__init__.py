# project/__init__.py

from flask import Flask, request, jsonify
import time

from flask import render_template, flash, redirect, url_for, request, g  
import flask
from flask import Flask,request,url_for, send_from_directory
import os
import time
import face
import random
import cv2
import sys
import json

import numpy as np

import datetime

# config
app = Flask(__name__)

app.config.from_object(__name__)



from collections import Counter

# routes


#my!-----------------------------------------------------------------------

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','txt','pdf'])
app.config['UPLOAD_FOLDER'] = os.getcwd()+"/project/save_file"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



emotion_labels=['angry', 'confused', 'sad', 'neutral', 'disgust', 'arousal', 'surprise', 'fear', 'valence', 'contempt', 'happy']


@app.route('/')
def index():
	return render_template("about.html")
@app.route('/index')
def index0():
	return redirect("../../")

@app.route('/result',methods = ['GET', 'POST'])
def contact_us():
	if request.method == "POST":
		print(111)
		file = request.files['file']
		tt=str(time.time()).split('.')[0]
		filename = tt+".jpg"
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		img0,img1,res,imgs,res_text,emo_sum_male,emo_sum_female=face.facedect(filename)
		d=Counter(res)
		always="???"
		if(len(res)>0):
			always=emotion_labels[d.most_common()[0][0] ]

		tt=str(time.time()).split('.')[0]
		path=os.getcwd()+"/project/static/resimg/"
		cv2.imwrite(path+tt+"0.png", img0)
		cv2.imwrite(path+tt+"1.png", img1)
		i=0
		outputs=[]
		print(res_text)
		for img in imgs:
			print(type(res_text[i]))
			fn=path+tt+"_"+str(i)+"_.png"
			cv2.imwrite(fn, img[0])
			outputs.append([tt+"_"+str(i)+"_.png" ,emotion_labels[ img[1]],res_text[i] ])
			i+=1
		return render_template("res.html",tt=tt,always=always,outputs=outputs,emo_sum_male=emo_sum_male,emo_sum_female=emo_sum_female,emotion_labels=str(emotion_labels))

	else:
		return "404"