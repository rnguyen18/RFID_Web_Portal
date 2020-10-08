from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from .models import Form_Entry
from django.contrib import messages


def home(request):
    return render(request, 'walmart/home.html')

def form(request):
    if request.method == 'POST':
        form_entry = Form_Entry(ID = Form_Entry.objects.count(),
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
                                modelName = request.POST.get("modelName"))
        form_entry.clean_fields()
        # form_entry.save()
        messages.success(request, "Form {} was successfully created!".format(form_entry.ID))
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'walmart/form_new.html')

def edit_form(request):
    context = {
        'entry' : Form_Entry.objects.first()
    }
    return render(request, 'walmart/vender_form.html', context)

def search_form(request):
    if request.method == 'POST':
        return HttpResponseRedirect(request.POST.get("formId"))
    else:
        return render(request, 'walmart/form_search.html')

class FormDetailView(DetailView):
    model = Form_Entry
    template_name='walmart/form_detail.html'
