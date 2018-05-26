from django import forms
from .models import Upload, Student, New, Grade
from django.contrib.auth.models import User

# Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('name', 'file', 'course', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


# Add/Edit User profile
class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'course', 'program', 'country', 'city', 'picture', 'website', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['program'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['website'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Website'})
        self.fields['course'].widget.attrs.update({'class': 'full-width'})


# Sign up form
class SignUpForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())

    username.widget.attrs.update({'class': 'form-control'})


    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.username)
            raise forms.ValidationError('User already exists')
        except User.DoesNotExist:
            return self.username


    def clean_password(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')

        if pw1 and pw2 and pw1 == pw2:
            return pw1
        raise forms.ValidationError("Password doesn't match")


# Select teachers for a specific course
class SelectTeachersForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})


class AddPostForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ('title', 'content', 'picture', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})


class GradeStudentsForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ('student', 'grade', )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        # self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['grade'].widget.attrs.update({'class': 'form-control'})


GradeStudentsFormSet = forms.modelformset_factory(Grade, form=GradeStudentsForm, extra=0)