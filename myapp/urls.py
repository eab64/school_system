from django.urls import path
from . import views

urlpatterns = [
    path('', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name='login'),
    path('student_menu/', views.studentMenu, name='student_menu'),

    path('adminka/', views.teacherMenu, name='teacher_menu'),
    path('students_view/', views.studentsView, name = 'studentsView'),
    path('lessons_view/', views.lessonsView, name = 'lessonsView'),
    path('sections_view/', views.sectionsView, name = 'sectionsView'),
    path('books_view/', views.booksView, name = 'booksView'),
    path('subject_view/', views.subjectView, name = 'subjectView'),

    # path('teacher_main/', views.adminView, name='teacher_main')
#     path('second_login/', views.secondLogin, name = 'second_login'),
#     path('second_register/', views.secondRegister, name = 'second_register')

    path('test_sql/', views.test_sql)
]