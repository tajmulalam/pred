from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('login', views.login, name='login'),
    url('aboutus', views.aboutus, name='aboutus'),
    url('contactus', views.contactus, name='contactus'),
    url('register', views.register, name='register'),
    url('logout', views.logout, name='logout'),
    # admin area pages
    url('challengelist', views.challengelist, name='challengelist'),
    url('addnewchallenge', views.addnewchallenge, name='addnewchallenge'),
    url(r'^editchallenge/(?P<challenge_id>[0-9]+)/$', views.editchallenge, name='editchallenge'),
    url(r'^predictionlist/(?P<challenge_id>[0-9]+)/$', views.predictionlist, name='predictionlist'),
    url(r'^updatescore/(?P<prediction_id>[0-9]+)/$', views.updatescore, name='updatescore'),
    url('deleteChallenge', views.deleteChallenge, name='deleteChallenge'),
    url('editchallengeData', views.editchallengeData, name='editchallengeData'),
    # /challenge/12/
    url(r'^adddataset/(?P<challenge_id>[0-9]+)/$', views.adddataset, name='adddataset'),
    url(r'^datasetlist/(?P<challenge_id>[0-9]+)/$', views.datasetlist, name='datasetlist'),
    url(r'^deletedataset/(?P<dataset_id>[0-9]+)/$', views.deletedataset, name='deletedataset'),
    # user area pages
    url('dashboard', views.dashboard, name='dashboard'),
    url('myprediction/(?P<prediction_id>[0-9]+)/$', views.myprediction, name='myprediction'),
    url('challengeDetails/(?P<challenge_id>[0-9]+)/$', views.challengeDetails, name='challengeDetails'),
    url('submitprediction/(?P<challenge_id>[0-9]+)/$', views.submitprediction, name='submitprediction'),

]
# for turning on media file access
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
