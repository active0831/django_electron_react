import uuid

from rest_framework import serializers
from .models import *

### [ Modify this ] ###

class Data1Serializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Data1Model
        fields = ['data_id', 'data_name', 'created_by', 'created_at', 'description', 'image', 'tags']

    def get_tags(self, obj):
        tags = Data1TagModel.objects.filter(data1=obj.data_id)
        return [tag.tag_text for tag in tags]

class Data1Parser():
    def __init__(self, multipart_form_data, user):
        self.data = {}
        self.data["data_id"] = self.set_id(multipart_form_data)
        self.data["data_name"] = multipart_form_data["data_name"]
        self.data["created_by"] = user['pk']
        self.data["description"] = multipart_form_data["description"]
        self.data["image"] = self.set_image(multipart_form_data)
        self.clear_empty_data()
        self.nested_data = {}
        self.nested_data["tags"] = self.set_tags(multipart_form_data)

    def set_id(self, multipart_form_data):
        if 'data_id' not in multipart_form_data:
            return str(uuid.uuid4().int)
        else:
            return multipart_form_data['data_id']

    def set_image(self, multipart_form_data):
        if 'image' not in multipart_form_data:
            return None
        elif type(multipart_form_data['image']) == str:
            return None
        else:
            return multipart_form_data['image']
        
    def set_tags(self, multipart_form_data):        
        if "tags[]" in multipart_form_data.keys():
            tags = multipart_form_data.getlist("tags[]")
            if "" in tags:
                tags.remove("")
        else:
            tags = []
        return tags

    def clear_empty_data(self):
        for key in list(self.data.keys()):
            if self.data[key] == None:
                del self.data[key]

    def write_data(self):
        try:
            old_data = Data1Model.objects.get(data_id=self.data['data_id']) #update
            serializer = Data1Serializer(old_data, data=self.data)            
        except:
            serializer = Data1Serializer(data=self.data) #create          
        if serializer.is_valid():
            serializer.save()
            self.write_nested_data()
        else:
            #print(serializer.errors)
            pass

    def write_nested_data(self):
        print("nd",self.nested_data)
        old_tags = Data1TagModel.objects.filter(data1=self.data['data_id'])
        for tag in old_tags:
            tag.delete()
        for tag in self.nested_data['tags']:
            if tag == "":
                pass
            else:
                data1 = Data1Model.objects.get(data_id=self.data['data_id'])
                Data1TagModel.objects.create(data1=data1,tag_text=tag)