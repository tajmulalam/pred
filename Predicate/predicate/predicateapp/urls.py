from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('login', views.login, name='login'),
    url('register', views.register, name='register'),
    url('logout', views.logout, name='logout'),
    url('dashboard', views.dashboard, name='dashboard'),
    url('challengelist', views.challengelist, name='challengelist'),
    # /challenge/12/
    url(r'^adddataset/(?P<challenge_id>[0-9]+)/$', views.addDataset, name='addDataset'),
    url(r'^myprediction/(?P<prediction_id>[0-9]+)/$', views.myprediction, name='myprediction')
]
