from django.conf.urls import url
from django.contrib import admin
from . import views
from .feeds import LatestPostsFeed
name='blog'

urlpatterns=[
    url(r'^$',views.post_list,name='post_list'),
    # url(r'^$',views.PostListView.as_view(),name='post_list'),  #通过在views.py定义PostListView来代替上面那种方法
                                                               #相当于没有使用post_list方法所以返回值会不一样
    url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,name='post_share'),
    url(r'^feed/$',LatestPostsFeed(),name='post_feed'),

]