from django import template

register=template.Library()
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

#在使用自定义的模板标签（template tags)之前，你必须使用{% load %}标签在模板（template）中来加载它们才能有效。
@register.simple_tag  #返回字符窜
def total_posts():              #一个Python函数定义了一个名为total_posts的标签，并用@register.simple-tag装饰器定义
    return Post.published.count()  # 此函数为一个简单标签（tag）并注册它。Django将会使用这个函数名作为标签（tag）名。


@register.inclusion_tag('post/latest_posts.html')  #返回渲染过后的模板latest_posts.html
def show_latest_posts(count=5):
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


