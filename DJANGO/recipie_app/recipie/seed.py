from faker import Faker
import random
from .models import *
fake = Faker()

def seed_db(n=10)->None:
    try:
        for i in range(0,n):
            departments_obj = Department.objects.all()
            random_idx = random.randint(0, len(departments_obj)-1)
            department_name = departments_obj[random_idx]
            student_id = f'STUD-0{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = fake.random_int(min=18, max=30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)
            Student.objects.create(department_name=department_name, student_id=student_id_obj, student_name=student_name, student_email=student_email, student_age=student_age, student_address=student_address) 
    except Exception as e:
        print(e)
        print('Error in seeding the database')  