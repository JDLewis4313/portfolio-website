# Create this file: main/api_views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Project, Technology, BlogPost, Skill, Contact
from .serializers import (
    ProjectSerializer, ProjectListSerializer, TechnologySerializer,
    BlogPostSerializer, BlogPostListSerializer, SkillSerializer,
    ContactSerializer
)

# ===== PROJECT API VIEWS =====

class ProjectListAPIView(generics.ListAPIView):
    """GET /api/projects/ - List all projects"""
    serializer_class = ProjectListSerializer
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Filter by featured projects
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
            
        # Filter by technology
        technology = self.request.query_params.get('technology')
        if technology:
            queryset = queryset.filter(technologies__name__icontains=technology)
            
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.distinct()

class ProjectDetailAPIView(generics.RetrieveAPIView):
    """GET /api/projects/{slug}/ - Get single project details"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

# ===== TECHNOLOGY API VIEWS =====

class TechnologyListAPIView(generics.ListAPIView):
    """GET /api/technologies/ - List all technologies"""
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    
    def get_queryset(self):
        queryset = Technology.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

# ===== BLOG API VIEWS =====

class BlogPostListAPIView(generics.ListAPIView):
    """GET /api/blog/ - List published blog posts"""
    serializer_class = BlogPostListSerializer
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(published=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

class BlogPostDetailAPIView(generics.RetrieveAPIView):
    """GET /api/blog/{slug}/ - Get single blog post"""
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

# ===== SKILLS API VIEWS =====

class SkillListAPIView(generics.ListAPIView):
    """GET /api/skills/ - List skills"""
    serializer_class = SkillSerializer
    
    def get_queryset(self):
        queryset = Skill.objects.filter(show_on_resume=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

# ===== CONTACT API VIEWS =====

class ContactCreateAPIView(generics.CreateAPIView):
    """POST /api/contact/ - Submit contact form"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {'message': 'Contact form submitted successfully!'},
            status=status.HTTP_201_CREATED
        )

# ===== API ROOT VIEW =====

@api_view(['GET'])
def api_root(request):
    """GET /api/ - API endpoints overview"""
    return Response({
        'message': 'Portfolio API',
        'endpoints': {
            'projects': '/api/projects/',
            'project_detail': '/api/projects/{slug}/',
            'technologies': '/api/technologies/',
            'blog': '/api/blog/',
            'blog_detail': '/api/blog/{slug}/',
            'skills': '/api/skills/',
            'contact': '/api/contact/',
        },
        'filters': {
            'projects': '?featured=true&technology=django&status=completed',
            'technologies': '?category=frontend',
            'blog': '?category=learning',
            'skills': '?category=programming'
        }
    })