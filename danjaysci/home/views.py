from django.shortcuts import render

from django.utils import timezone

from news.models import Post
from lab_members.models import LabMember

# Create your views here.
def index(request):
    posts = Post.objects.filter(pub_date__lte = timezone.now()).order_by('pub_date')
    context = {
        'posts': posts
    }
    return render(request, 'home/index.html', context)

def post_list(request):
    return render(request, 'home/post_list.html', {})
