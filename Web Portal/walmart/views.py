from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView, UpdateView
from .models import Vendor_Form
from django.contrib import messages


def home(request):
    return render(request, 'walmart/home.html')

def form(request):
    if request.method == 'POST':
        form_entry = Vendor_Form(ID = Vendor_Form.objects.count(),
                                vendorName = request.POST.get("vendorName"),
                                vendorNumber = request.POST.get("vendorNumber"),
                                senderName = request.POST.get("senderName"),
                                senderEmail = request.POST.get("senderEmail"),
                                senderCountryOfOrigin = request.POST.get("senderCountryOfOrigin"),
                                walmartBuyerName = request.POST.get("walmartBuyerName"),
                                upcEAN = request.POST.get("upcEAN"),
                                itemType = request.POST.get("itemType"),
                                departmentNumber = request.POST.get("departmentNumber"),
                                inlaySpec = request.POST.get("inlaySpec"),
                                inlayDeveloper = request.POST.get("inlayDeveloper"),
                                modelName = request.POST.get("modelName"),
                                privateBrand = request.POST.get("privateBrand"),
                                proprietaryBrand = request.POST.get("proprietaryBrand"),
                                supplierBrand = request.POST.get("supplierBrand"),
                                nationalBrand = request.POST.get("nationalBrand"))
        form_entry.clean_fields()
        form_entry.save()
        messages.success(request, "Form {} was successfully created!".format(form_entry.ID))
        return HttpResponseRedirect(reverse('form-detail', args=[form_entry.ID]))
    else:
        return render(request, 'walmart/form_new.html')

def edit_form(request):
    context = {
        'entry' : Form_Entry.objects.first()
    }
    return render(request, 'walmart/vender_form.html', context)

def search_form(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('form-detail', args=(request.POST.get("formId"))))
    else:
        return render(request, 'walmart/form_search.html')

class FormDetailView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Vendor_Form
    template_name='walmart/form_detail.html'
    
    def test_func(self):
        return True

class FormUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Vendor_Form
    template_name='walmart/form_update.html'

    def test_func(self):
        return True

class FormDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Vendor_Form
    template_name='walmart/form_delete.html'
    
    def test_func(self):
        return True


