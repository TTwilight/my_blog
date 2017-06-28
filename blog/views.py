from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post,Comment
from .forms import EmailPostForm,CommentForm
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
class PostListView(ListView):   #效果类似post_list
    queryset = Post.objects.all()
    context_object_name = 'posts'  #类似posts=queryset
    paginate_by = 3                #分页，3个一页
    template_name = 'post/list.html'

def post_list(request,tag_slug=None):
    object_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])

    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)

    return render(request,'post/list.html',{'posts':posts,'page':page,'tag':tag})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='Published',
                           publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    post_tag_ids=post.tags.values_list('id',flat=True)
    print('post_tag ',post_tag_ids)
    similar_posts=Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    print('similar ',similar_posts)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'post/detail.html',{'post':post,'comments':comments,'comment_form':comment_form,
                                              'new_comment':new_comment,'similar_posts': similar_posts})


def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        forms=EmailPostForm(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommands your reading {}'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject,message,'1063255195@qq.com',[cd['to'],],fail_silently=False)
            sent=True
    else:
        forms=EmailPostForm()

    return render(request,'post/share.html',{'sent':sent,'forms':forms,'post':post})