from django.urls import path
from . import views

urlpatterns = [
    path('', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name='login'),
    path('student_menu/', views.studentMenu, name='student_menu'),
    path('student_profile/', views.studentProfile, name='student_profile'),

    path('adminka/', views.teacherMenu, name='teacher_menu'),
    path('applicant_view/', views.NotQualStudentsView, name = 'applicantView'),
    path('students_view/', views.studentsView, name='studentsView'),

    path('lessons_view/', views.lessonsView, name = 'lessonsView'),
    path('sections_view/', views.sectionsView, name = 'sectionsView'),
    path('books_view/', views.booksView, name = 'booksView'),
    path('books_create/', views.bookCreate, name='booksCreate'),
    path('subject_view/', views.subjectView, name='subjectView'),

    # path('teacher_main/', views.adminView, name='teacher_main')
#     path('second_login/', views.secondLogin, name = 'second_login'),
#     path('second_register/', views.secondRegister, name = 'second_register')

    # path('test_sql/', views.test_sql),
    # path('test_form/', views.get_name),
    # path('student_create/', views.studentCreate),
    # # path('lesson_create/', views.lessonCreate),
    # path('section_create/', views.sectionCreate),
    # path('book_create/', views.bookCreate),
    # path('subject_creat/', views.subjectCreate),

    path('take_info/', views.take_info)


]