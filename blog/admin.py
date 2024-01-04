from django.contrib import admin

from blog.models import Post

# Register your models here.
# Jeito mais simples de incluir o modelo no site de administração:
''' admin.site.register(Post) '''

# Jeito mais elaborado, de incluir o modelo, com personalizações:

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','publish')