from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('produto', views.produto_list, name='produto_list'),
    path('produto/<int:pk>/', views.detail_prod, name='detail_prod'),
    path('add/', views.ProdutoCreate.as_view(), name='produto_add'),
    path('add/submit', views.produto_submit, name='produto_submit'),
    path('<int:pk>/edit/submit', views.detail_prod, name='detail_prod'),
    

    path('<int:pk>/edit/', views.ProdutoUpdate.as_view(), name='produto_edit'),
    path('produto/<int:pk>/json/', views.produto_json, name='produto_json'),
    path('estoque', views.ent_estoque, name='ent_estoque'),
    path('estoque/<int:pk>/', views.ent_estoque_detail, name='ent_estoque_detail'),
    path('estoque/add/', views.ent_estoque_form, name='ent_estoque_form'),
    path('estoque/saida/', views.sai_estoque, name='sai_estoque'),
    path('estoque/saida/<int:pk>/', views.sai_estoque_detail, name='sai_estoque_detail'),
    path('saida/', views.sai_estoque_form, name='sai_estoque_form'),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),

    path('parceiro/', views.parceiro_list, name='parceiro_list'),
    path('parceiro/<int:pk>/', views.parceiro_detail, name='parceiro_detail'),
    path('parceiro/add/', views.ParceiroCreate.as_view(), name='parceiro_add'),
    path('parceiro/<int:pk>/edit/', views.ParceiroUpdate.as_view(), name='parceiro_edit'),



]   
