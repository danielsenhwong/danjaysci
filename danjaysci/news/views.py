from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# Create your views here.
def index(request):
    latest_post_list = Post.objects.order_by(-pub_date)[:5]
    context = {
        'latest_post_list': latest_post_list,
    }
    return render(request, 'news/index.html', context)

def detail(request, post_id):
    post = get_oibject_or_404(Post, pk = post_id)
    return render(request, 'news/detail.html', {'post': post})


