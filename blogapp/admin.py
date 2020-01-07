from django.contrib import admin
from .models import Post, NewComment
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)
admin.site.register(NewComment)


