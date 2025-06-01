from django.contrib import admin
from .models import Technology, Project, BlogPost, Tag, Skill, Contact

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'color']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'featured', 'created_date']
    list_filter = ['status', 'featured', 'technologies', 'created_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    ordering = ['-priority', '-created_date']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'published_date', 'views']
    list_filter = ['category', 'published', 'tags', 'related_technologies']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags', 'related_technologies']
    ordering = ['-created_date']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'years_experience', 'show_on_resume']
    list_filter = ['category', 'proficiency', 'show_on_resume']
    search_fields = ['name']
    ordering = ['category', '-years_experience']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_date', 'responded']
    list_filter = ['responded', 'created_date']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_date']
    ordering = ['-created_date']