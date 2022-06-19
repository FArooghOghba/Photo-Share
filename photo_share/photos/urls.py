from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'photos'

urlpatterns = [
    path('login/', views.login_page_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('', views.gallery_view, name='gallery'),
    path('add/', views.add_photo_view, name='add'),
    path('photo/<str:pk>/', views.photo_view, name='photo'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
