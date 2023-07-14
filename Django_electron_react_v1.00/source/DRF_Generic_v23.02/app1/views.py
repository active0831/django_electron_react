import uuid, os, io, json, random, requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import *
from .models import *

from rest_framework.permissions import IsAuthenticated


class Data1ListView(APIView):
    def get(self, request, format=None):
        model_data = Data1Model.objects.all().order_by('-created_at')
        serializer = Data1Serializer(model_data, many=True)        
        return Response(serializer.data)


class Data1CreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = get_user(request)
        data = request.data
        parser = Data1Parser(data, user)
        parser.write_data()
        return Response(status=status.HTTP_201_CREATED)


class Data1DeleteFromIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, data_id, format=None):
        data = Data1Model.objects.get(data_id=data_id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Data1TagsListView(APIView):
    def get(self, request, format=None):
        tags = Data1TagModel.objects.values_list(
            'tag_text', flat=True).distinct()
        return Response(tags)
    

class Data1SearchWithKeywordView(APIView):
    def post(self, request, keyword, format=None):
        tags = request.data['tags']
        if keyword == " ":
            results = Data1Model.objects.all()
        else:
            results = Data1Model.objects.filter(data_name__contains=keyword)

        for tag in tags:
            data1_with_tag = Data1TagModel.objects.filter(tag_text=tag)
            results = results.filter(
                data_id__in=data1_with_tag.values_list('data1', flat=True))
            
        serializer = Data1Serializer(results, many=True)
        return Response(serializer.data)
    
    
def get_user(request):
    cookie = request.headers['Cookie']
    response = requests.get("http://localhost:8000/users/user/",
        headers={'Cookie': cookie})
    response_json = json.loads(response.text)
    return response_json