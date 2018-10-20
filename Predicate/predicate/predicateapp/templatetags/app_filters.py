from django import template
from ..models import User
from ..models import Challenge

register = template.Library()


@register.filter(name='get_user_info')
def get_user_info(userID):
    user = User.objects.get(id=userID)
    return user.firstName + " " + user.lastName


@register.filter(name='get_user_name')
def get_user_name(userID):
    user = User.objects.get(id=userID)
    return user.username


@register.filter(name='get_challenge_info')
def get_challenge_info(challengeID):
    challenge = Challenge.objects.get(id=challengeID)
    return challenge.challengeTitle


@register.filter(name='get_challenge_deadline')
def get_challenge_deadline(challengeID):
    challenge = Challenge.objects.get(id=challengeID)
    return challenge.challengeDeadline
