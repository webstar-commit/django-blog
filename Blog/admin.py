from django.contrib import admin

from .models import Category,Post,Comment,BadWord,Reply,Tag


# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(BadWord)
admin.site.register(Comment)

admin.site.register(Tag)


admin.site.register(Reply)



