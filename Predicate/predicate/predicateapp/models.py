from django.db import models
import datetime

class User(models.Model):
    firstName=models.TextField()
    lastName=models.TextField()
    email=models.TextField()
    password=models.TextField()
    userType=models.TextField(default='General')
    username=models.TextField()
    status=models.IntegerField(default=1)
    score=models.TextField(default='0')
    verificationCode=models.TextField()
    isVerified=models.BooleanField(default=False)

class Challenge(models.Model):
    challengeTitle=models.TextField()
    challengeDescription=models.TextField()
    challengeCreatedAt=models.DateField(("Date"), default=datetime.date.today)
    challengeDeadline=models.DateField()
    status=models.IntegerField(default=1)

class Dataset(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE)
    fileCaption=models.TextField()
    uploadedAt=models.DateField(("Date"), default=datetime.date.today)
    filePath=models.TextField()
    status = models.IntegerField(default=1)

class Prediction(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE)
    submittedBy=models.ForeignKey(User,on_delete=models.CASCADE)
    submittedAt=models.DateField(("Date"), default=datetime.date.today)
    predictionDescription=models.TextField()
    score=models.TextField(null=True)
    scoreUpdatedAt=models.TextField(null=True)
    status = models.IntegerField(default=1)


