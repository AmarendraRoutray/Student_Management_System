from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from student_App.EmailBackEnd import EmailBackEnd
from student_App.models import *
from django.contrib import messages


def demo(request):
    return render(request,'demo.html')


def showLoginPage(request):
    return render(request,'loginpage.html')


def doLogin(request):
    if request.method!="POST":
        return HttpResponse('<h2>Method not Allowed</h2>')
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request,'Inavlid Login Details')
            return HttpResponseRedirect('/')
        

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse('User: '+request.user.email+' Usertype: '+request.user.user_type)
    else:
        return HttpResponse('Please Login')
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')