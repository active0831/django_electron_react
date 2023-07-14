from django.db import models
from users.models import User

# Create your models here.

### [ Modify this ] ###

class Data1Model(models.Model):
    data_id = models.CharField(max_length=200, primary_key=True)
    data_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)

class Data1TagModel(models.Model):
    data1 = models.ForeignKey(Data1Model, on_delete=models.CASCADE)
    tag_text = models.CharField(max_length=100)    
    class Meta:
        unique_together = ['data1', 'tag_text']