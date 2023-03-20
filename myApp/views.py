from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import filesUploadModel
import pandas as pd
import os
from django.conf import settings

# Create your views here.

@login_required(login_url='login_page')
def homeView(request):
    if request.user.is_superuser == False:
        return redirect('upload_file_page')
    context = {}
    filesUploadModelObj = filesUploadModel.objects.all()
    context['filesUploadModelObj'] = filesUploadModelObj
    return render(request,'home.html',context)


def loginView(request):
    context = {}
    if request.user.is_authenticated == True:
        return redirect('homepage')
    if request.method == 'POST':
        username = str(request.POST.get('username')).lower()
        password = str(request.POST.get('password'))
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return_message = 'Login Successfull'
            messages.warning(request, return_message)
            return redirect('homepage')
        else:
            return_message = 'Invalid Login Credentials'
            messages.warning(request, return_message)
            return redirect('/')
    return render(request,'login.html',context)

@login_required(login_url='login_page')
def logoutView(request):
    auth.logout(request)
    return redirect('homepage')


def registerView(request):
    context = {}
    if request.user.is_authenticated == True:
        return redirect('homepage')
    if request.method == 'POST':
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        list_values = [first_name, last_name, username, email, password1, password2]
        if '' in list_values or ' ' in list_values:
            response_message = 'Please Enter values in all fields!!'
        elif len(User.objects.filter(username=username)) > 0:
            response_message = 'User with Username already Exists'
        elif len(User.objects.filter(email=email)) > 0:
            response_message = 'User with Email already Exists'
        elif password1 != password2:
            response_message = "Passwords are not matching"
        else:
            user_obj = User.objects.create_user(email = email, username = username, first_name=first_name, last_name = last_name, password = password1)
            response_message = "User Created Successfully"
        messages.warning(request, response_message)
        return redirect('login_page')
    return render(request,'register.html',context)


@login_required(login_url='login_page')
def uploadFileView(request):
    context = {}
    if request.method == 'POST':
        response_message = ''
        uploaded_file = request.FILES.get('upload_file')
        name = uploaded_file.name
        if '.xls' in name or '.csv' in name or '.xlsm' in name or '.ods' in name :
            title = request.POST.get('title')
            try:
                filesUploadModelObj = filesUploadModel()
                filesUploadModelObj.title = title
                filesUploadModelObj.name = name
                filesUploadModelObj.file_uploaded = uploaded_file
                filesUploadModelObj.user = request.user
                filesUploadModelObj.save()
                response_message = "File Uploaded Successfully"
            except:
                response_message = "An error Occurred. Please Try Again"
        else:
            response_message = "Invalid File Format. Supported file formats are:- '.xls', '.xlsx'."
        messages.warning(request, response_message)
        return redirect('upload_file_page')
    return render(request,'upload_file.html', context)


@login_required(login_url='login_page')
def showDataView(request, pk):
    if request.user.is_superuser == False:
        return redirect('upload_file_page')
    context = {}
    filesUploadModelObj = filesUploadModel.objects.get(id=pk)
    file_uploaded = filesUploadModelObj.file_uploaded
    name = file_uploaded.name
    file_path = os.path.join(settings.MEDIA_ROOT, name)
    try:
        if '.csv' in name:
            df = pd.read_csv(f'{file_path}')
            df_object = df.to_html(classes='data', header="true")
            context['dataframe'] = df_object
        elif '.xls' in name or '.xlsx' in name:
            df = pd.read_excel(f'{file_path}', engine='openpyxl')
            df_object = df.to_html(classes='data', header="true")
            context['dataframe'] = df_object
    except:
        response_message = 'Unexpected Error Occurred!'
        messages.warning(request, response_message)
        return redirect('homepage')
    return render(request,'show_data.html', context)


@login_required(login_url='login_page')
def deleteFileView(request, pk):
    if request.user.is_superuser == False:
        return redirect('upload_file_page')
    response_message = 'File Deleted successfully!!'
    try:
        filesUploadModelObj = filesUploadModel.objects.get(id=pk)
        file_uploaded = filesUploadModelObj.file_uploaded
        name = file_uploaded.name
        file_path = os.path.join(settings.MEDIA_ROOT, name)
        os.remove(file_path)
        filesUploadModelObj.delete()
    except:
        response_message = 'An unexpected Error Occurred!!'
        messages.warning(request, response_message)
    return redirect('homepage')