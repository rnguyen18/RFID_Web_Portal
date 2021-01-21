from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView, UpdateView, View
from .models import Vendor_Form
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .utils import render_to_pdf, create_pdf


def home(request):
    return render(request, 'walmart/home.html')


def form(request):
    if request.method == 'POST':
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
                                 images=request.FILES.get("photoFiles"))
        form_entry.clean_fields()
        form_entry.save()
        messages.success(request, "Form {} was successfully created!".format(form_entry.ID))

        subject = 'Vender Form {}'.format(form_entry.ID)
        message = 'Hello {},\n\nWe have received your vender form and it is attached below as well!\n\nThanks,\nAuburn RFID Lab'.format(
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
    else:
        return render(request, 'walmart/form_new.html')


def edit_form(request):
    context = {
        'entry': Vendor_Form.objects.first()
    }
    return render(request, 'walmart/vender_form.html', context)


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


class FormPDFView(DetailView):
    model = Vendor_Form

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        data = {
            'object': self.get_object(),
            'model_barcode': obj.model_barcode.url
        }

        pdf = render_to_pdf('walmart/vendorformtemplate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')