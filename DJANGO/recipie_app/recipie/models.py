from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipie(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipie_name = models.CharField(max_length=100)
    recipie_description = models.TextField()
    recipie_image = models.ImageField(upload_to='recipie ', default='')
    

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.department_name
    
    class meta:
        ordering = ['department_name']

class StudentID(models.Model):
    student_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.student_id
    

class Student(models.Model):
    department_name = models.ForeignKey(Department, related_name='depart', on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.OneToOneField(StudentID, on_delete=models.SET_NULL, null=True, blank=True)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()

    def __str__(self):
        return self.student_name
    class meta:
        ordering = ['student_name']
        verbose_name = 'Student'

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name='studentmarks',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subjectmarks',on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} - {self.subject} - {self.marks}' 

    class meta:
        unique_together = ['student', 'subject']


class ReportCard(models.Model):
     student = models.ForeignKey(Student, related_name='reportcard',on_delete=models.CASCADE) 
     student_rank = models.IntegerField(default=0)
     date_of_reportcard_generation = models.DateField(auto_now_add=True ) 

     class meta:
         unique_together = ['student_rank', 'date_of_reportcard_generation'] 


# creating a abstract class 
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(unique=True)
    user_bio = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', default='profile_pic/default.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    