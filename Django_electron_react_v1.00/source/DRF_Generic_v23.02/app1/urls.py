from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('data1/list/',Data1ListView.as_view()),
    path('data1/create/',Data1CreateView.as_view()),
    path('data1/delete/<str:data_id>/',Data1DeleteFromIdView.as_view()),
    path('data1/tags/list/',Data1TagsListView.as_view()),
    path('data1/search/<str:keyword>/',Data1SearchWithKeywordView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)