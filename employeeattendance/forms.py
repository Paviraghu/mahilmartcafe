from django import forms
from .models import EmployeeDetails,Gender,MaritalStatus,Shift,BloodGroup,Role,Attendance
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re   

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character (!,@,#,$,%,^,&,*, etc.)")

        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class EmployeeDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeDetailsForm, self).__init__(*args, **kwargs)
        self.fields['employee_code'].widget.attrs['readonly'] = True
        self.fields['DateofJoin'].widget.attrs['readonly'] = True


class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False 

class MaritalStatusForm(forms.ModelForm):
    class Meta:
        model = MaritalStatus
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee']

