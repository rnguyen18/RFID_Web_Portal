from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from .models import Form_Entry


def home(request):
    return render(request, 'walmart/home.html')

def form(request):
    if request.method == 'POST':
        form_entry = Form_Entry(request.POST)
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
