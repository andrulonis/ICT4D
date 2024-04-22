from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.xml', {}, content_type='text/xml')
