from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import campus,examenroll,studentRegistration,studentAcademicDetails,profRegistration,course,prof_course,student_course,department
from django.contrib import messages
from datetime import date
from datetime import datetime
import time

from django.http.response import StreamingHttpResponse
from cv2 import cv2
import numpy as np
# from .camera import VideoCamera
import dlib
from .import camera
from .import nextcamera

# Create your views here.
def index(request):
     return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def addexam(request):
    if request.method == 'POST':
        cid=request.POST['cid']
        date=request.POST['date']
        time=request.POST['starttime']
        endtime=request.POST['endtime']
        marks=request.POST['marks']
        obj=examenroll(courseId_id=cid,profId_id=request.session['pid'],marks =marks,date =date,starttime =time,endtime =endtime)
        obj.save()
        messages.info(request,"Do you want to add more exam")
        return render(request,'addexam.html')
    else:
        data = profRegistration.objects.get(pfRegId=request.session['pid'])
        dept = department.objects.get(deptId =data.deptId_id)
        cid=course.objects.filter(department=dept.deptName)
        print(cid)
        stu ={
             "courseId": cid
        }
        return render(request,'addexam.html',stu)
    

def exampage(request):
    return render(request,'exam.html')


def courseDetails(request):
    data = course.objects.filter(department=request.session['dept'])
    stu = {
        "student_number": data
    }
    return render(request,"studentCourseDetails.html", stu)

def profcourseDetails(request):
    data = course.objects.filter(department=request.session['dept'])
    prof = {
        "prof_number": data
    }
    return render(request,"profcourse.html", prof)

def registration(request):
    if request.method == 'POST':
        id = request.POST['id']
        uname = request.POST['username']
        mail = request.POST['email']
        Gen = request.POST['gender']
        Birthdate = request.POST['dob']
        reg = request.POST['year']
        pic = request.POST['pic']
        pasw = request.POST['password']
        ph = request.POST['phone']
        deptid = department.objects.get(deptName=request.POST['course'])
        obj = studentAcademicDetails(sid=id,name=uname,email=mail,gender=Gen,dob=Birthdate,y_o_reg=reg,deptId=deptid,image=pic)
        obj.save()
        obj1 = studentRegistration(stdReg_id=id,email=mail,password=pasw,phone=ph)
        obj1.save()
        request.session['id'] = request.POST['id']
        request.session['dept'] = request.POST['course']
        return redirect(courseDetails)
        
    else:
        return render(request,'registration.html')





def profregistration(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        pname = request.POST['username']
        mail = request.POST['email']
        deptid = department.objects.get(deptName=request.POST['course'])
        pasw = request.POST['password']
        ph = request.POST['phone']
        obj = profRegistration(pfRegId=pid,pname=pname,email=mail,deptId=deptid,password=pasw,phone=ph)
        obj.save()
        request.session['pid'] = request.POST['pid']
        request.session['dept'] = request.POST['course']
        return redirect(profcourseDetails)
    else:
        return render(request,'progReg.html')


def gotostu(request):
    data = student_course.objects.get(student_id=request.session['id'])
    dataa = examenroll.objects.get(courseId_id=data.course_id)
    now = datetime.now()
    print(now)
    print(dataa.date)
    print(date.today())
    if dataa.date == date.today() :
        print(dataa.starttime.hour)
        print(now.hour)
        print(dataa.starttime.minute)
        print(now.minute)
        if dataa.starttime.hour == now.hour or dataa.endtime.hour == now.hour :
            if dataa.starttime.minute <= now.minute and dataa.endtime.minute >= now.minute :
                print("Y1")
                dataa.isactive = 'Y'
                dataa.save()
        elif dataa.starttime.hour < now.hour and dataa.endtime.hour > now.hour :
            print("Y2")
            dataa.isactive = 'Y'
            dataa.save()
        else :
            print("N1")
            dataa.isactive = 'N'
            dataa.save()
    else:
        print("N2")
        dataa.isactive = 'N'
        dataa.save()
        print(dataa.isactive)
        print("Malini")
        print("Shalini")
    data = examenroll.objects.all().filter(courseId_id=data.course_id).values()
    
    print("malini")
    prof = {
        "profnumber": data
    }
    print(prof)
    return render(request,"profile.html",prof)

def gotofun(request):
    dataa = examenroll.objects.get(profId_id=request.session['pid'])
    now = datetime.now()
    print(now)
    print(dataa.date)
    print(date.today())
    if dataa.date == date.today() :
        print(dataa.starttime.hour)
        print(now.hour)
        print(dataa.starttime.minute)
        print(now.minute)
        if dataa.starttime.hour == now.hour or dataa.endtime.hour == now.hour :
            if dataa.starttime.minute <= now.minute and dataa.endtime.minute >= now.minute :
                print("Y1")
                dataa.isactive = 'Y'
                dataa.save()
        elif dataa.starttime.hour < now.hour and dataa.endtime.hour > now.hour :
            print("Y2")
            dataa.isactive = 'Y'
            dataa.save()
        else :
            print("N1")
            dataa.isactive = 'N'
            dataa.save()
    else:
        print("N2")
        dataa.isactive = 'N'
        dataa.save()
        print(dataa.isactive)
        print("Malini")
        print("Shalini")
    data = examenroll.objects.all().filter(profId_id=request.session['pid']).values()
    
    print("malini")
    prof = {
        "profnumber": data
    }
    print(prof)
    return render(request,"profile.html",prof)

def login(request):
    if request.method == 'POST':
        try:
            data =  studentRegistration.objects.get(stdReg_id=request.POST['id'])
            request.session['id'] = request.POST['id']
            if data.password == request.POST['psw']:
                return redirect(gotostu)
            else:
                messages.info(request," Password does not match")
                return render(request,'login.html')
        except:
            messages.info(request,"Student ID doesn't exists")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def proflogin(request):
    if request.method == 'POST':
        try:
            data =  profRegistration.objects.get(pfRegId=request.POST['pid'])
            print(data)
            print(data.deptId_id)
            request.session['pid'] = request.POST['pid']
            dept = department.objects.get(deptId =data.deptId_id)
            print(dept)
            request.session['dept'] = dept.deptName
            print(dept.deptName)
            # dataa = examenroll.objects.get(profId_id=request.POST['pid'])
            if data.password == request.POST['psw']:
                return redirect(gotofun)

            else:
                messages.info(request,"Password does not match")
                return render(request,'profLogin.html')
        except Exception as inst:
            print(inst)
            messages.info(request,"You do not set any exam")
            return render(request,'addexam.html')
    else:
        return render(request,'profLogin.html')



def profcourseenroll(request):
    if request.method == 'POST':
        courseID = request.POST.getlist('cid[]')
        pid = request.session['pid']
        for x in range(len(courseID)):
           obj=  prof_course(prof_id  = pid,course_id = courseID[x])
           obj.save()
        return redirect('/')


def courseenroll(request):
    if request.method == 'POST':
        courseID = request.POST.getlist('cid[]')
        p=request.session['id']
        for x in range(len(courseID)):
            obj= student_course(student_id = p,course_id = courseID[x])
            obj.save()
        return redirect('/') 

    else:
        return redirect('/') 

def facerecognization(request):
    return StreamingHttpResponse(camera.gen_frames(request.session['id']),content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed(request):
    return StreamingHttpResponse(camera.gen_frames(request.session['id']),content_type='multipart/x-mixed-replace; boundary=frame')


def videoframe(request):
    if request.method == 'POST':
        return render(request,'result.html')