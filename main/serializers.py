# Create this file: main/serializers.py

from rest_framework import serializers
from .models import Project, Technology, BlogPost, Skill, Contact, Tag

class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for Technology objects"""
    class Meta:
        model = Technology
        fields = ['id', 'name', 'category', 'color']

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects"""
    technologies = TechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'technologies', 'status', 'priority', 'featured',
            'github_url', 'demo_url', 'thumbnail',
            'created_date', 'updated_date', 'completion_date'
        ]

class ProjectListSerializer(serializers.ModelSerializer):
    """Simplified serializer for project listings"""
    technologies = TechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'technologies',
            'status', 'featured', 'github_url', 'demo_url', 'thumbnail'
        ]

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost objects"""
    tags = TagSerializer(many=True, read_only=True)
    related_technologies = TechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'category',
            'tags', 'related_technologies', 'published', 'published_date',
            'created_date', 'views'
        ]

class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for blog post listings"""
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'category',
            'tags', 'published_date', 'views'
        ]

class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill objects"""
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'proficiency',
            'years_experience', 'show_on_resume'
        ]

class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact form submissions"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        
    def create(self, validated_data):
        """Create a new contact submission"""
        return Contact.objects.create(**validated_data)