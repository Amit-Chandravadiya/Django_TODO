from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from . import forms as frm
from django.contrib import messages
from .models import Profile as P
import uuid as u
from django.conf import settings
from django.core import mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required(login_url='/login')
def main(request):
    return render(request,'main.html')

def login_app(request):
    if request.method == 'POST':
       try:
            uid=User.objects.get(username=request.POST.get('username'))
            prf_obj=P.objects.get(user=uid)
            if prf_obj.is_verified:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request,'main.html')
                else:
                    messages.error(request,'Invalid username or password !')
                    return render(request,'login.html')
            else:
                messages.error(request,'User is not verified ! Check your mail ! ')
                return render(request,'login.html')

       except Exception as e:
                print(e)
                messages.error(request,'User doesn\'t exist ! ')
                return render(request,'login.html')



    return render(request,'login.html')

def Register(request):
    
    if request.method == 'GET':
        fo=frm.Usercreate()
        context={
            'form':fo
        }
        return render(request,'register.html',context)
    else:
        fo=frm.Usercreate(request.POST)
        context={
            'form':fo
        }
        if fo.is_valid():
            if User.objects.filter(email=request.POST.get('email')):
                messages.error(request,"This email is already Registered!")
                return render(request,'register.html',context)
            else:
                obj=fo.save()
                uid=User.objects.get(username=str(obj))
                if obj:
                    prf_obj=P.objects.create(user=uid)
                    prf_obj.save()
                    tkn=check_auth_token(uid)
                    send_mail_reg(request,request.POST.get('email'),uid)
                    return redirect('token_send')
        else:

            messages.error(request, str(fo.errors))
            return render(request,'register.html',context)


def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token.html')

# sending mail for token verification through email .
def send_mail_reg(request,email,uid):
    subject = " Your account needs to be verified ! "
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{check_auth_token(uid)}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    try:
        mail.send_mail(subject,message,email_from,recipient_list)
    except Exception as e:
        print(e)



def check_auth_token(uid):
    prf_obj=P.objects.get(user=uid)
    return str(prf_obj.auth_token)

def verify(request,tkn):
    try:
        prf_obj=P.objects.filter(auth_token=tkn).first()
        if prf_obj:
                
            if prf_obj.is_verified:
                messages.success(request,'Your Profile is already verified ! Please sign in to Utilise our services.')
                return redirect('success')
            else:
                prf_obj.is_verified=True
                prf_obj.save()
                messages.success(request,'Email is verified !')
                return redirect('success')
        else:
            messages.error(request,'Failed to verify your email !')
            return redirect('error_page')
    except Exception as e:
        print(e)
        return HttpResponse('404')

def error_page(request):
    return render(request,'error.html')

