from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import EmployeeDetails,Gender,MaritalStatus,Shift,Role,BloodGroup,Attendance
from .forms import GenderForm,MaritalStatusForm,ShiftForm,BloodGroupForm,RoleForm,EmployeeDetailsForm,AttendanceForm,RegistrationForm,LoginForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser or user.is_staff   # Admin check

def is_employee(user):
    return user.is_authenticated and not user.is_superuser and not user.is_staff  # Only employees

@login_required
def index(request):
    return render(request, "index.html")

def auth_view(request):

    login_form = LoginForm()
    reg_form = RegistrationForm()
    
    if request.method == "POST":
        if "login" in request.POST:
            login_form = LoginForm(request.POST)
            reg_form = RegistrationForm()
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    return redirect("index")   
                else:
                    messages.error(request, "Invalid credentials")
                    
        elif "register" in request.POST:
            reg_form = RegistrationForm(request.POST)
            login_form = LoginForm()
            if reg_form.is_valid():
                User.objects.create_user(
                    username=reg_form.cleaned_data['username'],
                    email=reg_form.cleaned_data['email'],
                    password=reg_form.cleaned_data['password']
                )
                messages.success(request, "Registration successful! Please login.")
                return redirect("auth")
        
        elif "reset_password" in request.POST:
            username = request.POST.get("username")
            new_password = request.POST.get("new_password")
            login_form = LoginForm()
            reg_form = RegistrationForm()
            try:
                user = User.objects.get(username=username)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully! Please login.")
                return redirect("auth")
            except User.DoesNotExist:
                messages.error(request, "Username not found.")
    
    return render(request, "auth.html", {"reg_form": reg_form, "login_form": login_form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have logged out successfully!")
        return redirect("auth")   
    return render(request, "logout.html")

@login_required
@user_passes_test(is_admin)
def add_employee(request):
    last_emp = EmployeeDetails.objects.all().order_by("id").last()
    if last_emp and last_emp.employee_code:
        try:
            last_number = int(last_emp.employee_code[1:])
        except:
            last_number = 0
        next_emp_code = "M" + str(last_number + 1).zfill(4)
    else:
        next_emp_code = "M0001"

    if request.method == "POST":
        EmployeeDetails.objects.create(
            employee_code=request.POST.get("employee_code"),
            EmployeeName=request.POST.get("EmployeeName"),
            Gender=request.POST.get("Gender"),
            Marital_status=request.POST.get("Marital_status"),
            Relative_name=request.POST.get("Relative_name"),
            Address=request.POST.get("Address"),
            Qualification=request.POST.get("Qualification"),
            DateofBirth=request.POST.get("DateofBirth"),
            DateofJoin=request.POST.get("DateofJoin"),
            Phone_no=request.POST.get("Phone_no"),
            Emergency_phone_no=request.POST.get("Emergency_phone_no"),
            Shift_timing=request.POST.get("Shift_timing"),
            Blood_group=request.POST.get("Blood_group"),
            Role=request.POST.get("Role"),
            Aadhaar_number=request.POST.get("Aadhaar_number")
        )
        return redirect("add_employee")

    genders = Gender.objects.all()
    marital_statuses = MaritalStatus.objects.all()
    shifts = Shift.objects.all()
    roles = Role.objects.all()
    blood_groups = BloodGroup.objects.all()

    return render(request, "add_employee.html", {
        "genders": genders,
        "marital_statuses": marital_statuses,
        "shifts": shifts,
        "roles": roles,
        "blood_groups": blood_groups,
        "next_emp_code": next_emp_code,
    })

@login_required
@user_passes_test(is_admin)
def employee_list(request):
    employees = EmployeeDetails.objects.all().order_by('id')

    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        employee = get_object_or_404(EmployeeDetails, id=emp_id)

        employee.employee_code = request.POST.get("employee_code")
        employee.EmployeeName = request.POST.get("EmployeeName")
        employee.Gender = request.POST.get("Gender")
        employee.Marital_status = request.POST.get("Marital_status")
        employee.Relative_name = request.POST.get("Relative_name")
        employee.Address = request.POST.get("Address")
        employee.Qualification = request.POST.get("Qualification")
        employee.DateofBirth = request.POST.get("DateofBirth")
        employee.DateofJoin = request.POST.get("DateofJoin")
        employee.Phone_no = request.POST.get("Phone_no")
        employee.Emergency_phone_no = request.POST.get("Emergency_phone_no")
        employee.Shift_timing = request.POST.get("Shift_timing")
        employee.Blood_group = request.POST.get("Blood_group")
        employee.Role = request.POST.get("Role")

        employee.save()
        return redirect('employee_list')

    return render(request, 'employee_list.html', {"employees": employees})

@login_required
@user_passes_test(is_admin)
def master_data_view(request):
    if request.method == "POST":
        gender_form = GenderForm(request.POST, prefix="gender")
        marital_form = MaritalStatusForm(request.POST, prefix="marital")
        shift_form = ShiftForm(request.POST, prefix="shift")
        blood_form = BloodGroupForm(request.POST, prefix="blood")
        role_form = RoleForm(request.POST, prefix="role")

        forms = [gender_form, marital_form, shift_form, blood_form, role_form]

        for form in forms:
            if any(request.POST.get(f"{form.prefix}-{name}") for name in form.fields):
                if form.is_valid():
                    form.save()

        return redirect('master_data')  

    else:
        gender_form = GenderForm(prefix="gender")
        marital_form = MaritalStatusForm(prefix="marital")
        shift_form = ShiftForm(prefix="shift")
        blood_form = BloodGroupForm(prefix="blood")
        role_form = RoleForm(prefix="role")

    context = {
        'gender_form': gender_form,
        'marital_form': marital_form,
        'shift_form': shift_form,
        'blood_form': blood_form,
        'role_form': role_form,
    }
    return render(request, "master_data.html", context)

@login_required
def mark_attendance(request):
    today = timezone.now().date()
    employees = EmployeeDetails.objects.all()
    selected_employee = None
    todays_records = Attendance.objects.none()
    verified = False

    emp_id = request.GET.get("emp_id")
    if emp_id:
        selected_employee = EmployeeDetails.objects.filter(id=emp_id).first()

    verified_emp_id = request.session.get("verified_emp_id")
    if selected_employee:
        if verified_emp_id and str(verified_emp_id) == str(selected_employee.id):
            verified = True
            todays_records = Attendance.objects.filter(
                date=today, employee=selected_employee
            ).order_by("id")
        else:
            if verified_emp_id:
                request.session.pop("verified_emp_id", None)

    if request.method == "POST" and request.POST.get("action") == "back":
        request.session.pop("verified_emp_id", None)
        return redirect("mark_attendance")

    if request.method == "POST" and request.POST.get("action") == "verify":
        emp_id = request.POST.get("employee_id")
        password = request.POST.get("password")
        employee = EmployeeDetails.objects.filter(id=emp_id).first()

        if not employee:
            messages.error(request, "Employee not found!")
            return redirect("mark_attendance")

        dob_year = str(employee.DateofBirth.year) if employee.DateofBirth else None

        if dob_year and password == dob_year:
            request.session["verified_emp_id"] = str(employee.id)

            todays_record = Attendance.objects.filter(date=today, employee=employee).first()
            if not todays_record:
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    status="Absent",
                    employee_name=employee.EmployeeName,
                    employee_code=employee.employee_code, 

                )

            return redirect(f"{request.path}?emp_id={employee.id}")
        else:
            messages.error(request, "Invalid password! Please enter correct DOB year.")
            return redirect(f"{request.path}?emp_id={employee.id}")

    if request.method == "POST" and request.POST.get("action") in ["checkin", "checkout"]:
        emp_id = request.POST.get("employee_id")
        action = request.POST.get("action")
        employee = EmployeeDetails.objects.filter(id=emp_id).first()

        if not employee:
            messages.error(request, "Employee not found!")
            return redirect("mark_attendance")

        if str(request.session.get("verified_emp_id")) != str(employee.id):
            messages.error(request, "Please verify password for this employee before marking attendance.")
            return redirect(f"{request.path}?emp_id={employee.id}")

        last_record = Attendance.objects.filter(employee=employee, date=today).last()

        if action == "checkin":
            if last_record and last_record.check_in and not last_record.check_out:
                messages.warning(request, f"{employee.EmployeeName} already Checked In! Please Check Out first.")
            elif last_record and last_record.check_in and last_record.check_out:
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    check_in=timezone.now().time(),
                    status="Present",
                    employee_name=employee.EmployeeName,
                    employee_code=employee.employee_code,  

                )
                messages.success(request, f"{employee.EmployeeName} Checked In for a new session.")
            else:
                last_record.check_in = timezone.now().time()
                last_record.status = "Present"
                last_record.save()
                messages.success(request, f"{employee.EmployeeName} Checked In successfully.")

        elif action == "checkout":
            if not last_record or not last_record.check_in:
                messages.error(request, f"{employee.EmployeeName} must Check In before Check Out!")
            elif last_record.check_out:
                messages.warning(request, f"{employee.EmployeeName} already Checked Out! Please Check In again for a new session.")
            else:
                last_record.check_out = timezone.now().time()
                last_record.save()
                messages.success(request, f"{employee.EmployeeName} Checked Out successfully.")

        return redirect(f"{request.path}?emp_id={employee.id}")

    return render(request, "attendance.html", {
        "employees": employees,
        "records": todays_records,
        "selected_employee": selected_employee,
        "verified": verified,
    })

@login_required
@user_passes_test(is_admin)
def admin_attendance_edit(request):
    today = timezone.now().date()
    records = Attendance.objects.none()

    from_date = request.GET.get("from_date", "").strip()
    to_date = request.GET.get("to_date", "").strip()
    employee_code = request.GET.get("employee_code", "").strip()

    qs = Attendance.objects.all()
    try:
        if from_date and to_date:
            from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            qs = qs.filter(date__range=(from_date_obj, to_date_obj))
        elif from_date:
            from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            qs = qs.filter(date__gte=from_date_obj)
        elif to_date:
            to_date_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            qs = qs.filter(date__lte=to_date_obj)
        else:
            qs = qs.filter(date=today)
    except ValueError:
        messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        qs = Attendance.objects.none()

    if employee_code:
        try:
            Attendance._meta.get_field("employee_code")
            qs = qs.filter(employee_code__icontains=employee_code)
        except Exception:
            try:
                fk_field = Attendance._meta.get_field("employee")
                employee_model = fk_field.related_model
            except Exception:
                employee_model = None

            candidate_names = ["EmployeeCode", "employee_code", "code", "emp_code"]

            used = False
            if employee_model:
                for fname in candidate_names:
                    try:
                        employee_model._meta.get_field(fname)
                        lookup = f"employee__{fname}__icontains"
                        qs = qs.filter(**{lookup: employee_code})
                        used = True
                        break
                    except Exception:
                        continue

            if not used:
                try:
                    Attendance._meta.get_field("employee_id")
                    qs = qs.filter(employee_id__icontains=employee_code)
                except Exception:
                    messages.warning(request, "Employee code filter could not be applied — check your Employee model field name.")

    qs = qs.order_by("-date", "employee__EmployeeName")

    records = qs

    if request.method == "POST":
        rec_id = request.POST.get("record_id")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        status = request.POST.get("status")

        record = Attendance.objects.filter(id=rec_id).first()
        if record:
            if check_in:
                record.check_in = check_in
            if check_out:
                record.check_out = check_out
            if status:
                record.status = status
            record.save()
            messages.success(request, f"Attendance updated for {record.employee.EmployeeName}")

        params = []
        if from_date:
            params.append(f"from_date={from_date}")
        if to_date:
            params.append(f"to_date={to_date}")
        if employee_code:
            params.append(f"employee_code={employee_code}")

        querystring = "&".join(params)
        redirect_url = request.path
        if querystring:
            redirect_url = f"{request.path}?{querystring}"
        return redirect(redirect_url)

    return render(request, "edit_attendance.html", {
        "records": records,
        "from_date": from_date,
        "to_date": to_date,
        "employee_code": employee_code,
    })