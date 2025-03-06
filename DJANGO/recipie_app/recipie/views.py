from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
def recipies(request):
    # return HttpResponse("Hello, world. You're at the recipies index.")
    if request.method == 'POST':
        data = request.POST
        recipie_image = request.FILES.get('recipie_image')
        recipie_name = data['recipie_name'] # this will raise an error if the key is not found
        recipie_description = data.get('recipie_description') #  will return None if the key is not found
        print(recipie_name, recipie_description)
        print(recipie_image)
        Recipie.objects.create(
            recipie_name=recipie_name,
            recipie_description=recipie_description,
            recipie_image=recipie_image
        )
        return redirect('/recipies/')  # redirect to the same page
    queryset = Recipie.objects.all()

    if request.GET.get('search'):
        print(request.GET.get('search'))
        queryset = Recipie.objects.filter(recipie_name__icontains=request.GET.get('search'))

    context = {
        'recipies': queryset
    }
    return render(request, 'recipies.html', context)

def home(request):
    return render(request, 'home.html')

def delete_recipie(request, id):
    Recipie.objects.get(id=id).delete()
    return redirect('/recipies/')  # redirect to the same page

def update_recipie(request, id):
    recipie = Recipie.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipie_image = request.FILES.get('recipie_image')
        recipie_name = data['recipie_name'] # this will raise an error if the key is not found
        recipie_description = data.get('recipie_description') #  will return None if the key is not found
        recipie.recipie_name = recipie_name
        recipie.recipie_description = recipie_description
        if recipie_image:
            recipie.recipie_image = recipie_image
        recipie.save()
        return redirect('/recipies/')  # redirect to the same page
    context = {
        'recipie': recipie
    }
    return render(request, 'update_recipie.html', context)