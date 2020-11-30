from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files import File

import os
from django.conf import settings
from django.contrib.staticfiles import finders


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path

def create_pdf(context={}):
    template_path= 'walmart/vendorformtemplate.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="VendorForm.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=fetch_resources)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>').content
    return response.content

def render_to_pdf(template_path, context={}):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="VendorForm.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=fetch_resources)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>').content
    return response.content