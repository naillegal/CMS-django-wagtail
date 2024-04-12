from django.urls import path
from .views import register,login,custom_logout,create_blog,delete_blog,edit_blog

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('create-blog/', create_blog, name='create_blog'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/delete/', delete_blog, name='delete_blog'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/edit/', edit_blog, name='edit_blog'),
]
