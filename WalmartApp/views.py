from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, View
from .models import Vendor_Form
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .utils import render_to_pdf, create_pdf
import re


def home(request):
    return render(request, 'walmart/home.html')


def form(request):
    if request.method == 'POST':

        context = {
            "object": {
                "vendorName": request.POST.get("vendorName"),
                "vendorNumber" : request.POST.get("vendorNumber"),
                "senderName" : request.POST.get("senderName"),
                "senderEmail" : request.POST.get("senderEmail"),
                "senderCountryOfOrigin" : request.POST.get("senderCountryOfOrigin"),
                "walmartBuyerName" : request.POST.get("walmartBuyerName"),
                "upcEAN" : request.POST.get("upcEAN"),
                "itemType" : request.POST.get("itemType"),
                "departmentNumber" : request.POST.get("departmentNumber"),
                "inlaySpec" : request.POST.get("inlaySpec"),
                "inlayDeveloper" : request.POST.get("inlayDeveloper"),
                "modelName" : request.POST.get("modelName"),
                "brandName" : request.POST.get("brandName"),
                "brandType" : request.POST.get("brandType"),
                "images" : request.FILES.get("photoFiles")
            }
        }
        error = False

        vNum = request.POST.get("vendorNumber")
        if not (vNum.isnumeric() and len(vNum) == 6):
            messages.error(request, "Invalid Vendor Number")
            error = True

        email = request.POST.get("senderEmail")
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
            messages.error(request, "Invalid Email")
            error = True

        upceanNum = request.POST.get("upcEAN")
        if not upceanNum.isnumeric():
            messages.error(request, "Invalid UPC/EAN Number")
            error = True

        itemType = request.POST.get("itemType")
        if itemType == "":
            messages.error(request, "Select an Item Type")
            error = True

        departmentNumber = request.POST.get("departmentNumber")
        if departmentNumber == "":
            messages.error(request, "Select a Department Number")
            error = True

        inlaySpec = request.POST.get("inlaySpec")
        if inlaySpec == "":
            messages.error(request, "Select an Inlay Spec")
            error = True

        inlayDev = request.POST.get("inlayDeveloper")
        if inlayDev == "":
            messages.error(request, "Select an Inlay Developer")
            error = True

        brandType = request.POST.get("brandType")
        if brandType == "":
            messages.error(request, "Select a Brand Type")
            error = True

        if error:
            return render(request, 'walmart/form_new.html', context)


        form_entry = Vendor_Form(ID=Vendor_Form.objects.count(),
                                 vendorName=request.POST.get("vendorName"),
                                 vendorNumber=request.POST.get("vendorNumber"),
                                 senderName=request.POST.get("senderName"),
                                 senderEmail=request.POST.get("senderEmail"),
                                 senderCountryOfOrigin=request.POST.get("senderCountryOfOrigin"),
                                 walmartBuyerName=request.POST.get("walmartBuyerName"),
                                 upcEAN=request.POST.get("upcEAN"),
                                 itemType=request.POST.get("itemType"),
                                 departmentNumber=request.POST.get("departmentNumber"),
                                 inlaySpec=request.POST.get("inlaySpec"),
                                 inlayDeveloper=request.POST.get("inlayDeveloper"),
                                 modelName=request.POST.get("modelName"),
                                 brandName=request.POST.get("brandName"),
                                 brandType=request.POST.get("brandType"),
                                 images1=request.FILES.get("photoFiles"),
                                 images2=request.FILES.get("photoFiles1"),
                                 images3=request.FILES.get("photoFiles2"),
                                 images4=request.FILES.get("photoFiles3"),
                                 images5=request.FILES.get("photoFiles4"))

        form_entry.clean_fields()
        form_entry.save()
        messages.success(request, "Form {} was successfully created!".format(form_entry.ID))

        subject = 'Vendor Form {}'.format(form_entry.ID)
        message = 'Hello {},\n\nWe have received your vendor form and it is attached below as well!\n\nThanks,\nAuburn RFID Lab'.format(
            form_entry.senderName)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form_entry.senderEmail]

        email = EmailMessage(
            subject,
            message,
            email_from,
            recipient_list,
            [''],
            reply_to=[''],
            headers={'Message-ID': 'foo'},
        )
        email.attach_file('media/pdfs/Vendor_Form_{}.pdf'.format(form_entry.ID))
        email.send()

        if request.user.is_active:
            return HttpResponseRedirect(reverse('form-detail', args=[form_entry.ID]))
        else:
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'walmart/form_new.html')


def view_form(request):
    context = {
        'forms' : Vendor_Form.objects.all()
    }
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('form-detail', args=(request.POST.get("formId"))))
    else:
        return render(request, 'walmart/form_view.html',context)


class FormDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vendor_Form
    template_name = 'walmart/form_detail.html'

    def test_func(self):
        form = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class FormEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vendor_Form
    fields = ["vendorName",
              "vendorNumber",
              "senderName",
              "senderEmail",
              "senderCountryOfOrigin",
              "walmartBuyerName",
              "upcEAN",
              "itemType",
              "departmentNumber",
              "inlaySpec",
              "inlayDeveloper",
              "modelName",
              "brandName",
              "brandType",
              "images1",
              "images2",
              "images3",
              "images4",
              "images5"
              ]
    template_name= 'walmart/form_update.html'

    def test_func(self):
        form = self.get_object()
        if self.request.user.is_staff:
            return True
        return False


class FormPDFView(DetailView):
    model = Vendor_Form

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {
            'object': self.get_object()
        }

        pdf = render_to_pdf('walmart/vendorformtemplate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')