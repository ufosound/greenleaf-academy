from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Lesson, Question, Answer, UserProgress

class GreenLeafAdminSite(AdminSite):
    site_header = "Администрирование Академии Greenleaf"
    site_title = "Greenleaf Academy"
    index_title = "Панель управления"

admin_site = GreenLeafAdminSite(name='greenleaf_admin')

# Делаем ответы частью страницы вопроса
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2 # Показывать 2 пустых поля для новых ответов сразу

@admin.register(Lesson, site=admin_site)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Question, site=admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson')
    list_filter = ('lesson',)
    inlines = [AnswerInline] # Добавляем ответы прямо сюда

@admin.register(UserProgress, site=admin_site)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed')
    list_filter = ('is_completed', 'lesson')