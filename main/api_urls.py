# Create this file: main/api_urls.py

from django.urls import path
from . import api_views

urlpatterns = [
    # API Root
    path('', api_views.api_root, name='api_root'),
    
    # Projects
    path('projects/', api_views.ProjectListAPIView.as_view(), name='api_project_list'),
    path('projects/<slug:slug>/', api_views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
    
    # Technologies
    path('technologies/', api_views.TechnologyListAPIView.as_view(), name='api_technology_list'),
    
    # Blog
    path('blog/', api_views.BlogPostListAPIView.as_view(), name='api_blog_list'),
    path('blog/<slug:slug>/', api_views.BlogPostDetailAPIView.as_view(), name='api_blog_detail'),
    
    # Skills
    path('skills/', api_views.SkillListAPIView.as_view(), name='api_skill_list'),
    
    # Contact
    path('contact/', api_views.ContactCreateAPIView.as_view(), name='api_contact_create'),
]