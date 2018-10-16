from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('login',views.login,name='login'),
    #/challenge/12/
    url(r'^adddataset/(?P<challenge_id>[0-9]+)/$',views.addDataset,name='addDataset')
]