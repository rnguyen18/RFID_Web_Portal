from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode
from .utils import create_pdf


class Vendor_Form(models.Model):
    ID = models.IntegerField(primary_key=True)
    vendorName = models.CharField(max_length=100)
    vendorNumber = models.IntegerField()
    senderName = models.CharField(max_length=100)
    senderEmail = models.EmailField()
    senderCountryOfOrigin = models.CharField(max_length=100)
    walmartBuyerName = models.CharField(max_length=100)
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
    images = models.ImageField(upload_to="images", blank=True)
    model_barcode = models.ImageField(upload_to="barcodes", blank=True)
    model_qrcode = models.ImageField(upload_to='qr_codes', blank=True)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(str(self.getEAN(self.ID)), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.model_barcode.save(f'{self.ID}.png', File(buffer), save=False)

        image = Image.open(self.model_barcode)
        (width, height) = image.size
        heightRatio = int(height / 100)
        newWidth = int(width * heightRatio)
        size = (newWidth, 100)
        image = image.resize(size, Image.ANTIALIAS)

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
            self.modelName) + "\n" + str(self.privateBrand) + "\n" + str(self.proprietaryBrand) + "\n" + str(
            self.supplierBrand) + "\n" + str(self.nationalBrand)