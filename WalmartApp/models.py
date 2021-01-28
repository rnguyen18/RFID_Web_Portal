from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode
from .utils import create_pdf
from django.core.validators import RegexValidator
from django.shortcuts import reverse


class Vendor_Form(models.Model):
    ID = models.IntegerField(primary_key=True)
    vendorName = models.CharField(max_length=100)
    vendorNumber = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    senderName = models.CharField(max_length=100)
    senderEmail = models.EmailField()
    senderCountryOfOrigin = models.CharField(max_length=100)
    walmartBuyerName = models.CharField(blank=True, max_length=100)
    upcEAN = models.PositiveIntegerField()
    itemType = models.CharField(max_length=100)
    departmentNumber = models.CharField(max_length=3)
    inlaySpec = models.CharField(max_length=100)
    inlayDeveloper = models.CharField(max_length=100)
    modelName = models.CharField(max_length=100)
    brandName = models.CharField(max_length=100)
    brandType = models.CharField(max_length=100)
    images1 = models.ImageField(upload_to="images1", blank=True)
    images2 = models.ImageField(upload_to="images2", blank=True)
    images3 = models.ImageField(upload_to="images3", blank=True)
    images4 = models.ImageField(upload_to="images4", blank=True)
    images5 = models.ImageField(upload_to="images5", blank=True)
    model_qrcode = models.ImageField(upload_to='qr_codes', blank=True)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.getQRCodeData())
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.ID}' + '.png'
        buffer2 = BytesIO()
        canvas.save(buffer2, 'PNG')
        self.model_qrcode.save(fname, File(buffer2), save=False)
        canvas.close()

        pdf = create_pdf({'object': self})
        filename = "Vendor Form {}.pdf".format(self.ID)
        self.pdf.save(filename, File(BytesIO(pdf)), save=False)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('form-detail', args=[self.ID])

    def __str__(self):
        return "{}, {}".format(self.vendorName, self.upcEAN)

    def getEAN(self, id):
        string = str(id)
        for i in range(len(string), 12):
            string = "0" + string
        return string

    def getQRCodeData(self):
        return str(self.ID) + "\n" + str(self.vendorName) + "\n" + str(self.vendorNumber) + "\n" + str(
            self.senderName) + "\n" + str(self.senderEmail) + "\n" + str(self.senderCountryOfOrigin) + "\n" + str(
            self.walmartBuyerName) + "\n" + str(self.upcEAN) + "\n" + str(self.itemType) + "\n" + str(
            self.departmentNumber) + "\n" + str(self.inlaySpec) + "\n" + str(self.inlayDeveloper) + "\n" + str(
            self.modelName) + "\n" + str(self.brandName) + "\n" + str(self.brandType) + "\n"