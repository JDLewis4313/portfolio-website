# Replace your production settings section with this:

# Production settings
import os
if os.environ.get('RAILWAY_ENVIRONMENT'):
    DEBUG = False
    ALLOWED_HOSTS = ['.railway.app', '.up.railway.app', 'web-production-d54c7.up.railway.app']
    
    # Use Railway's PostgreSQL database
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
    
    # Static files for production
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Less strict security settings for now
    SECURE_SSL_REDIRECT = False  # Changed to False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'  # Changed from DENY to SAMEORIGIN