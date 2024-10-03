from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.views import (
    index,
    register,
    register_done,
    UserLoginView,
    teacher_profile,
    student_profile,
    TeacherLoginView,
    logout_view,
    reporting,
    subscription,
    schedule_user,
    schedule_teacher,
    schedule_schools_for_user,
    schedule_schools_for_teacher,
    extend_subscription,
    purchase_subscription,
    unsubscribe_lesson,
)

from posts.views import post_list

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls, name='admin_panel'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('blog/', post_list, name='post_list'),
    path('login_teacher/', TeacherLoginView.as_view(), name='login_teacher'),
    path('register/', register, name='register'),
    path('register_done/', register_done, name='register_done'),
    path('student-profile/', student_profile, name='student-profile'),
    path('teacher-profile/', teacher_profile, name='teacher-profile'),
    path('reporting/', reporting, name='reporting'),
    path('subscription/', subscription, name='subscription'),
    path('schedule_user/', schedule_user, name='schedule_user'),
    path('schedule_teacher/', schedule_teacher, name='schedule_teacher'),
    path('schedule_schools_for_user/', schedule_schools_for_user, name='schedule_schools_for_user'),
    path('unsubscribe/<int:lesson_id>/', unsubscribe_lesson, name='unsubscribe_lesson'),
    path('schedule_schools_for_teacher/', schedule_schools_for_teacher, name='schedule_schools_for_teacher'),
    path('subscription/extend/<int:subscription_id>/', extend_subscription, name='extend_subscription'),
    path('subscription/purchase/<int:option_id>/', purchase_subscription, name='purchase_subscription'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
