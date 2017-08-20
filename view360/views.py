from django.shortcuts import render

# Create your views here.
def TestView(request):
    return render(request, 'view360/view360_base.html')
