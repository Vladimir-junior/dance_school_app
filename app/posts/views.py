from django.shortcuts import render
from .models import PostModel


def post_list(request):
    posts = PostModel.objects.all().order_by('-date')
    return render(request, 'post_list.html', {'posts': posts})



