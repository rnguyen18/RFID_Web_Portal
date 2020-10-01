from django.db import models
from django.forms import ModelForm


class Form_Entry(models.Model):
    ID = models.IntegerField(primary_key=True)
    venderName = models.CharField(max_length=100)
    venderNumber = models.IntegerField()
    senderName =  models.CharField(max_length=100)
    senderEmail = models.EmailField()
    senderCountryOfOrigin =  models.CharField(max_length=100)
    walmartBuyerName =  models.CharField(max_length=100)
    upcEAN = models.IntegerField()
    itemType = models.CharField(max_length=100)
    departmentNumber = models.IntegerField()
    inlaySpec = models.CharField(max_length=100)
    inlayDeveloper = models.CharField(max_length=100)
    modelName = models.CharField(max_length=100)

    def __str__(self):
        return "{}, {}".format(self.venderName, self.upcEAN)

class Entry_Form(ModelForm):
    class Meta:
        model = Form_Entry
        fields = ['venderName', 'venderNumber', 'senderName', 'senderEmail',
                  'senderCountryOfOrigin', 'walmartBuyerName', 'upcEAN', 'itemType', 'departmentNumber', 
                  'inlaySpec', 'inlayDeveloper', 'modelName']