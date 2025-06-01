from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Technology(models.Model):
    """Technology/skill model for organizing projects"""
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('framework', 'Framework'),
        ('language', 'Programming Language'),
        ('tool', 'Tool'),
        ('other', 'Other'),
    ])
    color = models.CharField(max_length=7, default='#3498db', help_text='Hex color for UI')
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = 'Technologies'
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """Tags for blog posts and general organization"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """Main project model for portfolio"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text='URL-friendly version of title')
    description = models.TextField(help_text='Brief project description')
    detailed_description = models.TextField(blank=True, help_text='Detailed project explanation')
    
    # Technical details
    technologies = models.ManyToManyField(Technology, related_name='projects')
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True, help_text='Live demo URL')
    
    # Project status and priority
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('development', 'In Development'),
        ('completed', 'Completed'),
        ('maintenance', 'Maintenance'),
        ('archived', 'Archived'),
    ], default='development')
    
    priority = models.IntegerField(default=0, help_text='Higher numbers show first')
    featured = models.BooleanField(default=False, help_text='Show on homepage')
    
    # Media
    thumbnail = models.ImageField(upload_to='project_thumbnails/', blank=True)
    screenshots = models.TextField(blank=True, help_text='JSON array of screenshot URLs')
    
    # Metadata
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    completion_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-priority', '-created_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

class BlogPost(models.Model):
    """Blog/learning journal for documenting progress"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text='Brief summary')
    
    # Categorization
    category = models.CharField(max_length=50, choices=[
        ('learning', 'Learning'),
        ('tutorial', 'Tutorial'),
        ('project_update', 'Project Update'),
        ('reflection', 'Reflection'),
        ('tech_review', 'Tech Review'),
        ('coursework', 'Coursework'),
    ], default='learning')
    
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')
    related_technologies = models.ManyToManyField(Technology, blank=True)
    related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Publishing
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Engagement
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date', '-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

class Skill(models.Model):
    """Skills and proficiency levels"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('database', 'Databases'),
        ('tools', 'Tools & Software'),
        ('soft_skills', 'Soft Skills'),
        ('concepts', 'Concepts & Methodologies'),
    ])
    
    proficiency = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ])
    
    years_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    show_on_resume = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', '-years_experience', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.proficiency})"

class Contact(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    response_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"