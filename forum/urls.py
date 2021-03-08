from . import views
from django.urls import path
from .views import UserEditView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('blog/', views.blogs, name='blogs'),
    path('<int:blogs_id>/', views.detail, name='detail'),
    path('password/', views.change_password, name='change_password'),
    path('profile/', views.profile_edit, name='profile_edit'),
]
