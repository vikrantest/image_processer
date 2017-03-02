""
from django.conf.urls import url
from django.contrib import admin
from image_proj import views

urlpatterns = [
    url(r'^set-processing/', views.SetStayImageProcessing.as_view()),
    url(r'^get-stay-image-scores/', views.GetStayImageScores.as_view()),
]
