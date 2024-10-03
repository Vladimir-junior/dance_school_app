from django.shortcuts import get_object_or_404

from .models import LessonSignup, Achievement, StudentAchievement
from django.utils import timezone


def check_achievements(student):
    attended_count = LessonSignup.objects.filter(student=student, attended=True).count()
    if attended_count >= 5:
        unlock_achievement(student, "Посетил 5 занятий")

    if attended_count >= 10:
        unlock_achievement(student, "Посетил 10 занятий")

    if attended_count >= 15:
        unlock_achievement(student, "Посетил 15 занятий")

    distinct_styles_count = LessonSignup.objects.filter(student=student, attended=True).values('lesson__dance_style').distinct().count()
    if distinct_styles_count >= 3:
        unlock_achievement(student, "3 разных направления")

    if distinct_styles_count >= 5:
        unlock_achievement(student, "5 разных направления")


def unlock_achievement(student, achievement_name):
    achievement = get_object_or_404(Achievement, name=achievement_name)

    if not StudentAchievement.objects.filter(student=student, achievement=achievement).exists():
        StudentAchievement.objects.create(
            student=student,
            achievement=achievement,
            date=timezone.localdate()
        )
