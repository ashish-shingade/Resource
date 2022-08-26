from django.shortcuts import HttpResponse
from ResourceApp.serializers import ResourcesSerializer
from django.http.response import JsonResponse
from Institutes.models import *
from ResourceApp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from datetime import datetime, timedelta
import json
import jwt
from ReSource import settings
from ReSource.utils import Check
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework import throttling
from rest_framework.decorators import api_view, throttle_classes
from login.models import Anamoly

# Create your views here.
# @csrf_exempt
# def send_mail_after_registration(request):
#     email = "rajeev.singh@vit.edu.in"
#     token = str(uuid.uuid4())
#     subject = 'Your accounts need to be verified'
#     message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
#     print(message)
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     print(email_from,recipient_list)
#     try:
#         send_mail(subject, message , email_from ,recipient_list ,fail_silently=False)
#     except Exception as e:
#         print(e)

@csrf_exempt
def register(request,id=0):
    if request.method == 'POST':    
        registerdata = json.loads(request.body)
        college = registerdata['institute']
        email = registerdata['username']
        password = registerdata['password']
        print(registerdata,id)
        if id in [1,2,3,7,8]:
            try:
                t = Institutes.objects.get(email = email)
                return JsonResponse({'status':409,"message":"User Exists"})
            except:
                db = Institutes(email= email ,password= password,name = college,role_id = id)
                db.save()
                return JsonResponse({'status':200,'username':email})
        elif id in [4,5]:
            try: 
                t = WorkForce.objects.get(email_id = email)
                return JsonResponse({'status':409,"message":"User Exists"})
            except:
                clg_obj = Institutes.objects.get(name = college)
                print(clg_obj)
                db = WorkForce(email_id= email ,password= password,role_id=id,institute = clg_obj)
                db.save()
                return JsonResponse({'status':200,'username':email})
        elif id == 6:
            try: 
                t = Students.objects.get(email = email)
                return JsonResponse({'status':409,"message":"User Exists"})
            except:
                clg_obj = Institutes.objects.get(name = college)
                print(clg_obj)
                db = Students(email= email ,password= password,institute_id = clg_obj)
                db.save()
                return JsonResponse({'status':200,'username':email})
        else:
            return HttpResponse("Registration FAILED")




# class CustomUserThrottle(throttling.UserRateThrottle):
#     def allow_request(self,request, view):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
        
#         db = Anamoly.objects.create(ip = ip)
#         return JsonResponse(data = {
#             'status':401,
#             'message': 'You have exhausted your limits'
#         })
        
# class CustomAnoThrottle(throttling.AnonRateThrottle):
#     def allow_request(self,request, view):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
        
#         # add in db
#         return JsonResponse(data = {
#             'status':401,
#             'message': 'You have exhausted your limits'
#         })


# @api_view(['GET', 'POST'])
# @throttle_classes([UserRateThrottle ,AnonRateThrottle ])
@csrf_exempt
def signup(request,id):
     if request.method == "POST":
        print('HI')
        print(id)
        try:
            logindata = json.loads(request.body)
            username = logindata['username']
            password = logindata['password']
            if id in [1,2,3]:
                print('HII')
                try:
                    t = Institutes.objects.get(email = username)
                    if t.status != 1:
                        return JsonResponse({'status':403,"message":"Verify Email First"})
                    # if check_password(password, t.password):
                    if password == t.password:
                        dt = datetime.now() + timedelta(days = 2)
                        token_data = {'user_id':t.id , 'role_id':id, 'exp': dt.timestamp()}
                        key = settings.SECRET_KEY
                        token = jwt.encode(token_data, key, 'HS256')
                        request.session['username'] = username
         
                          
                        return JsonResponse({'status':200,'username':username,'Role':id,'user_id':t.id , 'token':token})
                    else:
                        return JsonResponse({'status':403,"message":"Password Incorrect"}) 
                except Exception as e:
                    print(e)
                    return JsonResponse({'status':403,"message":"Email Does not exists"})
            elif id in [4,5,7,8,9]:
                try:
                    t = WorkForce.objects.get(email_id = username)
                    if t.status != 1:
                        return JsonResponse({'status':403,"message":"Verify Email First"})
                    if password == t.password:
                        dt = datetime.now()  + timedelta(days  = 2)             
                        token_data = {'user_id':t.id , 'role_id':id, 'exp': dt.timestamp()}
                        key = settings.SECRET_KEY
                        token = jwt.encode(token_data, key, 'HS256')
                        request.session['username'] = username   
                        return JsonResponse({'status':200,'username':username,'Role':id,'user_id':t.id , 'token':token})
                    else:
                        return JsonResponse({'status':403,"message":"Password Incorrect"}) 
                except:
                    return JsonResponse({'status':403,"message":"Email Does not exists"})
            elif id == 6:
                try:
                    t = Students.objects.get(email = username)
                    if t.status != 1:
                        return JsonResponse({'status':403,"message":"Verify Email First"})

                    if password == t.password:
                        dt = datetime.now() + timedelta(days = 2)
                        token_data = {'user_id':t.id , 'role_id':id ,'exp': dt.timestamp()}
                        key = settings.SECRET_KEY
                        token = jwt.encode(token_data, key, 'HS256')
                        request.session['username'] = username   
                        return JsonResponse({'status':200,'username':username,'Role':id,'user_id':t.id , 'token':token})
                    else:
                        return JsonResponse({'status':403,"message":"Password Incorrect"}) 
                except:
                    return JsonResponse({'status':403,"message":"Email Does not exists"})
            else:
                return JsonResponse({'status':403,"message":"LOGIN FAILED"})
            # redirect to success page
        except:    
            return JsonResponse({'status':403,"message":"LOGIN FAILED"})
    
@csrf_exempt
def logout(request):
    try:
        token = request.headers['Authorization']
    except:
        return JsonResponse(data = {
            'status':401,
            'message': "Unauthorized Access"
        })
    if Check.verify_token(token):
        return JsonResponse(data = {
            'status':401,
            'message': "Redirect to home"
        })
    else:
        return JsonResponse(data = {
            'status':401,
            'message':'Donot logout tempered token'
        })
    
@csrf_exempt
def fetch_role_id(request):
    print("HERE")
    try:
        token = request.headers['Authorization']
    except:
        return JsonResponse(data= {
            "message":"Unauthorized Access, Please Login",
            "status":401
        })
    print(token)
    info = Check.check_auth(token)
    if info['status'] == 0:
        return JsonResponse(data= {
            "message":"Unauthorized Access, Please Login",
            "status":401
        })
    role_id = info['role_id']
    user_id = info['user_id']
    return role_id
