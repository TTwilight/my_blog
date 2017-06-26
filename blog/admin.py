from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')                              #显示所有的文章时，展示出来的字段
    list_filter = ('status','author','publish','created')  #侧边栏显示，用来过滤显示不同属性的文章
    search_fields = ('title','body')            #添加一个搜索框，可以根据title,body关键词来搜索文章
    prepopulated_fields = {'slug':('title',)}   #在add_posts时，当填写title时候,可以根据title预填写slug框
    raw_id_fields = ('author',)       #在add_posts时,用户添加变为搜索框，通过搜索添加用户
    date_hierarchy = 'publish'        #在搜索框下面添加一个通过时间快速导航的栏目
    ordering = ['status', 'publish']  #使文章默认按照status，publish排序

admin.site.register(Post,PostAdmin)

