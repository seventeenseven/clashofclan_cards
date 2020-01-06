from django.urls import path
from forum import views


urlpatterns = [
    path('threads/', views.threads, name='threads'),
    path('thread/<int:id>', views.thread, name='thread'),
    path('delete_com/<int:id>', views.delete_com, name='delete_com'),
    path('delete_thread/<int:id>', views.delete_thread, name='delete_thread'),
    ]