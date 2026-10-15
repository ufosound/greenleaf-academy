from django.urls import path, include
from courses.views import user_login
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from courses.admin import admin_site # Импортируем нашу кастомную админку

urlpatterns = [
    path('admin/', admin_site.urls), # Используем admin_site вместо admin.site
    path('login/', user_login, name='login'),
    path('', TemplateView.as_view(template_name='courses/home.html'), name='home'),
    path('app/', include('courses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)