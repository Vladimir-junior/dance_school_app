from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import (
    User,
    DanceStyle,
    Studio,
    ReplenishmentHistory,
    Subscription,
    Lesson,
    LessonSignup,
    Achievement,
    StudentAchievement,
)


class UserAdmin(admin.ModelAdmin):
    list_display = ["user_full_name", "password", "role", "phone"]

    search_fields = ["first_name", "last_name"]

    fields = [
        "first_name",
        "last_name",
        "email",
        "password",
        "role",
        "phone",
    ]

    @admin.display(empty_value="-")
    def user_full_name(self, obj: User):
        return f'{obj.last_name} {obj.first_name}'


class DanceStyleAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ('name',)


class StudioAdmin(admin.ModelAdmin):
    list_display = ["address", "description"]
    search_fields = ('address',)


class ReplenishmentHistoryAdmin(admin.ModelAdmin):
    list_display = ["date", "price", "visits_amount"]
    search_fields = ('date',)
    ordering = ('-date',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'studio', 'dance_style', 'date_time', 'max_people_count')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'studio__address', 'dance_style__name')
    ordering = ('date_time',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('student', 'visits_amount', 'replenishment_history')
    search_fields = ('student__first_name', 'student__last_name', 'student__email')


class LessonSignupAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'date', 'attended')
    search_fields = ('student__first_name', 'student__last_name', 'lesson__teacher__first_name', 'lesson__teacher__last_name')
    ordering = ('-date',)


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'condition_of_receipt')
    search_fields = ('name',)


class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement', 'date')
    search_fields = ('student__email', 'achievement__name')


admin.site.register(User, UserAdmin)
admin.site.register(DanceStyle, DanceStyleAdmin)
admin.site.register(Studio, StudioAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonSignup, LessonSignupAdmin)
admin.site.register(ReplenishmentHistory, ReplenishmentHistoryAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(StudentAchievement, StudentAchievementAdmin)
admin.site.unregister(Group)
