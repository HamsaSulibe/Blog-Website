from django.apps import AppConfig

#CONFIGRATION CLASS FOR MY BLOG APP , USED TO SETUP THE APP SPECIFIC SETTINGS
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
