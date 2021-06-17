from django.db import models
import datetime


class campus(models.Model):
    campusId = models.CharField(max_length=25,primary_key=True)
    campusName = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()


    class Meta:
        db_table = "campus"

class department(models.Model):
    deptId = models.CharField(max_length=25,primary_key=True)
    deptName = models.CharField(max_length=50)
    campus = models.ForeignKey(campus,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "department"


class studentAcademicDetails(models.Model):
    sid = models.CharField(max_length=25,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=8)
    dob = models.DateField()
    y_o_reg = models.BigIntegerField()
    deptId  = models.ForeignKey(department,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "academic_details"


class studentRegistration(models.Model):
    stdReg = models.OneToOneField(studentAcademicDetails,on_delete=models.CASCADE)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "student_registration"
    

class profRegistration(models.Model):
    pfRegId = models.CharField(max_length=25,primary_key=True)
    pname = models.CharField(max_length=50)
    email = models.EmailField()
    deptId  = models.ForeignKey(department,on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "prof_registration"
   
class course(models.Model):
    cid = models.CharField(max_length=25,primary_key=True)
    cname = models.CharField(max_length=100)
    ccredit = models.IntegerField()
    ctype = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "course"

class student_course(models.Model):
    student = models.ForeignKey(studentAcademicDetails,on_delete=models.CASCADE)
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "student_course"

class prof_course(models.Model):
    prof = models.ForeignKey(profRegistration,on_delete=models.CASCADE)
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "prof_course"


class department_course(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "department_course"


class examenroll(models.Model):
    courseId = models.ForeignKey(course,on_delete=models.CASCADE)
    profId = models.ForeignKey(profRegistration,on_delete=models.CASCADE)
    marks = models.IntegerField()
    date = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    isactive = models.CharField(max_length=3,default='Y')
    objects = models.Manager()

    class Meta:
        db_table = "exam"





