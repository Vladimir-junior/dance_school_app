from django.db import models
from django.utils.translation import gettext_lazy as _


class PostModel(models.Model):
    title = models.TextField(_("title"), max_length=100)
    text = models.TextField(_("text"), max_length=500)
    date = models.DateField(_("date"))
    photo = models.ImageField(upload_to='post_photos/', null=True, blank=True, verbose_name="Photo")

    def __str__(self):
        return self.title
