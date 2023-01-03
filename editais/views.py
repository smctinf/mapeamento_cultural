from django.shortcuts import render

# Create your views here.
def editais(request):
    context={}
    return render(request, 'editais/editais.html', context)

def editais2(request):
    context={}
    return render(request, 'editais/editais2.html', context)