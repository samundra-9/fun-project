"""recipie_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipie.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base),
    path('recipies/', recipies), 
    path('delete/<int:id>/', delete_recipie),
    path('update/<int:id>/', update_recipie),
    path('login/', login_page),
    path('register/', register_page),
    path('logout/', logout_page),
    path('students/', get_students),
    path('see_marks/<str:student_id>/', see_marks, name='see_marks'), 
    path('admin/', admin.site.urls),

] 

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
