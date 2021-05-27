from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
import locale

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
            surname = form.cleaned_data.get('last_name')
            cursor.execute("INSERT INTO implicant (name,surname) VALUES (?,?)", name, surname)
            conn.commit()

            messages.success(request, 'Регистрация прошла успешна')
            return redirect('login')

    context = {'form': form}
    return render(request, 'myapp/register.html', context)


"""NUJNA PROVERKA EWE I NA APPLICANTA esli ne student to tolko view menu"""


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user.username == 'admin':
            login(request, user)
            return redirect('teacher_menu')
        elif user is not None:
            login(request, user)

            student = cursor.execute('SELECT * FROM student WHERE name=?', username)
            context = {'student': student}
            return render(request, 'users/profile.html', context)
            # return redirect('student_menu')
    context = {}
    return render(request, 'myapp/login.html', context)


def studentMenu(request):
    return render(request, 'users/student_menu.html')


def studentProfile(request):
    return render(request, 'users/profile.html')


# ----------------------------------------------------------------------ADMINS TEMA
def teacherMenu(request):
    teachers = cursor.execute('exec SelectAllTeachers')

    columns2 = [column[0] for column in teachers.description]

    result2 = []
    for row in teachers.fetchall():
        result2.append(dict(zip(columns2, row)))
    context = {'teachers': result2}

    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        subject = request.POST.get('subject')
        salary = request.POST.get('salary')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        success = request.POST.get('success')
        date = request.POST.get('date')
        # date = date.replace('T',' ')

        # date_with = datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')
        # print(date_with)
        sql_qual = ("""{ CALL CreateQualification (@date=?, @succes=?, @name=?, @surname=?) }""")
        # sql_teacher = ("""{ CALL CreateTeacher (@name=?, @surname=?, @subject=?, @salary=?) }""")
        params_teacher = (name, surname, salary, subject)
        params_qual = (date, success, first_name, last_name)
        cursor.execute(sql_qual, params_qual)
        # cursor.execute(sql_teacher, params_teacher)
        cursor.commit()
    return render(request, 'admin/teacher_menu.html', context=context)


def studentsView(request):
    student = cursor.execute('SELECT * FROM student')

    columns = [column[0] for column in student.description]
    result = []
    for row in student.fetchall():
        result.append(dict(zip(columns, row)))
    context = {'students': result}

    return render(request, 'admin/students.html', context=context)


def NotQualStudentsView(request):
    implicants = cursor.execute('SELECT * FROM implicant WHERE score IS NULL')
    rows = implicants.fetchall()
    column_names = [d[0] for d in cursor.description]

    columns = [column[0] for column in implicants.description]
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))
    context = {'implicants': result}
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        score = request.POST.get('score')
        cursor.execute('UPDATE implicant SET score = ? where name = ? AND surname = ?', score, name, surname)
        cursor.commit()
        print(name)
        print(surname)
        print(score)

    return render(request, 'admin/applicants.html', context)


"""Здесь скорее всего про lessons?  КОРОЧ ОН ТУПИЛ ПОТОМУЧТО МЫ ИХ НЕ СОЗДАЛИ,
 МОЖНО ВПРИНЦИПЕ РЕШИТЬ ВСЕ ПРОБЛЕМЫ ЗАДАВ ИХ СТАТИЧНО В НАЧАЛЕ"""


def lessonsView(request):
    lesson = cursor.execute('exec SelectLesson')
    rows = lesson.fetchall()
    columns2 = [column[0] for column in lesson.description]
    result2 = []
    for row in rows:
        result2.append(dict(zip(columns2, row)))
    print(result2)
    context = {'lessons': result2}
    if request.method == "POST":
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        date = date.replace('T', ' ')
        date_with = datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')

        room = request.POST.get('room')

        sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
        params = (name, date_with, room, subject)
        cursor.execute(sql, params)
        cursor.commit()

    return render(request, 'admin/lessons.html', context)


"""КОРОЧ ЗДЕСЬ ЧЕ ТА В в атрибутах какой то SUBJECT стоит, может поменять на КРУЖОК
Если мы как то привязываемся к ним
ТАКЖЕ В lessons and SECTIONS делаем обычный SELECT и все процедура только для создания
Для САНЖИКА вместо надо проитись по созданным переменным( NE XVATAET class v section)"""


def sectionsView(request):
    section = cursor.execute('exec SelectSection')
    rows = section.fetchall()
    columns2 = [column[0] for column in section.description]
    result2 = []
    for row in rows:
        result2.append(dict(zip(columns2, row)))
    print(result2)
    context = {'sections': result2}
    if request.method == "POST":
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        room = request.POST.get('room')

        print(name)
        print(subject)
        print(date)
        print(room)

    return render(request, 'admin/sections.html', context)


"""ОЧЕНЬ МНОГОЕ НАДО ПОМЕНЯТЬ
Я сам вызыву жай select all
ДЛЯ списка должников вызывается процедура TACKAWAY
просто отдает спискок должников надо бы заполнить тоже людьми для показа с годом больше 1го"""


def booksView(request):
    debt_students = cursor.execute('exec GetStudentsWithBooks')
    columns2 = [column[0] for column in debt_students.description]
    result2 = []
    for row in debt_students.fetchall():
        result2.append(dict(zip(columns2, row)))

    if request.method == "POST":
        name = request.POST.get('name')
        subject = request.POST.get('surname')
        date = request.POST.get('class')
        room = request.POST.get('book')
        cursor.commit()
        print(name)
        print(subject)
        print(date)
        print(room)
    context = {'debts': result2}
    return render(request, 'admin/books.html', context=context)


def bookCreate(request):
    books = cursor.execute('SELECT * FROM book')
    columns = [column[0] for column in books.description]

    result = []
    for row in books.fetchall():
        result.append(dict(zip(columns, row)))
    context = {'books': result}
    if request.method == "POST":
        adds = request.POST.get('one_book')
        cursor.execute("INSERT INTO book (name) VALUES (?)", adds)
        cursor.commit()
        print(adds)

    return render(request, 'admin/add_book.html', context=context)


def subjectView(request):
    subjects = cursor.execute('SELECT * FROM subject')
    columns = [column[0] for column in subjects.description]

    result2 = []
    for row in subjects.fetchall():
        result2.append(dict(zip(columns, row)))
    context = {'subjects': result2}
    if request.method == "POST":
        name = request.POST.get('name')
        cursor.execute('{call CreateSubject (?)}', name)
        print(name)
        cursor.commit()
        messages.add_message(request, messages.INFO, 'Success')

    return render(request, 'admin/subject.html', context=context)


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


def test_sql(request):
    cursor.execute("SELECT * FROM teacher")
    for row in cursor:
        print(row)
    return render(request, 'myapp/sql.html')


# ----------------------------------------------------------------------------------------------
"""ЗДЕСЬ НАЧИНАЮТСЯ ВСЕ ФОРМЫ КОТОРЫЕ ПОСЛЕ ПРОСТО ПЕРЕНОСИМ В view и кусок его html добавляем в MAIN
ПРОСТО БЕРЕШЬ СОЗДАЕШЬ ПЕРЕМЕННЫЕ с полученных ДАННЫХ и с ними делаешь ЗАПРОС и все
ТУТ ПО СУТИ ОДНИ inserts поэтому процедура примет данные и сама INSERT в первом примере уже есть готовый шаблон
Если INSERT то его"""


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
            params = (name, surname, salary, subject)
            cursor.execute(sql, params)
            cursor.commit()
            return HttpResponseRedirect('/test_form')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherForm()

    return render(request, 'myapp/test_html.html', {'form': form})


def studentCreate(request):  # Zakon4it nado
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


# def lessonCreate(request):
#     if request.method == 'POST':
#         form = LessonForm(request.POST)
#         if form.is_valid():
#             klass = form.cleaned_data.get('klass')
#             subject = form.cleaned_data.get('subject')
#             date = form.cleaned_data.get('date')
#             room = form.cleaned_data.get('room')
#             sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
#             params = (klass, date, room, subject)
#             cursor.execute(sql, params)
#             cursor.commit()
#
#             return HttpResponseRedirect('/lesson_create')
#
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = LessonForm()
#
#     return render(request, 'myapp/Lesson_test.html', {'form': form})


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


# def bookCreate(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data.get('klass')
#
#             # sql = ("""{ CALL CreateLesson (@class=?, @startDate=?, @room=?, @subject=?) }""")
#             # params = (klass, date, room, subject)
#             # cursor.execute(sql, params)
#             # cursor.commit()
#
#             # cursor.execute("UPDATE implicant SET score=%s WHERE name='yeldos3' AND surname='bolatov'", [score])
#             # cursor.commit()
#             return HttpResponseRedirect('/book_create')
#
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = BookForm()
#
#     return render(request, 'myapp/book_test.html', {'form': form})


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


def student_profile(request):
    """ОТДАТЬ ИНФУ ПРО СТУДЕНТА ЧИСТО СЕЛЕКТЫ"""
    pass
