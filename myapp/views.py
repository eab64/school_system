from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import  LoginView, LogoutView
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CreateUserForm, TeacherForm, StudentForm, LessonForm, BookForm, SectionsForm, SubjectForm

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

            cursor.execute("INSERT INTO implicant(name) VALUES (?)", name)
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
    teachers = cursor.execute('exec SelectAllTeachers')
    students = cursor.execute('SELECT * FROM student')
    columns = [column[0] for column in students.description]
    result = []
    for row in students.fetchall():
        result.append(dict(zip(columns, row)))

    result2 = []
    for row in teachers.fetchall():
        result.append(dict(zip(columns, row)))

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            subject = form.cleaned_data.get('subject')
            salary = form.cleaned_data.get('salary')
            sql = ("""{ CALL CreateTeacher (@name=?, @surname=?, @subject=?, @salary=?) }""")
            params = (name, surname, salary, subject)
            cursor.execute(sql, params)
            cursor.commit()
            return HttpResponseRedirect('/adminka')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherForm()
    context = {'students':result,
               'teacher':result2}
    return render(request, 'admin/teacher_menu.html', context)

def NotQualStudentsView(request):
    implicants = cursor.execute('SELECT * FROM student')
    columns = [column[0] for column in implicants.description]
    result = []
    for row in implicants.fetchall():
        result.append(dict(zip(columns, row)))
    context = {'implicants':result}
    return render(request, 'admin/students.html', context)

def lessonsView(request):
    teachers = cursor.execute('exec SelectLessons')
    columns = [column[0] for column in teachers.description]

    result = []
    for row in teachers.fetchall():
        result.append(dict(zip(columns, row)))
    context = {'lessons':result}
    return render(request, 'admin/lessons.html',context)

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

# def teacherMenu(request):
#     pass



def test_sql(request):
    cursor.execute("SELECT * FROM teacher")
    for row in cursor:
        print(row)
    return render(request, 'myapp/sql.html')


def SelectAllStudents(request):
    return render()

def DeleteStundent(request, pk):
    pass


from django.http import HttpResponseRedirect
from django.shortcuts import render


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            subject = form.cleaned_data.get('subject')
            salary = form.cleaned_data.get('salary')
            sql = ("""{ CALL CreateTeacher (@name=?, @surname=?, @subject=?, @salary=?) }""")
            params =(name, surname, salary, subject)
            cursor.execute(sql, params)
            cursor.commit()
            return HttpResponseRedirect('/test_form')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherForm()

    return render(request, 'myapp/test_html.html', {'form': form})


def studentCreate(request):# Zakon4it nado
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            score = form.cleaned_data.get('score')
            cursor.execute("UPDATE implicant SET score=%s WHERE name='yeldos3' AND surname='bolatov'", [score])
            cursor.commit()
            return HttpResponseRedirect('/student_create')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'myapp/student_test.html', {'form': form})


def lessonCreate(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            klass = form.cleaned_data.get('klass')
            subject = form.cleaned_data.get('subject')
            date = form.cleaned_data.get('date')
            room = form.cleaned_data.get('room')
            sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
            params = (klass, date, room, subject)
            cursor.execute(sql, params)
            cursor.commit()

            return HttpResponseRedirect('/lesson_create')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = LessonForm()

    return render(request, 'myapp/Lesson_test.html', {'form': form})


def sectionCreate(request):
    if request.method == 'POST':
        form = SectionsForm(request.POST)
        if form.is_valid():
            classs = form.cleaned_data.get('klass')
            subject = form.cleaned_data.get('subject')
            date = form.cleaned_data.get('date')
            room = form.cleaned_data.get('room')
            # sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
            # params = (klass, date, room, subject)
            # cursor.execute(sql, params)
            # cursor.commit()

            # cursor.execute("UPDATE implicant SET score=%s WHERE name='yeldos3' AND surname='bolatov'", [score])
            # cursor.commit()
            return HttpResponseRedirect('/section_create')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = SectionsForm()

    return render(request, 'myapp/section_test.html', {'form': form})


def bookCreate(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('klass')

            # sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
            # params = (klass, date, room, subject)
            # cursor.execute(sql, params)
            # cursor.commit()

            # cursor.execute("UPDATE implicant SET score=%s WHERE name='yeldos3' AND surname='bolatov'", [score])
            # cursor.commit()
            return HttpResponseRedirect('/book_create')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookForm()

    return render(request, 'myapp/book_test.html', {'form': form})


def subjectCreate(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('klass')

            # sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
            # params = (klass, date, room, subject)
            # cursor.execute(sql, params)
            # cursor.commit()

            # cursor.execute("UPDATE implicant SET score=%s WHERE name='yeldos3' AND surname='bolatov'", [score])
            # cursor.commit()
            return HttpResponseRedirect('/subject_create')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubjectForm()

    return render(request, 'myapp/subject_test.html', {'form': form})



def take_info(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        print('post')
        data = request.data()
        return Response(data)







