from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from accounts import views
from cards_game import settings


urlpatterns= [
    path('profile/<int:id>', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('create_profile/<str:username>', views.new_profile, name='new_profile'),
    path('all_user/', views.all_user, name='all_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
