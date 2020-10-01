from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from .models import Form_Entry, Entry_Form


def home(request):
    return render(request, 'walmart/home.html')

def form(request):
    if request.method == 'POST':
        print(request.POST.get("venderName"))
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'walmart/vender_form.html')

def edit_form(request):
    context = {
        'entry' : Form_Entry.objects.first()
    }
    return render(request, 'walmart/vender_form.html', context)

class FormDetailView(DetailView):
    model = Form_Entry
    template_name='walmart/form_entry.html'
