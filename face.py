import requests
import json
import cv2
import os
import numpy as np


def get_dict_value(date, keys, default=None): #这个函数是用来把迭代的字典用A.B.C的形式进行输出
	#default=None，在key值不存在的情况下，返回None
	keys_list = keys.split('.')
	#以“.”为间隔，将字符串分裂为多个字符串，其实字符串为字典的键，保存在列表keys_list里
	if isinstance(date,dict):
		#如果传入的数据为字典
		dictionary = dict(date)
		#初始化字典
		for i in keys_list:
			#按照keys_list顺序循环键值
			try:
				if dictionary.get(i) != None:
					dict_values = dictionary.get(i)
				#如果键对应的值不为空，返回对应的值
				elif dictionary.get(i) == None:
					dict_values = dictionary.get(int(i))
				#如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
			except:
				return default
					#如果字符串型的键转换整数型错误，返回None
			dictionary = dict_values
		return dictionary
	else:
		#如果传入的数据为非字典
		try:
			dictionary = dict(eval(date))
			#如果传入的字符串数据格式为字典格式，转字典类型，不然返回None
			if isinstance(dictionary,dict):
				for i in keys_list:
					#按照keys_list顺序循环键值
					try:
						if dictionary.get(i) != None:
							dict_values = dictionary.get(i)
						#如果键对应的值不为空，返回对应的值
						elif dictionary.get(i) == None:
							dict_values = dictionary.get(int(i))
						#如果键对应的值为空，将字符串型的键转换为整数型，返回对应的值
					except:
						return default
							#如果字符串型的键转换整数型错误，返回None
					dictionary = dict_values
				return dictionary
		except:
			return default

appid = "5a200ce8e6ec3a6506030e54ac3b970e"
register_data = {"cmd": "getFace", "appid": appid, "userid": "0B789C68DEF466423B55BF03682DE2623"}#userID是可以多次使用的，主要看CMD的值

emotion_labels=['angry', 'confused', 'sad', 'neutral', 'disgust', 'arousal', 'surprise', 'fear', 'valence', 'contempt', 'happy']
def emotionlist(data):
	 return [data.get("angry"), data.get("confused"), data.get("sad"), data.get("neutral"), data.get("disgust"), data.get("arousal"), data.get("surprise"), data.get("fear"), data.get("valence"), data.get("contempt"), data.get("happy")]

def facedect(filename):
	path='./project/save_file/'+filename
	print(path)
	sample_image = cv2.imread('./project/save_file/'+filename)
	sample_image0 = cv2.imread('./project/save_file/'+filename)
	
	low=500
	if(sample_image.shape[0]>low):#宽度
		r = low*1.0/sample_image.shape[1]
		dim = (low, int(sample_image.shape[0]*r))
		sample_image=cv2.resize(sample_image, dim, interpolation=cv2.INTER_AREA)
		sample_image0=cv2.resize(sample_image0, dim, interpolation=cv2.INTER_AREA)
	if(sample_image.shape[1]>low):#高度
		r = low*1.0/sample_image.shape[0]
		dim = ( int(sample_image.shape[1]*r),low)
		sample_image=cv2.resize(sample_image, dim, interpolation=cv2.INTER_AREA)
		sample_image0=cv2.resize(sample_image0, dim, interpolation=cv2.INTER_AREA)
	cv2.imwrite('./project/save_file/'+filename,sample_image)
	#上传
	url = "http://idc.emotibot.com/api/ApiKey/openapi.php"
	files = {'file': open(path, 'rb')}#运行时替换文件地址
	r = requests.post(url, params=register_data, files=files)

	#返回值解析
	response = json.dumps(r.json(), ensure_ascii=False)
	jsondata = json.loads(response)
	datas = jsondata.get("data")#读数据
	image = cv2.imread(path)#读取图片

	print(datas)
	#输出特征
	print("Return: %s" % jsondata.get("return"))
	print("ReturnMessage: %s" % jsondata.get("img_width"))
	print("脸的数量是: %s" % jsondata.get("num_faces"))
	if(int(jsondata.get("num_faces"))==0):
		datas=[]
	#图片切片和坐标输出
	res=[]
	imgs=[]
	res_text=[]
	emo_sum_female=np.zeros(len(emotion_labels))
	emo_sum_male=np.zeros(len(emotion_labels))
	male_num=0
	female_num=0
	for data in datas:
		print("face_id is : %s" % data.get('face_id'))
		#切片
		print("x= %f y= %f" %(get_dict_value(data, 'position.center.x'),get_dict_value(data, 'position.center.y')))
		a=(int(jsondata.get("img_width")*(get_dict_value(data, 'position.center.x')-get_dict_value(data, 'position.size.width')/2)))
		b=(int(jsondata.get("img_width")*(get_dict_value(data, 'position.center.x')+get_dict_value(data, 'position.size.width')/2)))
		c=(int(jsondata.get("img_height")*(get_dict_value(data, 'position.center.y')-get_dict_value(data, 'position.size.height')/2)))
		d=(int(jsondata.get("img_height")*(get_dict_value(data, 'position.center.y')+get_dict_value(data, 'position.size.height')/2)))
		
		x=a
		y=c
		w=b-a
		h=d-c

		print(x,y,w,h)
		cv2.rectangle(sample_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		age = get_dict_value(data, 'attribute.age')
		gender="male" if (float(get_dict_value(data, 'attribute.gender')) < 0.5) else "female"
		emolist=emotionlist(data.get("emotions"))
		i=0
		for sig_emo in emolist:
			if gender=="male":
				emo_sum_male[i]+=sig_emo
				male_num+=1
			else:
				emo_sum_female[i]+=sig_emo
				female_num+=1
			i+=1
			
		ind=emolist.index(max(emolist))
		res.append(ind)
		res_text.append("age: "+str(age)+", gender: "+gender)
		text=emotion_labels[ind]
		imgs.append([sample_image0[y:y+h, x:x+w],ind])
		font=cv2.FONT_HERSHEY_SIMPLEX
		sample_image=cv2.putText(sample_image,text,(x, y),font,1.2,(255,255,255),2)

		
		# cv2.imwrite("/Users/yangchengran/Desktop/test/"+str(data.get('face_id'))+".jpg",cropImg) #//保存到指定目录

	# print(get_dict_value(data, 'position.size.width'))
	# print(get_dict_value(data,'position.size.height'))#对于任何一个输入，可以把"emotion"换成任意索引，比如"emotion.angry","position.center.x"

	#输出性别和是否年轻
	# for data in datas:
	#	 print("face_id is : %s" % data.get('face_id'))
	#	 if(get_dict_value(data, 'attribute.young')>0.8):
	#		 print('young')
	#	 else:
	#		 print('not young')
	#	 if (float(get_dict_value(data, 'attribute.gender')) > 0.5):
	#		 print("female")

	#	 if (float(get_dict_value(data, 'attribute.gender')) < 0.5):
	#		 print("male")

	#	 if (float(get_dict_value(data, 'attribute.gender')) == 0.5):
	#		 print("可男可女")
	print(res)
	emo_sum_male/=male_num
	emo_sum_female/=female_num
	return sample_image0,sample_image,res,imgs,res_text,emo_sum_male.tolist(),emo_sum_female.tolist()
