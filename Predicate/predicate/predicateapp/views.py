from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .utils import Utils
import json
from django.http import JsonResponse
from .models import User
from .models import Challenge


def index(request):
    return render_to_response('index.html')


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


def addDataset(request, challenge_id):
    return HttpResponse("<h1>challenge id " + str(challenge_id) + "</h1>")


def dashboard(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        return render_to_response('dashboard.html', {'user': user})


def challengelist(request):
    user = checkUserAliveInSession(request)
    if user is None:
        return render_to_response('login.html')
    else:
        challenge = Challenge.objects.all()
        return render_to_response('challengelist.html', {'challenge': challenge})


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
        errorMsg += "First name is required" + "\n"
    else:
        isFirstNameOK = True

    if isBlank(data['lastName']):
        isLastNameOK = False
        errorMsg += "Last name is required" + "\n"
    else:
        isLastNameOK = True

    if isBlank(data['email']):
        isEmailOK = False
        errorMsg += "Email is required" + "\n"
    else:
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = None
        if user is None:
            isEmailOK = True
        else:
            errorMsg += "Email already exists" + "\n"
            isEmailOK = False

    if isBlank(data['username']):
        isUsernameOK = False
        errorMsg += "Username is required" + "\n"
    else:
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None
        if user is None:
            isUsernameOK = True
        else:
            errorMsg += "Username already exists" + "\n"
            isUsernameOK = False

    if isBlank(data['password']):
        isPasswordOK = False
        errorMsg += "Password is required" + "\n"
    else:
        if isBlank(data['cfpassword']):
            isPasswordOK = False
            errorMsg += "Confirm password is required " + "\n"
        else:
            if data['password'] == data['cfpassword']:
                isPasswordOK = True
            else:
                isPasswordOK = False
                errorMsg += "Password Not matched" + "\n"
    if isFirstNameOK and isLastNameOK and isEmailOK and isUsernameOK and isPasswordOK:
        result.append("Registration Successful redirecting to login.")
        result.append(True)
        return result
    else:
        result.append(errorMsg)
        result.append(False)
        print(errorMsg)
        return result


def isBlank(myString):
    return not (myString and myString.strip())
