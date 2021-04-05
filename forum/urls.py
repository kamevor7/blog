from . import views
from django.urls import path
from .views import UserEditView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', views.change_password, name='change_password'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_list/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('user_list/<int:pk>/delete/', views.del_user, name='del_user'),
    path('user_list/<int:pk>/upgrade/', views.upgrade_user, name='upgrade'),
    path('user_list/<int:pk>/downgrade/', views.downgrade_user, name='downgrade'),
    path('user_list/<int:pk>/suspend/', views.suspend_user, name='suspend'),
    path('user_list/<int:pk>/activate/', views.activate_user, name='activate'),
    path('product_list', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
    path('create', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('process', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),

]
