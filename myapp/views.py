from django.shortcuts import render
from random import randint
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
 
from .models import *
from django import template

# Create your views here.

def index(request):
    data = Recipe.objects.all()
    return render(request, "home.html", locals())

@login_required(login_url='/user_Login/')
def user_index(request):
    recipes = Recipe.objects.filter(register__user=request.user)
    all_comments = Comment.objects.all()
    new_comments = Comment.objects.filter(status=1)
    rejected_comments = Comment.objects.filter(status=3)
    approval_comments = Comment.objects.filter(status=2)
    return render(request, "user_dashboard.html", locals())

def admin_index(request):
    users = Registration.objects.all()
    recipes = Recipe.objects.all()
    all_comments = Comment.objects.all()
    new_comments = Comment.objects.filter(status=1)
    rejected_comments = Comment.objects.filter(status=3)
    approval_comments = Comment.objects.filter(status=2)
    return render(request, "admin_dashboard.html", locals())

def index_about(request):
    data = About.objects.all()
    return render(request, "index_about.html", locals())


def admin_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('admin_index')
            else:
                messages.success(request, "Invalid User")
                return redirect('admin_login')
        except:
            messages.success(request, "Invalid User")
            return redirect('admin_login')
    return render(request, "admin_login.html")

def user_registration(request, pid=None):
    user = None
    register = None

    if pid:
        user = User.objects.get(id=pid)
        register = Registration.objects.get(user=user)

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES, instance=register)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(
                    email=request.POST['email'],
                    username=request.POST['email'],
                    first_name=request.POST['firstname'],
                    password=request.POST['password']
                )
                new_register = form.save(commit=False)
                new_register.user = new_user
                new_register.save()
                messages.success(request, "Registration Successful")
                return redirect('user_Login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
                return redirect('user_registration')
    else:
        form = RegistrationForm(instance=register)

    return render(request, 'user_register.html', {'form': form})

def user_Login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('user_Login')
            else:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('user_index')
        else:
            messages.success(request, "Invalid User")
            return redirect('user_Login')
    return render(request, "user_login.html")

@login_required(login_url='/user_Login/')
def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('user_Login')

@login_required(login_url='/admin_login/')
def logout_admin(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('admin_login')

def reg_user(request):
    data = Registration.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", d)

def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        email = request.POST['email']
        contact = request.POST['contact']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, email=email)
        Registration.objects.filter(user=request.user).update(contact=contact)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Registration.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/user_Login/')
def add_recipe(request, pid=None):
    recipe = None
    if pid:
        recipe = Recipe.objects.get(id=pid)

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if recipe_form.is_valid():
            ingredients_list = request.POST.getlist('ingredients[]')
            ingredients_text = ", ".join(ingredients_list)
            reg = Registration.objects.get(user=request.user)
            new_recipe = recipe_form.save(commit=False)
            new_recipe.register = reg
            new_recipe.ingredients = ingredients_text
            new_recipe.save()

            messages.success(request, "Update Recipe Successful")
            return redirect('manage_recipe')
    return render(request, 'add_recipe.html', locals())

@login_required(login_url='/user_Login/')
def comment(request, pid=None):
    if request.user.is_staff:
        recipe = None
        if pid:
            recipe = Comment.objects.get(id=pid)

        if request.method == "POST":
            recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

            if recipe_form.is_valid():
                ingredients_list = request.POST.getlist('ingredients[]')
                ingredients_text = ", ".join(ingredients_list)
                new_recipe = recipe_form.save(commit=False)
                new_recipe.ingredients = ingredients_text
                new_recipe.save()

                messages.success(request, "Update Comment Successful")
                return redirect('admin_index')
        return render(request, 'admin_comment.html', locals())
    else:
        recipe = None
        if pid:
            recipe = Comment.objects.get(id=pid)

        if request.method == "POST":
            recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

            if recipe_form.is_valid():
                ingredients_list = request.POST.getlist('ingredients[]')
                ingredients_text = ", ".join(ingredients_list)
                reg = Registration.objects.get(user=request.user)
                new_recipe = recipe_form.save(commit=False)
                new_recipe.register = reg
                new_recipe.ingredients = ingredients_text
                new_recipe.save()

                messages.success(request, "Update Comment Successful")
                return redirect('user_index')
        return render(request, 'comment.html', locals())

@login_required(login_url='/user_Login/')
def delete_recipe(request, pid):
    data = Recipe.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('manage_recipe')

# @login_required(login_url='/user_Login/')
# def add_recipe(request, pid=None):
#     recipe = None
#     if pid:
#         recipe = Recipe.objects.get(id=pid)
#     if request.method == "POST":
#         recipe = RecipeForm(request.POST, request.FILES, request.FILES, instance=recipe)
#         if recipe.is_valid():
#             reg = Registration.objects.get(user=request.user)
#             new_recipe = recipe.save()
#             new_recipe.register = reg
#             new_recipe.save()
#         messages.success(request, "Add Recipe Successful")
#         return redirect('manage_recipe')
#     return render(request, 'add_recipe.html', locals())


@login_required(login_url='/user_Login/')
def manage_recipe(request):
    reg = Registration.objects.get(user=request.user)
    data = Recipe.objects.filter(register=reg)
    d = {'data': data}
    return render(request, "manage_recipe.html", d)

@login_required(login_url='/user_Login/')
def admin_manage_recipe(request):
    data = Recipe.objects.filter()
    d = {'data': data}
    return render(request, "admin_manage_recipe.html", d)

def index_recipe(request):
    data = Recipe.objects.all()
    return render(request, "index_recipe.html", locals())

def add_comment(request, pid):
    data = Recipe.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Comment.objects.create(recipe=data, name=name, email=email, message=message)
        messages.success(request, "Add Comment Successful")
        return redirect('index')

    return render(request, "index_recipe_view.html", locals())

@login_required(login_url='/user_Login/')
def commentlist(request):
    action = request.GET.get('action')
    if action == "New":
        data = Comment.objects.filter(status=1)
    elif action == "Approval":
        data = Comment.objects.filter(status=2)
    elif action == "Rejected":
        data = Comment.objects.filter(status=3)
    elif action == "All":
        data = Comment.objects.filter()
    return render(request, "commentlist.html", locals())

def admin_comment_apply(request):
    action = request.GET.get('action')
    if action == "New":
        data = Comment.objects.filter(status=1)
    elif action == "Approval":
        data = Comment.objects.filter(status=2)
    elif action == "Rejected":
        data = Comment.objects.filter(status=3)
    elif action == "All":
        data = Comment.objects.filter()

    return render(request, "admin_comment_apply.html", locals())

def change_comment_status(request, pid):
    data = Comment.objects.get(id=pid)
    data.status = request.GET.get('action')
    data.save()
    messages.success(request, "comment Status Changed Successfull")
    return redirect('/admin_index/')

@login_required(login_url='/admin_login/')
def user_recipe(request, pid):
    register = Registration.objects.get(id=pid)
    data = Recipe.objects.filter(register__id=pid)
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    d = {'page': page}
    return render(request, "user_recipe.html", locals())

def add_contact(request):
    data = Contact2.objects.all()
    if request.method == "POST":
        contact = ContactForm(request.POST, request.FILES, instance=None)
        if contact.is_valid():
            new_contact = contact.save()
            new_contact.save()
        messages.success(request, "add_contact Successful")
        return redirect('index')
    return render(request, "add_contact.html", locals())

@login_required(login_url='/admin_login/')
def edit_contact(request, pid):
    contact = Contact.objects.get(id=pid)
    if request.method == "POST":
        data = ContactForm(request.POST, request.FILES, instance=contact)
        if data.is_valid():
            new_contact = data.save(commit=False)
            new_contact.status = "read"
            new_contact.save()
        messages.success(request, "Update Successful")
        return redirect("admin_index")
    return render(request, "edit_contact.html", locals())

@login_required(login_url='/admin_login/')
def contactlist(request):
    action = request.GET.get('action')
    if action == 'read':
        data = Contact.objects.filter(status='read')
    else:
        data = Contact.objects.filter(status='unread')
    d = {'data': data}
    return render(request, "view_contact.html", d)

@login_required(login_url='/admin_login/')
def delete_contact(request, pid):
    data = Contact.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('contactlist')

@login_required(login_url='/user_Login/')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        contact = request.POST['contact']

        user = User.objects.filter(id=request.user.id).update(first_name=fname)
        Registration.objects.filter(user=request.user).update(contact=contact)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Registration.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/user_Login/')
def user_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('user_change_password')
    return render(request, 'user_change_password.html')

@login_required(login_url='/admin_login/')
def admin_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

@login_required(login_url='/user_Login/')
def search_recipe(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Recipe.objects.filter(title__icontains=fromdate, register__user=request.user)
    return render(request, "search_recipe.html", locals())

@login_required(login_url='/admin_login/')
def admin_search_recipe(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Recipe.objects.filter(title__icontains=fromdate)
    return render(request, "admin_search_recipe.html", locals())

@login_required(login_url='/admin_login/')
def admin_user_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Registration.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "admin_user_report.html", locals())

@login_required(login_url='/admin_login/')
def admin_recipe_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Recipe.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "admin_recipe_report.html", locals())

@login_required(login_url='/admin_login/')
def admin_edit_recipe(request, pid=None):
    recipe = None
    if pid:
        recipe = Recipe.objects.get(id=pid)

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if recipe_form.is_valid():
            ingredients_list = request.POST.getlist('ingredients[]')
            ingredients_text = ", ".join(ingredients_list)
            new_recipe = recipe_form.save(commit=False)
            new_recipe.ingredients = ingredients_text
            new_recipe.save()

            messages.success(request, "Update Recipe Successful")
            return redirect('admin_manage_recipe')

    return render(request, 'admin_edit_recipe.html', locals())

@login_required(login_url='/admin_login/')
def admin_delete_recipe(request, pid):
    data = Recipe.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('admin_manage_recipe')

@login_required(login_url='/admin_login/')
def about(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        About.objects.filter(id=1).update(pagetitle=pagetitle, description=description)
        messages.success(request, "Update About Successful")
        return redirect('about')
    data = About.objects.get(id=1)
    return render(request, "about.html", locals())

@login_required(login_url='/admin_login/')
def contact(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']

        Contact2.objects.filter(id=3).update(pagetitle=pagetitle, description=description)
        messages.success(request, "Update Contact Successful")
        return redirect('contact')
    data = Contact2.objects.get(id=3)
    return render(request, "contact.html", locals())
