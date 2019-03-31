from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm, PostForm
#from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required

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


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
        publish__year=year,publish__month=month,publish__day=day)
    
    # 列出对应评论
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 创建数据对象但不保存
            new_comment = comment_form.save(commit=False)
            new_comment.post = post #外键为当前文章
            new_comment.save()  # 评论写入
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.objects.all().filter(tags__in=post_tags_ids).exclude(id=post.id) #除去本文
    similar_post = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/detail.html', 
        {'post':post, 'comments':comments,'new_comment':new_comment,
        'comment_form':comment_form, 'similar_posts':similar_post,
        'url_post':'/{}/{}/{}/{}/{}'.format('blog',year,month,day,post.slug)})
    '''
    return render(request, 'blog/detail.html', 
        {'post':post, 'comments':comments,'new_comment':new_comment,
        'comment_form':comment_form,
        'url_post':'/{}/{}/{}/{}/{}'.format('blog',year,month,day,post.slug)})
    '''

@login_required
def create_post(request):
    new_post = None

    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            
            new_post.save()
            for i in post_form.cleaned_data['tags']:
                new_post.tags.add(i)
    else:
        post_form = PostForm()
    
    return render(request, 'blog/create_post.html', {'post_form':post_form, 
      'new_post':new_post,})
    