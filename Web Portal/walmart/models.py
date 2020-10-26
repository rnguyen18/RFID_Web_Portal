from django.db import models
from django.contrib.auth.models import User


class Vendor_Form(models.Model):
    ID = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vendorName = models.CharField(max_length=100)
    vendorNumber = models.IntegerField()
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
    privateBrand = models.CharField(max_length=100)
    proprietaryBrand = models.CharField(max_length=100)
    supplierBrand = models.CharField(max_length=100)
    nationalBrand = models.CharField(max_length=100)

    def __str__(self):
        return "{}, {}".format(self.vendorName, self.upcEAN)