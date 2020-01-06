from django.urls import path
from trading import views


urlpatterns = [
    path('trade/<int:id>', views.trade, name='trade'),
    path('sale/<int:id>', views.sale, name='sale'),
    path('all_transactions', views.all_transaction, name='all_transactions'),
    path('detail_transac/<int:id>', views.detail_transac, name='detail_transac'),
    path('abort_transac/<int:id>', views.abort_transac, name='abort_transac'),
    path('pay_card/<int:id>', views.pay_card, name='pay_card'),
    path('leader_board/', views.leader, name='leader'),
    path('delete_transac/<int:id>', views.delete_transac, name='delete_transac'),
    path('cards/', views.cards, name="cards"),
    path('delete_card/<int:id>', views.delete_card, name='delete_card'),
    ]