from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_("password"), max_length=150)
    phone = models.CharField(_("phone"), max_length=13, blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DanceStyle(models.Model):
    name = models.CharField(_("name"), max_length=25)
    description = models.TextField(_("description   "), max_length=300)

    def __str__(self):
        return self.name


class Studio(models.Model):
    address = models.CharField(_("address"), max_length=50)
    description = models.TextField(_("description"), max_length=300)

    def __str__(self):
        return self.address


class ReplenishmentHistory(models.Model):
    date = models.DateField(_("date"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    visits_amount = models.IntegerField(_("visits amount"))

    def __str__(self):
        return str(self.date)


class Lesson(models.Model):
    teacher = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    dance_style = models.ForeignKey(DanceStyle, verbose_name=_("dance style"), on_delete=models.CASCADE)

    date_time = models.DateTimeField(_("date"))
    description = models.TextField()
    max_people_count = models.IntegerField(_("max people count"))

    def __str__(self):
        return f"Урок от {self.teacher} в {self.date_time}"


class Subscription(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'role': 'student'}, on_delete=models.CASCADE)
    visits_amount = models.IntegerField(_("visits amount"), default=0)
    replenishment_history = models.ForeignKey('ReplenishmentHistory', verbose_name=_("replenishment history"), on_delete=models.SET_NULL, null=True)


class LessonSignup(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'role': 'student'}, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} записан на {self.lesson}"


class Achievement(models.Model):
    name = models.CharField(_("name"), max_length=25)
    description = models.TextField(_("description"), max_length=300)
    condition_of_receipt = models.TextField(verbose_name="Condition of Receipt")

    def __str__(self):
        return self.name


class StudentAchievement(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'role': 'student'}, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.student} - {self.achievement} on {self.date}"

    class Meta:
        unique_together = ('student', 'achievement')
