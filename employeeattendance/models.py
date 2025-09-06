from django.db import models
from django.utils import timezone


class EmployeeDetails(models.Model):
    id = models.AutoField(primary_key=True)  
    employee_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    EmployeeName = models.CharField(max_length=200)
    Gender = models.CharField(max_length=20)
    Marital_status = models.CharField(max_length=20)
    Relative_name = models.CharField(max_length=200, blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    Qualification = models.CharField(max_length=100, blank=True, null=True)
    DateofBirth = models.DateField()
    DateofJoin = models.DateField()
    Phone_no = models.CharField(max_length=15)
    Emergency_phone_no = models.CharField(max_length=15, blank=True, null=True)
    Shift_timing = models.CharField(max_length=50)
    Blood_group = models.CharField(max_length=10)
    Role = models.CharField(max_length=50)
    Aadhaar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.employee_code:
            last_employee = EmployeeDetails.objects.all().order_by("id").last()
            if last_employee:
                last_code = last_employee.employee_code
                try:
                    last_number = int(last_code[1:])  
                except:
                    last_number = 0
                new_number = last_number + 1
            else:
                new_number = 1
            self.employee_code = "M" + str(new_number).zfill(4)
        super().save(*args, **kwargs)

class Gender(models.Model):
    genderid=models.IntegerField(unique=True)
    gender = models.CharField(max_length=50)             

    def __str__(self):
        return self.gender


class MaritalStatus(models.Model):
    maritalid=models.IntegerField(unique=True)
    marital = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.marital


class Shift(models.Model):
    timeid=models.IntegerField(unique=True)
    time = models.CharField(max_length=100)             

    def __str__(self):
        return self.time


class BloodGroup(models.Model):
    bloodgroupid=models.IntegerField(unique=True)
    bloodgroup = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.bloodgroup


class Role(models.Model):
    roleid=models.IntegerField(unique=True)
    role = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.role
    

class Attendance(models.Model):
    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    employee_code = models.CharField(max_length=50, null=True, blank=True)  
    employee_name = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Absent")

    def save(self, *args, **kwargs):
        if self.employee:
            self.employee_name = self.employee.EmployeeName
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_name} - {self.date} - {self.status}"
  