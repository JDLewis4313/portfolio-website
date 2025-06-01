from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, BlogPost, Technology, Skill, Contact

def home(request):
    """Homepage with featured projects and recent blog posts"""
    featured_projects = Project.objects.filter(featured=True, status='completed')[:3]
    recent_posts = BlogPost.objects.filter(published=True)[:3]
    technologies = Technology.objects.all()[:8]  # Show top 8 technologies
    
    context = {
        'featured_projects': featured_projects,
        'recent_posts': recent_posts,
        'technologies': technologies,
    }
    return render(request, 'main/home.html', context)

def projects(request):
    """Projects listing page with filtering"""
    projects_list = Project.objects.all()
    
    # Filter by technology if specified
    tech_filter = request.GET.get('technology')
    if tech_filter:
        projects_list = projects_list.filter(technologies__slug=tech_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        projects_list = projects_list.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(projects_list, 6)  # 6 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Get all technologies for filter dropdown
    technologies = Technology.objects.all()
    
    context = {
        'projects': projects,
        'technologies': technologies,
        'current_tech': tech_filter,
        'current_status': status_filter,
    }
    return render(request, 'main/projects.html', context)

def project_detail(request, slug):
    """Individual project detail page"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(
        technologies__in=project.technologies.all()
    ).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'main/project_detail.html', context)

def blog(request):
    """Blog listing page"""
    posts_list = BlogPost.objects.filter(published=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        posts_list = posts_list.filter(category=category_filter)
    
    # Pagination
    paginator = Paginator(posts_list, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = BlogPost.objects.values_list('category', flat=True).distinct()
    
    context = {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_filter,
    }
    return render(request, 'main/blog.html', context)

def blog_detail(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    
    # Increment view count
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        published=True,
        tags__in=post.tags.all()
    ).exclude(id=post.id).distinct()[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'main/blog_detail.html', context)

def about(request):
    """About page with skills"""
    skills_by_category = {}
    skills = Skill.objects.filter(show_on_resume=True)
    
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category,
    }
    return render(request, 'main/about.html', context)

def contact(request):
    """Contact page with form handling"""
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        contact_submission = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Success message (we'll add Django messages later)
        return render(request, 'main/contact.html', {'success': True})
    
    return render(request, 'main/contact.html')