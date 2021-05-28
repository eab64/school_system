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
            email = form.cleaned_data.get('email')
            cursor.execute("INSERT INTO implicant (name,surname,email) VALUES (?,?,?)", name, surname, email)
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
            print(username)
            student = cursor.execute('SELECT * FROM student WHERE name=?', username)
            rows = student.fetchall()
            print(rows)
            columns = [column[0] for column in student.description]
            print(columns)
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            context = {'students': result}
            return render(request, 'users/profile.html', context)
        return render(request, 'users/profile.html')

        # return redirect('student_menu')
    context = {}
    return render(request, 'myapp/login.html', context)


def studentMenu(request):
    return render(request, 'users/student_menu.html')


def studentProfile(request):
    return render(request, 'users/profile.html')


"""Нужен фильтр по студенту"""


def lessonsList(request):
    lessons = cursor.execute('exec SelectLesson')
    columns2 = [column[0] for column in lessons.description]

    result2 = []
    for row in lessons.fetchall():
        result2.append(dict(zip(columns2, row)))
    context = {'lessons': result2}
    print(result2)
    return render(request, 'users/lessons_list.html', context=context)


def sectionsList(request):
    lessons = cursor.execute('exec SelectLesson')
    columns2 = [column[0] for column in lessons.description]

    result2 = []
    for row in lessons.fetchall():
        result2.append(dict(zip(columns2, row)))
    context = {'lessons': result2}
    print(result2)

    return render(request, 'users/sections_list.html', context=context)


# ----------------------------------------------------------------------ADMINS TEMA
def teacherMenu(request):
    teachers = cursor.execute('exec SelectAllTeachers')
    rows = teachers.fetchall()
    columns2 = [column[0] for column in teachers.description]
    result2 = []
    for row in rows:
        result2.append(dict(zip(columns2, row)))
    context = {'teachers': result2}
    # ----------------------------------------------------------------------------------------------
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        subject = request.POST.get('subject')
        salary = request.POST.get('salary')
        sql_teacher = ("""{ CALL CreateTeacher (@name=?, @surname=?, @subject=?, @salary=?) }""")
        params_teacher = (name, surname, salary, subject)
        cursor.execute(sql_teacher, params_teacher)
        cursor.commit()

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        success = request.POST.get('success')
        sql_qual = ("""{ CALL CreateQualification (@succes=?, @name=?, @surname=?) }""")
        params_qual = (success, first_name, last_name)
        cursor.execute(sql_qual, params_qual)
        cursor.commit()

        return redirect('/adminka/')
        # date = request.POST.get('date')
        # date = date.replace('T',' ')

        # date_with = datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')
        # print(date_with)
        # sql_qual = ("""{ CALL CreateQualification (@date=?, @succes=?, @name=?, @surname=?) }""")

    return render(request, 'admin/teacher_menu.html', context=context)


def studentsView(request):
    student = cursor.execute('SELECT * FROM student')

    columns = [column[0] for column in student.description]
    result = []
    for row in student.fetchall():
        result.append(dict(zip(columns, row)))
    context = {'students': result}

    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        classs = request.POST.get('class')

        sql_teacher = ("""{ CALL InsertStudentPayment (@name=?, @surname=?, @class=?) }""")
        params_teacher = (name, surname, classs)
        cursor.execute(sql_teacher, params_teacher)
        cursor.commit()
        return redirect('/students_view/')

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
        family = request.POST.get('family_status')
        cursor.execute('UPDATE implicant SET score = ?,  large_family_mamber = ? where name = ? AND surname = ?', score,
                       family, name, surname)
        cursor.commit()
        return redirect('/applicant_view/')

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
        return redirect('/lessons_view/')

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
        date = date.replace('T', ' ')
        date_with = datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')

        room = request.POST.get('room')

        sql = ("""{ CALL CreateSection (@class=?, @startDate=?, @room=?, @subject=?) }""")
        params = (name, date_with, room, subject)
        cursor.execute(sql, params)
        cursor.commit()
        return redirect('/sections_view/')

    return render(request, 'admin/sections.html', context)


"""ОЧЕНЬ МНОГОЕ НАДО ПОМЕНЯТЬ
Я сам вызыву жай select all
ДЛЯ списка должников вызывается процедура TACKAWAY
просто отдает спискок должников надо бы заполнить тоже людьми для показа с годом больше 1го"""


def booksView(request):
    debt_students = cursor.execute('exec GetStudentsWithBooks')
    rows = debt_students.fetchall()
    print(rows)
    columns2 = [column[0] for column in debt_students.description]
    print(columns2)
    result2 = []
    for row in rows:
        result2.append(dict(zip(columns2, row)))
    print(result2)

    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        classs = request.POST.get('class')
        book = request.POST.get('book')
        print(name)
        print(surname)
        print(classs)
        print(book)

        sql = ("""{ CALL TakeBook (@name=?, @surname=?, @class=?, @book=?) }""")
        params = (name, surname, classs, book)
        cursor.execute(sql, params)
        cursor.commit()
        return redirect('/books_view/')

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
        return redirect('/books_create/')
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
        return redirect('/subject_view/')
        messages.add_message(request, messages.INFO, 'Success')

    return render(request, 'admin/subject.html', context=context)


def addToClass(request):
    if request.method == "POST":
        name_to_add = request.POST.get('first_name')

        name = request.POST.get('name')
        surname = request.POST.get('surname')
        classs = request.POST.get('class')
        print(name)
        print(surname)
        print(classs)
        sql = ("""{ CALL InsertStudentIntoClass (@name=?, @surname=?, @class=?) }""")
        params = (name, surname, classs)
        cursor.execute(sql, params)
        cursor.commit()
        return redirect('/add_class/')

        messages.add_message(request, messages.INFO, 'Success')

    return render(request, 'admin/classes.html')

# ----------------------------------------------------------------------------------------------
"""ЗДЕСЬ НАЧИНАЮТСЯ ВСЕ ФОРМЫ КОТОРЫЕ ПОСЛЕ ПРОСТО ПЕРЕНОСИМ В view и кусок его html добавляем в MAIN
ПРОСТО БЕРЕШЬ СОЗДАЕШЬ ПЕРЕМЕННЫЕ с полученных ДАННЫХ и с ними делаешь ЗАПРОС и все
ТУТ ПО СУТИ ОДНИ inserts поэтому процедура примет данные и сама INSERT в первом примере уже есть готовый шаблон
Если INSERT то его"""
