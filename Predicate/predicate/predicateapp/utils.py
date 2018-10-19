from django.db import connection, transaction
from collections import namedtuple
from datetime import date, datetime
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from .models import User
import json


class Utils:
    def __init__(self):
        self.cursor = connection.cursor()

    # def getAllMeasurements(self,x,y):
    # 	self.cursor.execute(
    # 		"""SELECT * from dataview
    #               where data_capture_time
    #               between TO_DATE(%s, 'YYYY-MM-DD') and
    #               TO_DATE(%s, 'YYYY-MM-DD'); """, (x, y))

    # 	desc = self.cursor.description
    # 	nt_result = namedtuple('Result', [col[0] for col in desc])
    # 	return [nt_result(*row) for row in self.cursor.fetchall()]

    def checkCredentials(self, username, password):
        user = None
        result = []
        try:
            user = User.objects.get(username=username, password=password)
            print(user.status)
        except User.DoesNotExist:
            user = None
        if user is not None:
            # request.session['logged_in'] = True
            # request.session['user'] = user
            if user.status == 1:
                if user.userType == 'General':
                    print(user.userType)
                    result.append('200')
                    result.append(user)
                    return result  # General user valid
                elif user.userType == 'Admin':
                    print(user.userType)
                    result.append('201')
                    result.append(user)
                    return result  # Admin user valid
                else:
                    result.append('500')
                    result.append(None)
                    return result  # error or not found
            elif user.status == 0:
                result.append('250')
                result.append(None)
                return result  # user is not active
            else:
                result.append('500')
                result.append(None)
                return result  # error or not found
        else:
            result.append('500')
            result.append(None)
            return result  # error or not found
