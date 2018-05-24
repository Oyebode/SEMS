from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from .models import Course, Program, User, Upload, Student, New, Grade
from django.contrib.auth.models import User, Group
from elearning import settings
from django.db.models import Sum
from .forms import UploadFormFile, UpdateProfile, SelectTeachersForm, AddPostForm, GradeStudentsForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404


def programs_view(request):
    programs = Program.objects.all()
    return render (
        request,
        'programs_list.html',
        {'programs': programs},
    )


def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk)
    credits = Course.objects.aggregate(Sum('credits'))
    return render(
        request,
        'program_single.html',
        {'program': program, 'courses': courses, 'credits': credits},
    )


def students_view(request):
    students = Student.objects.all()
    programs = Program.objects.all()

    if request.method == 'GET':
        p = request.GET.get('program', '')
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')

        if p != '':
            students = Student.objects.filter(program=p, first_name__contains=name, email__contains=email)
        else:
            students = Student.objects.filter(first_name__contains=name, email__contains=email)

    return render(
        request,
        'students_list.html',
        {'students': students, 'programs': programs, 'media_url': settings.MEDIA_ROOT},
    )


def student_detail(request, pk):
    student = Student.objects.get(pk=pk)

    return render(
        request, 'student_profile.html', {'student': student},
    )


def course_detail(request, pk):
    course = Course.objects.get(pk = pk)
    files = Upload.objects.filter(course_id = pk)
    # group = Group.objects.get(name='Teacher')
    # users = group.user_set.all()
    users = User.objects.all()
    grades = Grade.objects.filter(student_id=request.user.id, course_id=pk)

    return render(
        request, 'course_single.html', {'usrs': users, 'course': course, 'files': files, 'grades': grades, 'media_url': settings.MEDIA_ROOT},
    )


def course_add(request):
    pass


def handle_file_upload(request, course_id):
    course = Course.objects.get(pk = course_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            return redirect('/programs/course/' + str(course_id))
    else:
        form = UploadFormFile()
    return render(
        request, 'upload_file_form.html', {'form': form, 'course': course},
    )


def user_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uid = Student.objects.latest('pk').pk
            return redirect('user_edit', pk=uid)
    else:
        form = UserCreationForm()
    return render(
        request, 'user_add.html', {'form': form},
    )


def user_edit(request, pk):
    user = Student.objects.get(pk=pk)

    instance = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = UpdateProfile(instance=instance)

    return render(
        request, 'user_profile_edit.html', {'form': form, 'user': user},
    )


def select_teacher(request, course_id):
    instance = get_object_or_404(Student, pk=1)
    if request.method == 'POST':
        form = SelectTeachersForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('programs')
    else:
        form = SelectTeachersForm(instance=instance)
    return render (
        request, 'select_teacher.html', {'form': form},
    )


def filter_courses_view(request):
    program = request.GET.get('program', None)
    course = Course.objects.filter(program=program).values('pk', 'name', )
    data = list(course)
    return JsonResponse(data, safe=False)


def home_view(request):
    uploads = Upload.objects.all().order_by('-upload_time')[:5]
    programs = Program.objects.all()
    users = User.objects.all().order_by('-last_login')[:5]
    news = New.objects.all().order_by('-create_date')[:3]

    return render (
        request, 'home.html', {'uploads': uploads, 'programs': programs, 'users': users, 'news': news},
    )


def post_single(request, pk):
    post = New.objects.get(pk=pk)
    posts = New.objects.all().order_by('-create_date')[:10]
    uploads = Upload.objects.all().order_by('-upload_time')[:5]

    return render (
        request, 'post_single.html', {'post': post, 'posts': posts, 'uploads': uploads},
    )

def post_add(request):

    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    return render (
        request, 'add_new_post.html', {'form': form},
    )


def grade_students(request, course_id):
    course = Course.objects.get(pk=course_id)
    students = User.objects.all()

    if request.method == 'POST':
        form = GradeStudentsForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST.getlist('student'))
            return redirect('course_detail', pk=course_id)
    else:
        form = GradeStudentsForm()

    return render (
        request, 'grade_students.html', {'course': course, 'form': form, 'students': students},
    )
