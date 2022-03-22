from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls', namespace='user')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('quiz.urls', namespace='quiz')),
]
