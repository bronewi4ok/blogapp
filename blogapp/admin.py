from django.contrib import admin
from .models import Post, NewComment, Category, Slider
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    readonly_fields = ('slug_title', 'slug_date', )
    """fields = ['author', 'cover', 'title', 'text', 'created_date', 'published_date']"""
    list_display = ['__str__', 'author', 'slug_date', 'category']


@admin.register(NewComment)
class NewCommentAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'post', 'created_date']

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
      prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Slider)

# admin.site.register(Category, DraggableMPTTAdmin)


