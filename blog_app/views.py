from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
#from .forms import EmailPostForm, CommentForm, PostForm
#from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# Create your views here.

def post_list(request, tag_slug=None):

    object_list = Post.objects.all()
    # 获取 Tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) #实例化Paginator显示3页
    page = request.GET.get('page') #当前页面

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)   #页数非整数返回第一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) #超过总页数返回最后一页
    return render(request, 'blog/list.html',{'page':page,'posts':posts,'tag':tag})


def post_detail():
    pass


def create_post():
    pass