
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('user.urls')),

    path('ticket/', include('ticket.urls')),

    path('', include('core.urls')),

    path('comment/', include('comment.urls')),

    path('category/', include('category.urls')),
]
