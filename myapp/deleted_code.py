

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
