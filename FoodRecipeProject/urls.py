"""FoodRecipeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('index_recipe/', index_recipe, name="index_recipe"),
    path('user_index/', user_index, name="user_index"),
    path('admin_index/', admin_index, name="admin_index"),
    path('user_Login/', user_Login, name="user_Login"),
    path('admin_login/', admin_login, name="admin_login"),
    path('logout_user/', logout_user, name="logout_user"),
    path('logout_admin/', logout_admin, name="logout_admin"),
    path('user_registration/', user_registration, name="user_registration"),
    path('reg_user/', reg_user, name="reg_user"),
    path('add_recipe/', add_recipe, name="add_recipe"),
    path('edit_recipe/<int:pid>', add_recipe, name="edit_recipe"),
    path('delete_recipe/<int:pid>', delete_recipe, name="delete_recipe"),
    path('manage_recipe/', manage_recipe, name="manage_recipe"),
    path('add_comment/<int:pid>', add_comment, name="add_comment"),
    path('change-comment-status/<int:pid>/', change_comment_status, name="change_comment_status"),
    path('commentlist/', commentlist, name="commentlist"),
    path('admin_comment_apply/', admin_comment_apply, name="admin_comment_apply"),
    path('admin_manage_recipe/', admin_manage_recipe, name="admin_manage_recipe"),
    path('user_recipe/<int:pid>', user_recipe, name="user_recipe"),
    path('add_contact/', add_contact, name="add_contact"),
    path('edit_contact/<int:pid>/', edit_contact, name="edit_contact"),
    path('contactlist/', contactlist, name="contactlist"),
    path('delete_contact/<int:pid>/', delete_contact, name="delete_contact"),
    path('user_profile/', user_profile, name="user_profile"),
    path('user_change_password/', user_change_password, name="user_change_password"),
    path('search_recipe/', search_recipe, name="search_recipe"),
    path('admin_search_recipe/', admin_search_recipe, name="admin_search_recipe"),
    path('admin_user_report/', admin_user_report, name="admin_user_report"),
    path('admin_recipe_report/', admin_recipe_report, name="admin_recipe_report"),
    path('admin_change_password/', admin_change_password, name="admin_change_password"),
    path('comment/<int:pid>', comment, name="comment"),
    path('admin_edit_recipe/<int:pid>', admin_edit_recipe, name="admin_edit_recipe"),
    path('admin_delete_recipe/<int:pid>', admin_delete_recipe, name="admin_delete_recipe"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('index_about/', index_about, name="index_about"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
