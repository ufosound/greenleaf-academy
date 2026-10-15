from django.urls import path
from . import views

urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/quiz/', views.take_quiz, name='take_quiz'),
    path('final/', views.final_exam, name='final_exam'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.user_register, name='register'),
    path('contact/', views.contact_methodist, name='contact_methodist'),
]