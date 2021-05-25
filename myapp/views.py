from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import  LoginView, LogoutView
from django.urls import reverse

from .forms import CreateUserForm

import pyodbc
server_name = 'localhost'
db_name = 'school'
username = 'SA'
password = 'Postgres123'
conn = pyodbc.connect(
                      'Driver={ODBC Driver 17 for SQL Server};'
                      f'Server={server_name};'
                      f'Database={db_name};'
                      f'UID={username};'
                      f'PWD={password};'
                      'Mars_Connection=Yes;'
                     )
cursor = conn.cursor()

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            cursor.execute("INSERT INTO myapp_student_test(name) VALUES (?, ?)", name, email)
            conn.commit()

            messages.success(request, 'Регистрация прошла успешна')
            return redirect('login')

    context = {'form':form}
    return render(request, 'myapp/register.html', context)

def loginPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)
        if user.username == 'admin':
            login(request, user)
            return redirect('teacher_menu')
        elif user is not None:
            login(request, user)
            return redirect('student_menu')
    context = {}
    return render(request, 'myapp/login.html', context)

def studentMenu(request):
    return render(request, 'users/student_menu.html')


#----------------------------------------------------------------------ADMINS TEMA
def teacherMenu(request):
    return render(request, 'admin/teacher_menu.html')

def studentsView(request):
    return render(request, 'admin/students.html')

def lessonsView(request):
    return render(request, 'admin/lessons.html')

def sectionsView(request):
    return render(request, 'admin/sections.html')

def booksView(request):
    return render(request, 'admin/books.html')

def subjectView(request):
    return render(request, 'admin/subject.html')

#
# def test_sql(request):
#     name = 'Yeldos'
#     # cursor.execute("SELECT * FROM test_table")
#     # for row in cursor:
#     #     print(row)
#     cursor.execute ("insert into test_table (name) values (?)",name)
#     cursor.commit()
#     # context = {'result':result}
#     return render(request, 'myapp/sql.html')

def teacherMenu(request):
    pass



def test_sql(request):
    cursor.execute("SELECT * FROM teacher")
    for row in cursor:
        print(row)
    return render(request, 'myapp/sql.html')


def SelectAllStudents(request):
    return render()

def DeleteStundent(request, pk):
    pass

