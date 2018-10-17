from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .utils import Utils
import json
from django.http import JsonResponse

def index(request):
    return render_to_response('index.html')

@csrf_exempt
def login(request):
	if request.method=='GET':
		return render_to_response('login.html')    	
	elif request.method == 'POST':
		utils=Utils()
		data = json.loads(request.body)
		print(data['username'])
		validUser=utils.checkCredentials(data['username'],data['password'])
		return HttpResponse(json.dumps({'user':validUser}),content_type='application/json')
	else:
		return render_to_response('login.html')


def addDataset(request, challenge_id):
    return HttpResponse("<h1>challenge id " + str(challenge_id) + "</h1>")
