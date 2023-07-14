from django.apps import AppConfig

class App1Config(AppConfig):  # [Your app name (첫 글자는 대문자로)]Config #Modify This
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'  #Your app name #Modify This
