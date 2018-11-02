from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import simplejson as json
import base64
from django.core.files.base import ContentFile
import cognitive_face as CF
import os
import sys
# Create your views here.


KEY = '2ff6da2477a64d7c96cb16eca00f3fa0'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
BASE_URL = 'https://centralindia.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(os.path.dirname(BASE_DIR),'face_app','media','soma.png')


def index(request):
	return render(request, 'index.html')

@csrf_exempt
def add(request):
	if request.method == "POST":
		payload = json.loads(request.body)
		image_data = payload['imageData']
		#format, imgstr = image_data.split(';base64,')
		#ext = format.split('/')[-1]
		data = base64.b64decode(image_data) #Image data
		f = open(filepath, 'wb')
		f.write(data)
		f.close()
		img_url = filepath
		response_detect = CF.face.detect(img_url)

		if (response_detect == []):
			return HttpResponse('{"name":"NULL"}')
		else:
			face_ids= [d['faceId'] for d in response_detect]
			identified = CF.face.identify(face_ids,'firstgroup')
			if (identified[0]['candidates'] == []):
				return HttpResponse('{"name":"unidentified"}')
			else:
				info = [d['personId'] for d in identified[0]['candidates']]
				per_info = (CF.person.get('firstgroup',info[0]));
				return HttpResponse('{"name":"' + per_info['name']+ '"}')
	else:
		return HttpResponse('no data')

@csrf_exempt
def reg(request):
	if (request.method == "POST"):
		name = (json.loads(request.body)['reg_name'])
		# print (request.body['reg_name'])
		img_url=filepath
		response_detect = CF.face.detect(img_url)
		response = CF.person.create('firstgroup',name)
		person_id=response['personId']
		CF.person.add_face(img_url,'firstgroup', person_id);
		CF.person_group.train('firstgroup')
		return HttpResponse('{"name":"NULL"}')
	else:
		return HttpResponse('no data')


"""
@csrf_exempt
def add(request):
	if request.method == "POST":
		payload = json.loads(request.body)
		image_data = payload['imageData']
		#format, imgstr = image_data.split(';base64,')
		#ext = format.split('/')[-1]
		data = base64.b64decode(image_data) #Image data
		f = open('someimage.png', 'wb')
		f.write(data)
		f.close()
		return HttpResponse(request)
	else:
		return HttpResponse('no data')
"""

"""
@csrf_exempt
def add(request):
	if request.method == "POST":
		payload = json.loads(request.body)
		image_data = payload['imageData']
		#format, imgstr = image_data.split(';base64,')
		#ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(image_data)) #Image data
		myfile = "profile-"+"." + "png"  #filename
		fs = FileSystemStorage()
		filename = fs.save(myfile, data)
		return HttpResponse(request)
	else:
		return HttpResponse('no data')
"""

"""
@csrf_exempt
def add(request):
	if request.method == "POST":
		payload = json.loads(request.body)
		print(payload['imageData'])
		image_data = base64.b64decode(payload['imageData'])
		f = open('Pic.png', 'w')
		f.write(str(image_data))
		f.close()
		#print(image_data)
		#f = open(settings.MEDIA_ROOT + ima.jpg', 'wb')
		#print(request.POST.data)
		return HttpResponse(request)
	else:
		return HttpResponse('no data')
"""