from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserRegistrationForm, UserLoginForm, TeacherLoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils import timezone
from django.http import JsonResponse
from .achievements import check_achievements
from .models import Subscription, ReplenishmentHistory, LessonSignup, Lesson, StudentAchievement


@login_required
def student_profile(request):
    return render(request, 'profile_user.html')


@login_required
def teacher_profile(request):
    return render(request, 'profile_teacher.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()

        if user.role == 'student':
            login(self.request, user)
            return redirect('/schedule_user/')
        else:
            messages.error(self.request, 'Войдите через кнопку "Преподаватель"')
            return redirect('login')


class TeacherLoginView(LoginView):
    form_class = TeacherLoginForm
    template_name = 'login_teacher.html'

    def form_valid(self, form):
        user = form.get_user()

        if user.role == 'teacher':
            login(self.request, user)
            return redirect('/schedule_teacher/')
        else:
            messages.error(self.request, 'Вы не являетесь преподавателем')
            return redirect('login_teacher')


def index(request):
    return render(request, "index.html")


def login_teacher(request):
    return render(request, "login_teacher.html")


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('register_done')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def register_done(request):
    return render(request, "register_done.html")


@login_required
def reporting(request):
    student_signups = LessonSignup.objects.filter(student=request.user)

    total_signups = student_signups.count()
    lessons = Lesson.objects.filter(lessonsignup__student=request.user).distinct()
    attendance_data = {
        'attended': student_signups.filter(attended=True).count(),
        'missed': student_signups.filter(attended=False).count(),
    }

    check_achievements(request.user)

    student_achievements = StudentAchievement.objects.filter(student=request.user).select_related('achievement')

    context = {
        'total_signups': total_signups,
        'lessons': lessons,
        'signups': student_signups,
        'attendance_data': attendance_data,
        'student_achievements': student_achievements,
    }
    return render(request, "reporting.html", context)



@login_required
def schedule_schools_for_teacher(request):
    lessons = Lesson.objects.all()
    return render(request, "schedule_schools_for_teacher.html", {'lessons': lessons})


@login_required
def schedule_schools_for_user(request):
    lessons = Lesson.objects.all()
    signups = LessonSignup.objects.filter(student=request.user)
    signed_up_lessons = signups.values_list('lesson', flat=True)

    if request.method == "POST":
        lesson_id = request.POST.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)

        if lesson_id not in signed_up_lessons:
            LessonSignup.objects.create(student=request.user, lesson=lesson)

        return redirect('schedule_schools_for_user')

    return render(request, 'schedule_schools_for_user.html', {
        'lessons': lessons,
        'signed_up_lessons': signed_up_lessons
    })


def schedule_teacher(request):
    if request.user.role != 'teacher':
        return redirect('profile_student')

    lessons = Lesson.objects.filter(teacher=request.user)
    context = {
        'lessons': lessons,
    }

    return render(request, "schedule_teacher.html", context)


@login_required
def schedule_user(request):
    user = request.user
    lessons = LessonSignup.objects.filter(student=user).select_related('lesson__teacher', 'lesson__studio',
                                                                       'lesson__dance_style')
    context = {
        'lessons': lessons,
    }
    return render(request, 'schedule_user.html', context)


def unsubscribe_lesson(request, lesson_id):
    signup = get_object_or_404(LessonSignup, lesson_id=lesson_id, student=request.user)
    if request.method == 'POST':
        signup.delete()
    return redirect('schedule_user')


@login_required
def subscription(request):
    subscription, created = Subscription.objects.get_or_create(student=request.user)
    subscription_options = ReplenishmentHistory.objects.all()

    return render(request, 'subscription.html', {
        'subscription': subscription,
        'subscription_options': subscription_options,
        'created': created
    })


@login_required
def extend_subscription(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id, student=request.user)

    if request.method == 'POST':
        visits_amount = int(request.POST['visits_amount'])
        price = float(request.POST['price'])

        replenishment = ReplenishmentHistory.objects.create(
            date=timezone.now(),
            price=price,
            visits_amount=visits_amount
        )

        subscription.visits_amount += visits_amount
        subscription.replenishment_history = replenishment
        subscription.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'new_visits_amount': subscription.visits_amount,
                'message': 'Абонемент успешно продлен!'
            })

        return redirect('subscription')

    return JsonResponse({'error': 'Недопустимый метод запроса'}, status=400)


@login_required
def purchase_subscription(request, option_id):
    option = ReplenishmentHistory.objects.get(id=option_id)
    subscription = Subscription.objects.get(student=request.user)
    subscription.visits_amount += option.visits_amount
    subscription.save()

    return redirect('subscription')



