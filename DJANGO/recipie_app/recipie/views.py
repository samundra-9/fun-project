from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Student

# Create your views here.
from .models import *


@login_required(login_url='/login/')
def recipies(request):
    # return HttpResponse("Hello, world. You're at the recipies index.")
    if request.method == 'POST':
        data = request.POST
        recipie_image = request.FILES.get('recipie_image')
        recipie_name = data['recipie_name'] # this will raise an error if the key is not found
        recipie_description = data.get('recipie_description') #  will return None if the key is not found
        # print(recipie_name, recipie_description)
        # print(recipie_image)
        Recipie.objects.create(
            recipie_name=recipie_name,
            recipie_description=recipie_description,
            recipie_image=recipie_image
        )
        return redirect('/recipies/')  # redirect to the same page
    queryset = Recipie.objects.all()

    if request.GET.get('search'): # search is from name attribute of input field
        # print(request.GET.get('search')) 
        queryset = Recipie.objects.filter(recipie_name__icontains=request.GET.get('search'))

    context = {
        'recipies': queryset
    }
    return render(request, 'recipies.html', context)



def base(request):
    return render(request, 'base.html')


@login_required(login_url='/login/')
def delete_recipie(request, id):
    Recipie.objects.get(id=id).delete()
    return redirect('/recipies/')  # redirect to the same page



@login_required(login_url='/login/')
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


# for login and logout
def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = User.objects.filter(username=username).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/recipies/')
        else:
            return render(request, 'login.html', context={"message":"Invalid username or password"})
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'register.html', context={"message":"username must be unique"})
        User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        return redirect('/login/')
    return render(request, 'register.html')

from django.db.models import Q, Sum

def get_students(request):
    students = Student.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        students = Student.objects.filter(
            Q(student_name__icontains=search) | 
            Q(student_email__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(department_name__department_name__icontains=search)
            )

    paginator = Paginator(students, 16)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'students': page_obj.object_list,
        
    }
    return render(request, 'students.html', context) 

from .seed import generate_report_card
def see_marks(request,student_id):
    # generate_report_card()
    querySet = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = querySet.aggregate(total_marks =Sum('marks'))
    # rank = list(Student.objects.annotate(total_marks=Sum('studentmarks__marks')).order_by('-total_marks','-student_age'))
    # print(rank)
    #  rank = [student.student_id.student_id for student in rank].index(student_id) + 1
    # rank = rank.index(next(student for student in rank if student.student_id == student_id)) + 1
    context = {
        'querySet': querySet,
        'total_marks': total_marks['total_marks'],
        'student_id': student_id,
        'student_name': querySet[0].student.student_name,
        # 'rank': rank
    }
    print(querySet)
    return render(request, 'see_marks.html', context)
    # return HttpResponse(f"Student ID: {student_id}")
   
