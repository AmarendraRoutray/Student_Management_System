import datetime
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from student_App.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .forms import *


def admin_home(request):
    return render(request,'hod_template/home_content.html')


def add_staff(request):
    return render(request,'hod_template/add_staff_template.html')

def add_staff_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        
        try:
            user=CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,user_type=2)
            user.staffs.address=address
            user.save()
            
            messages.success(request,'Successfully Staff Added')
            return HttpResponseRedirect(reverse('add_staff'))
        except:
            messages.error(request,'Failed to add staff')
            return HttpResponseRedirect(reverse('/add_staff'))
        
        
def add_course(request):
    return render(request,'hod_template/add_course_template.html')


def add_course_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        course_name=request.POST.get('course')
        try:
            course_model=Course(course_name=course_name)
            course_model.save()
            messages.success(request,'Course Added Successfully')
            return HttpResponseRedirect(reverse('add_course'))
        except:
            messages.error(request,'Failed to add Course')
            return HttpResponseRedirect(reverse('add_course'))
        
        

def add_student(request):
    form=AddStudentForm()
    return render(request,'hod_template/add_student_template.html',{'form':form})



def add_student_save(request):
    if request.method!='POST':
        return HttpResponse('Method not Allowed')
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            address=form.cleaned_data['address']
            session_year_id=form.cleaned_data['session_year_id']
            course_id=form.cleaned_data['course']
            sex=form.cleaned_data['sex']
            
            # print(request.FILES['profile_pic'])
            
            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            
            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=3)
                user.students.address=address
                
                course_obj=Course.objects.get(id=course_id)
                user.students.course_id=course_obj
                
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=sex
                user.students.profile_pic=profile_pic_url
                user.save()
                
                messages.success(request,'Student added Successfully')
                return HttpResponseRedirect(reverse('add_student'))
                
            except:
                # print(e)
                messages.error(request,'Failed to add Student')
                return HttpResponseRedirect(reverse('add_student')) 
        else:
            form = AddStudentForm(request.POST)
            return render(request,'hod_template/add_student_template.html',{'form':form})

            
        
        
def add_subject(request):
    courses=Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/add_subject_template.html',{'courses':courses,'staffs':staffs})


def add_subject_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        subject=request.POST.get('subject')
        
        course_id=request.POST.get('course')
        course=Course.objects.get(id=course_id)
        
        staff_id=request.POST.get('staff')
        staff=CustomUser.objects.get(id=staff_id)
        try:
            subject=Subjects(subject_name=subject,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,'Subject added Successfully')
            return HttpResponseRedirect(reverse('add_subject'))
        except:
            messages.error(request,'Failed to add subject')
            return HttpResponseRedirect(reverse('add_subject'))


# manage

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,'hod_template/manage_staff_template.html',{'staffs':staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request,'hod_template/manage_student_template.html',{'students':students})

def manage_course(request):
    courses=Course.objects.all()
    return render(request,'hod_template/manage_course_template.html',{'courses':courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,'hod_template/manage_subject_template.html',{'subjects':subjects})



# edit

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,'hod_template/edit_staff_template.html',{'staff':staff,'id':staff_id})

def edit_staff_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        staff_id=request.POST.get('staff_id')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        address=request.POST.get('address')
        
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            
            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            
            messages.success(request,'Updated Successfully')
            return HttpResponseRedirect(reverse('edit_staff',kwargs={'staff_id':staff_id}))
        except:
            messages.error(request,'Failed to edit')
            return HttpResponseRedirect(reverse('edit_staff',kwargs={'staff_id':staff_id}))


def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    # form.fields['session_end'].initial=student.session_end_year
    
    return render(request,'hod_template/edit_student_template.html',{'form':form,'id':student_id,'username':student.admin.username})


def edit_student_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        student_id=request.session.get('student_id')
        if student_id==None:
            return HttpResponseRedirect(reverse('manage_student'))
        
        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            address=form.cleaned_data['address']
            session_year_id=form.cleaned_data['session_year_id']
            course_id=form.cleaned_data['course']
            sex=form.cleaned_data['sex']

            
            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES.get('profile_pic')
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None
            
            try:
                user = CustomUser.objects.get(id=student_id)
                user.username=username
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.save()
                
                student=Students.objects.get(admin=student_id)
                student.address=address
                
                session_year=SessionYearModel.object.get(id=session_year_id)
                student.session_year_id=session_year
                student.gender=sex
                
                course=Course.objects.get(id=course_id)
                student.course_id=course
                
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                    
                student.save()
                del request.session['student_id']
                
                messages.success(request,'Updated successfully')
                return HttpResponseRedirect(reverse('edit_student',kwargs={'student_id':student_id}))
            except Exception as e:
                print(e)
                messages.error(request,'Failed to edit')
                return HttpResponseRedirect(reverse('edit_student',kwargs={'student_id':student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,'hod_template/edit_student_template.html',{'form':form,'id':student_id,'username':student.admin.username})
        
        


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,'hod_template/edit_subject_template.html',{'subject':subject, 'courses':courses, 'staffs':staffs,'id':subject_id})



def edit_subject_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        subject_id=request.POST.get('subject_id')
        subject_name=request.POST.get('subject')
        course_id=request.POST.get('course')
        staff_id=request.POST.get('staff')
        
        try:
            subject=Subjects.objects.get(id=subject_id)
            course=Course.objects.get(id=course_id)
            staff=CustomUser.objects.get(id=staff_id)
            
            subject.subject_name=subject_name
            subject.staff_id=staff
            subject.course_id=course
            
            subject.save()
            
            messages.success(request,'Subject Updated Successfully')
            return HttpResponseRedirect(reverse('edit_subject',kwargs={'subject_id':subject_id}))
        
        except Exception as e:
            print(e)
            messages.error(request,'Failed to edit')
            return HttpResponseRedirect(reverse('edit_subject',kwargs={'subject_id':subject_id}))




def edit_course(request,course_id):
    course = Course.objects.get(id=course_id)
    return render(request,'hod_template/edit_course_template.html',{'course':course,'id':course_id})


def edit_course_save(request):
    if request.method!='POST':
        return HttpResponse('Method not allowed')
    else:
        course_id=request.POST.get('course_id')
        course_name=request.POST.get('course')
        
        try:
            course=Course.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            
            messages.success(request,'Updated Course Successfully')
            return HttpResponseRedirect(reverse('edit_course',kwargs={'course_id':course_id}))
        except:
            messages.error(request,'Failed to edit')
            return HttpResponseRedirect(reverse('edit_course',kwargs={'course_id':course_id}))
            
            
            
def manage_session(request):
    return render(request,'hod_template/manage_session_template.html')


def add_session_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('manage_session'))
    else:
        session_start_year=request.POST.get('session_start')
        session_end_year=request.POST.get('session_end')
        
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            
            messages.success(request,'Succesfully Added Session Year')
            return HttpResponseRedirect(reverse('manage_session'))
        except:
            messages.error(request,'Failed to add Session Year')
            return HttpResponseRedirect(reverse('manage_session'))