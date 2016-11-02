# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from adminpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^login/?$', Login.as_view()),
    url(r'^logout/?$', Logout.as_view()),
    url(r'^activity/list/?$', ActivityList.as_view()),
    url(r'^activity/create/?$', CreateActivity.as_view()),
    url(r'^activity/delete/?$', DeleteActivity.as_view()),
    url(r'^activity/detail/?$', ActivityDetail.as_view()),
    url(r'^activity/menu/?$', ActivityMenu.as_view()),
    url(r'^activity/checkin/?$', CheckIn.as_view()),
    url(r'^image/upload/?$', UploadImage.as_view()),
]

