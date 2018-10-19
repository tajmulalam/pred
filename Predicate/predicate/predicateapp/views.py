from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .utils import Utils
import json
from django.http import JsonResponse
from .models import User
from .models import Challenge
from .models import Prediction
from .models import Dataset
from datetime import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect


def index(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('index.html')
    else:
        if user.userType == "General":
            return redirect('/dashboard/')
        else:
            return render_to_response('challengelist.html')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render_to_response('register.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        result = validateFields(data)
        if result[1]:
            user = User(firstName=data['firstName'],
                        lastName=data['lastName'],
                        email=data['email'],
                        password=data['cfpassword'],
                        username=data['username'],
                        verificationCode='123',
                        isVerified=True)
            user.save()
            if user.pk:
                return HttpResponse(json.dumps({"msg": result[0], "status": 200}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": 'Error while processing', "status": 500}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"msg": result[0], "status": 500}),
                                content_type='application/json')
    else:
        return render_to_response('login.html')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render_to_response('login.html')
    elif request.method == 'POST':
        utils = Utils()
        data = json.loads(request.body)
        print(data['username'])
        validUser = utils.checkCredentials(data['username'], data['password'])
        if validUser[0] == '200':
            request.session['user'] = validUser[1].id
        elif validUser[0] == '201':
            request.session['user'] = validUser[1].id
        return HttpResponse(json.dumps({"status": validUser[0], "userID": validUser[1].id}),
                            content_type='application/json')
    else:
        return render_to_response('login.html')


def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return render_to_response("login.html")


@csrf_exempt
def adddataset(request, challenge_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            challenge = Challenge.objects.get(id=challenge_id)
            return render_to_response('adddataset.html', {'user': user, 'challenge': challenge})
        elif request.method == 'POST':
            myfile = request.FILES['files']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            dataset = Dataset(challenge_id=challenge_id, fileCaption=myfile.name, filePath=uploaded_file_url)
            dataset.save()
            if dataset.pk:
                challenge = Challenge.objects.get(id=challenge_id)
                return redirect('/datasetlist/' + str(challenge.id))
            return render_to_response('addnewchallenge.html', {'user': user, 'challenge': None})
        else:
            return render_to_response('addnewchallenge.html', {'user': user, 'challenge': None})


def datasetlist(request, challenge_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            challenge = Challenge.objects.get(id=challenge_id)
            dataset = Dataset.objects.all().filter(challenge_id=challenge_id).order_by('-id')
            return render_to_response('datasetlist.html', {'user': user, 'dataset': dataset, 'challenge': challenge})
        else:
            return render_to_response('login.html')


@csrf_exempt
def deletedataset(request, dataset_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            dataset = Dataset.objects.get(id=dataset_id)
            challenge_id = dataset.challenge_id
            challenge = Challenge.objects.get(id=challenge_id)
            dataset.delete()
            return redirect('/datasetlist/' + str(challenge.id))
        else:
            return render_to_response('login.html')


def dashboard(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        challenge = Challenge.objects.all()
        prediction = Prediction.objects.all().filter(submittedBy_id=user.id)
        return render_to_response('dashboard.html', {'user': user, 'challenge': challenge, 'prediction': prediction})


def challengelist(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        challenge = Challenge.objects.all().order_by('-id')
        return render_to_response('challengelist.html', {'user': user, 'challenge': challenge})


@csrf_exempt
def addnewchallenge(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            return render_to_response('addnewchallenge.html', {'user': user})
        elif request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            result = validateChallenge(data)
            if result[1]:
                challenge = Challenge(challengeTitle=data['challengeTitle'],
                                      challengeDescription=data['challengeDescription'],
                                      challengeDeadline=data['deadline'])
                challenge.save()
                if challenge.pk:
                    return HttpResponse(json.dumps({"msg": result[0], "status": 200}),
                                        content_type='application/json')
                else:
                    return HttpResponse(json.dumps({"msg": 'Error while processing', "status": 500}),
                                        content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": result[0], "status": 500}),
                                    content_type='application/json')
        else:
            return render_to_response('login.html')


@csrf_exempt
def editchallenge(request, challenge_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            challengeDetect = None
            try:
                challengeDetect = Challenge.objects.get(id=challenge_id)
            except Challenge.DoesNotExist:
                challengeDetect = None
            return render_to_response('editchallenge.html', {'user': user, 'challenge': challengeDetect})
        else:
            return render_to_response('login.html')


@csrf_exempt
def editchallengeData(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        result = validateChallenge(data)
        if result[1]:
            challenge = Challenge.objects.get(id=data['challengeID'])
            challenge.challengeTitle = data['challengeTitle']
            challenge.challengeDescription = data['challengeDescription']
            challenge.challengeDeadline = data['deadline']
            challenge.save()
            if challenge.pk:
                return HttpResponse(json.dumps({"msg": result[0], "status": 200}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": 'Error while processing', "status": 500}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"msg": result[0], "status": 500}),
                                content_type='application/json')
    else:
        return render_to_response('login.html')


@csrf_exempt
def deleteChallenge(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        if request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            challenge = Challenge.objects.get(id=data['challengeID'])
            challenge.delete()
            return HttpResponse(json.dumps({"msg": "Delete Successful", "status": 200}),
                                content_type='application/json')
        else:
            return render_to_response('login.html')


def myprediction(request, prediction_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        prediction = Prediction.objects.all().filter(id=prediction_id)
        return render_to_response('prediction.html', {'user': user, 'prediction': prediction})


def challengeDetails(request, challenge_id):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        challenge = Challenge.objects.get(id=challenge_id)
        return render_to_response('challengeDetails.html', {'user': user, 'challenge': challenge})


"""This is the common method for checking user session"""


def checkUserAliveInSession(request):
    if request.session.has_key('user'):
        userID = request.session['user']
        user = None
        try:
            user = User.objects.get(id=userID)
        except User.DoesNotExist:
            user = None
        if user is not None:
            return user
        else:
            return None


def validateFields(data):
    errorMsg = ""
    result = []
    isFirstNameOK = False
    isLastNameOK = False
    isEmailOK = False
    isUsernameOK = False
    isPasswordOK = False

    if isBlank(data['firstName']):
        isFirstNameOK = False
        errorMsg += "First name is required" + "</br>"
    else:
        isFirstNameOK = True

    if isBlank(data['lastName']):
        isLastNameOK = False
        errorMsg += "Last name is required" + "</br>"
    else:
        isLastNameOK = True

    if isBlank(data['email']):
        isEmailOK = False
        errorMsg += "Email is required" + "</br>"
    else:
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = None
        if user is None:
            isEmailOK = True
        else:
            errorMsg += "Email already exists" + "</br>"
            isEmailOK = False

    if isBlank(data['username']):
        isUsernameOK = False
        errorMsg += "Username is required" + "</br>"
    else:
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None
        if user is None:
            isUsernameOK = True
        else:
            errorMsg += "Username already exists" + "</br>"
            isUsernameOK = False

    if isBlank(data['password']):
        isPasswordOK = False
        errorMsg += "Password is required" + "</br>"
    else:
        if isBlank(data['cfpassword']):
            isPasswordOK = False
            errorMsg += "Confirm password is required " + "</br>"
        else:
            if data['password'] == data['cfpassword']:
                isPasswordOK = True
            else:
                isPasswordOK = False
                errorMsg += "Password Not matched" + "</br>"
    if isFirstNameOK and isLastNameOK and isEmailOK and isUsernameOK and isPasswordOK:
        result.append("Registration Successful redirecting to login.")
        result.append(True)
        return result
    else:
        result.append(errorMsg)
        result.append(False)
        print(errorMsg)
        return result


def validateChallenge(data):
    errorMsg = ""
    result = []
    isTitleOK = False
    isDescription = False
    isDateOK = False

    if isBlank(data['challengeTitle']):
        isTitleOK = False
        errorMsg += "Challenge title is required" + "</br>"
    else:
        isTitleOK = True

    if isBlank(data['challengeDescription']):
        isDescription = False
        errorMsg += "Challenge description is required" + "</br>"
    else:
        isDescription = True

    if isBlank(data['deadline']):
        isDateOK = False
        errorMsg += "Deadline is required" + "</br>"
    else:
        isDateOK = True

    if isTitleOK and isDescription and isDateOK:
        result.append("Challenge Created and publish Successful")
        result.append(True)
        return result
    else:
        result.append(errorMsg)
        result.append(False)
        print(errorMsg)
        return result


def isBlank(myString):
    return not (myString and myString.strip())
