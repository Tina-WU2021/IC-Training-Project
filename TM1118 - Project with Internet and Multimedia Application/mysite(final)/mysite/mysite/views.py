from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mysite/index.html') # Pass the context to HTML template